"""Turn a typed instruction into a plan the runtime can execute.

Two backends behind one function. Claude parses free-form English against the
live scene inventory; a regex grammar handles the canonical phrasings with no
network and no API key, so the demo never depends on either. The fallback is not
a stub -- it is the path the console uses whenever ANTHROPIC_API_KEY is unset.

Note what the prompt does and does not do here. With an ACT checkpoint loaded it
*selects* a behaviour: ACT has no language input. Load a checkpoint that declares
one (SmolVLA, pi0) and `armlab.policies` passes the same text straight into the
model instead -- see the `policy` step below.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

MODEL = 'claude-opus-4-8'
LOOKUP = Path(__file__).resolve().parents[2] / 'computer-vision' / 'barcodes' / 'lookup_table.json'

_SAMPLE = re.compile(r'\b(SMP-\d{4})\b', re.I)
_BALANCE = re.compile(r'\bbalance[ _-]?(\d)\b', re.I)
_PICK = re.compile(r'\b(pick|grab|take|lift|get|collect)\b', re.I)
_PLACE = re.compile(r'\b(place|put|set|drop|deposit|load)\b', re.I)
_HOME = re.compile(r'\b(home|rest|neutral|stow|park)\b', re.I)
_POLICY = re.compile(r'\b(act|policy|cube|checkpoint|model|transfer)\b', re.I)
_BENCH = re.compile(r'\b(bench|down|back)\b', re.I)


@dataclass
class Plan:
    steps: list[dict] = field(default_factory=list)
    reason: str = ''
    source: str = 'grammar'     # 'claude' | 'grammar'

    def as_dict(self) -> dict:
        return {'steps': self.steps, 'reason': self.reason, 'source': self.source}


PLAN_TOOL = {
    'name': 'submit_plan',
    'description': 'Submit the sequence of robot actions that carries out the operator instruction.',
    'input_schema': {
        'type': 'object',
        'properties': {
            'steps': {
                'type': 'array',
                'description': 'Actions in the order they should run. Empty if the '
                               'instruction cannot be carried out.',
                'items': {
                    'type': 'object',
                    'properties': {
                        'skill': {
                            'type': 'string',
                            'enum': ['pick', 'place', 'home', 'stow', 'policy'],
                            'description': 'pick: grasp a labelled container and lift it. '
                                           'place: set whatever is held onto a target. '
                                           'home/stow: return both arms to the rest pose. '
                                           'policy: hand control to the loaded Hugging Face '
                                           'checkpoint (it does the cube-transfer task).',
                        },
                        'sample_id': {'type': 'string',
                                      'description': 'Container to pick, e.g. SMP-0009.'},
                        'target_id': {'type': 'string',
                                      'description': 'Instrument to bring it to, e.g. balance_2.'},
                        'seconds': {'type': 'number',
                                    'description': 'For `policy`: how long to run. Default 20.'},
                    },
                    'required': ['skill'],
                    'additionalProperties': False,
                },
            },
            'reason': {
                'type': 'string',
                'description': 'One short sentence. If steps is empty, say why.',
            },
        },
        'required': ['steps', 'reason'],
        'additionalProperties': False,
    },
}

SYSTEM = """You plan actions for a UR10e on a linear rail in a simulated chemistry lab.

Translate the operator's instruction into a sequence of skills, then call
submit_plan. Only ever use objects from the inventory you are given -- never
invent a sample id or a target.

Rules:
- `place` acts on whatever is currently held, so it must follow a `pick`.
- The targets are the five balances. `place` brings the vessel to one and sets it
  on the bench in front of it -- not on the balance, which is sealed behind a
  glass draft shield and has no pan a vessel could stand on. Say so if asked to
  put something *on* a balance, then plan the `place` anyway: bringing it there
  is the useful half of the request.
- If the instruction is about the loaded model, the policy or the checkpoint,
  emit a single `policy` step.
- If the instruction cannot be carried out, return no steps and explain why in
  one sentence. Never guess."""


def plan(prompt: str, inventory: dict | None = None) -> Plan:
    """Parse `prompt` into an executable plan, preferring Claude when available."""
    inventory = inventory or {}
    if os.environ.get('ANTHROPIC_API_KEY'):
        try:
            return _claude_plan(prompt, inventory)
        except Exception as exc:  # network, quota, bad key -- the demo carries on
            fallback = _grammar_plan(prompt, inventory)
            fallback.reason = f'{fallback.reason} (Claude unavailable: {exc})'.strip()
            return fallback
    return _grammar_plan(prompt, inventory)


def _claude_plan(prompt: str, inventory: dict) -> Plan:
    import anthropic

    context = (f'Containers in reach: {", ".join(inventory.get("samples", [])) or "none"}\n'
               f'Placement targets: {", ".join(inventory.get("targets", [])) or "none"}')
    response = anthropic.Anthropic().messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        tools=[PLAN_TOOL],
        tool_choice={'type': 'tool', 'name': 'submit_plan'},
        messages=[{'role': 'user', 'content': f'{context}\n\nInstruction: {prompt}'}],
    )
    for block in response.content:
        if block.type == 'tool_use':
            return _validate(Plan(steps=list(block.input.get('steps', [])),
                                  reason=str(block.input.get('reason', '')),
                                  source='claude'), inventory)
    return Plan(reason='Claude returned no plan', source='claude')


def _grammar_plan(prompt: str, inventory: dict) -> Plan:
    """Keyword parser over the canonical phrasings. Offline, instant, demo-safe."""
    text = prompt.strip()
    steps: list[dict] = []
    samples = [s.upper() for s in _SAMPLE.findall(text)]

    if _POLICY.search(text) and not samples:
        return _validate(Plan([{'skill': 'policy', 'args': {}}],
                              'running the loaded checkpoint'), inventory)
    # "put SMP-0084 on balance 1" names no pick verb but plainly needs one: you
    # cannot place what you are not holding.
    if samples and (_PICK.search(text) or _PLACE.search(text)):
        steps.append({'skill': 'pick', 'sample_id': samples[0]})
    if balance := _BALANCE.search(text):
        steps.append({'skill': 'place', 'target_id': f'balance_{balance.group(1)}'})
    elif steps and (_PLACE.search(text) or _BENCH.search(text)):
        # "put it down" with no instrument named: the nearest balance is as good
        # a destination as any, and it is the only kind of target there is.
        nearest = sorted(inventory.get('targets') or ())
        if nearest:
            steps.append({'skill': 'place', 'target_id': nearest[0]})
    if _HOME.search(text) or steps:
        steps.append({'skill': 'home'})
    if not steps:
        return Plan(reason=f'Could not parse {text!r}. Try "pick up SMP-0044 and bring it '
                           f'to balance 2", or set ANTHROPIC_API_KEY for free-form phrasing.')
    return _validate(Plan(steps, 'parsed by the offline grammar'), inventory)


def _validate(parsed: Plan, inventory: dict) -> Plan:
    """Drop steps naming objects this scene does not have, and normalise args.

    The catalogue of 200 sample ids is shared with the vision side, so an id the
    planner invents is caught here rather than surfacing as a runtime error.
    """
    known_samples = set(inventory.get('samples') or ())
    known_targets = set(inventory.get('targets') or ())
    catalogue = _catalogue()
    steps, dropped = [], []
    for raw in parsed.steps:
        skill = raw.get('skill')
        args = dict(raw.get('args') or {})
        for key in ('sample_id', 'target_id', 'seconds'):
            if raw.get(key) not in (None, ''):
                args[key] = raw[key]
        sample = args.get('sample_id')
        if sample is not None:
            sample = args['sample_id'] = str(sample).upper()
            if known_samples and sample not in known_samples:
                dropped.append(f'{sample} is not in this scene'
                               + ('' if not catalogue or sample in catalogue
                                  else ' and is not a catalogued sample'))
                continue
        target = args.get('target_id')
        if target is not None and known_targets and target not in known_targets:
            dropped.append(f'{target} is not a target in this scene')
            continue
        steps.append({'skill': skill, 'args': args})
    if dropped:
        parsed.reason = '; '.join([parsed.reason, *dropped]).strip('; ')
    parsed.steps = steps
    return parsed


def _catalogue() -> set[str]:
    """The 200 committed sample ids, shared with `computer-vision/labvision`.

    `entries` is keyed by EAN-13 code; the sample id is a field on each row.
    """
    try:
        table = json.loads(LOOKUP.read_text())
    except (OSError, ValueError):
        return set()
    return {row['sample_id'] for row in table.get('entries', {}).values()
            if isinstance(row, dict) and 'sample_id' in row}
