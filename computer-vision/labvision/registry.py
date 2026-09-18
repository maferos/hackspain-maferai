"""Sample registry: hash a sample record into an EAN-13 code and index it.

Each physical sample on the bench gets a barcode. The barcode carries no
information about the sample itself, only an identifier; everything a caller
wants to know is looked up from the identifier in a table. The identifier is
derived from the record by hashing, so the same record always produces the same
barcode and the table can be rebuilt from the records alone.

EAN-13 holds twelve free decimal digits, which is far less than a SHA-256
digest, so the digest is *truncated*: the first three digits are fixed to the
GS1 "200" prefix reserved for internal use, and the remaining nine come from the
digest modulo 10^9. Nine digits is about 30 bits, so for a catalogue of this
size collisions are vanishingly unlikely but not impossible, and
:func:`build_registry` resolves any it finds by re-hashing with a salt rather
than trusting the odds.
"""

import argparse
import hashlib
import json
import logging
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2

from labvision import ean13

logger = logging.getLogger(__name__)

INTERNAL_PREFIX = "200"
"""GS1 prefix reserved for in-store and internal codes."""

DIGITS_FROM_HASH = 9
"""Decimal digits of the payload taken from the digest."""

DEFAULT_SEED = 20260918
"""Seed fixing the default catalogue, so the table is reproducible."""

REGISTRY_VERSION = 4
"""Schema version written into the lookup table.

Version 2 introduced the liquid/powder split: ``flask_ml`` became
``container_ml`` and a ``phase`` field was added. Version 3 gave both phases the
same container series, so ``vessel_class`` no longer encoded phase and the
``jar_*`` classes were gone. Version 4 gives powders their own labware again,
the white HDPE bottles in ``assets/agrochemical-bottles``: powder rows move to
the ``bottle_*`` classes and every powder barcode changes, while liquid rows are
untouched. The field set is unchanged since 2, so the bumps exist to stop a
consumer keyed on the old class names reading a newer table as if nothing had
moved.
"""

# Nominal flask capacities in millilitres. 10, 20, 50 and 100 are standard
# volumetric capacities (ISO 1042); 30 is not in that series, whose neighbour is
# 25, but it is a common amber storage-bottle size for aroma chemicals, which
# suits a raw-material inventory better.
FLASK_VOLUMES_ML: tuple[float, ...] = (10.0, 20.0, 30.0, 50.0, 100.0)

# Nominal powder-bottle capacities in millilitres. These are the sizes of the
# white HDPE bottle kit in ``assets/agrochemical-bottles`` (Bote_100mL, _250mL,
# _500mL, _1L and _2L), which is the labware the simulation renders powders in,
# so a powder row must name a bottle that actually exists as a mesh. The kit's
# sixth bottle, the wide-mouth 1 L, is left out: it has the same nominal
# capacity as the regular 1 L, and container_ml could not tell the two apart.
#
# Version 3 of the catalogue put powders in the flask series above, so that a
# detector could not read "powder" off the vessel shape and skip the barcode.
# That shortcut is now open again -- a bottle means powder -- and is accepted:
# phase only tells the robot how to dispense, while the compound, which is what
# the barcode is for, is still a full cross product against bottle size.
BOTTLE_VOLUMES_ML: tuple[float, ...] = (100.0, 250.0, 500.0, 1000.0, 2000.0)

# Flavour and fragrance raw materials that are LIQUID at room temperature,
# with their CAS numbers.
LIQUID_MATERIALS: tuple[tuple[str, str], ...] = (
    ("Limonene", "5989-27-5"),
    ("Linalool", "78-70-6"),
    ("Geraniol", "106-24-1"),
    ("Citral", "5392-40-5"),
    ("Eugenol", "97-53-0"),
    ("Benzaldehyde", "100-52-7"),
    ("Citronellol", "106-22-9"),
    ("Nerol", "106-25-2"),
    ("Anethole", "104-46-1"),
    ("Cinnamaldehyde", "104-55-2"),
    ("Carvone", "99-49-0"),
    ("alpha-Pinene", "80-56-8"),
    ("alpha-Terpineol", "98-55-5"),
    ("Farnesol", "4602-84-0"),
    ("Nerolidol", "7212-44-4"),
    ("Benzyl acetate", "140-11-4"),
    ("Phenylethyl alcohol", "60-12-8"),
    ("Methyl salicylate", "119-36-8"),
    ("Linalyl acetate", "115-95-7"),
    ("cis-3-Hexen-1-ol", "928-96-1"),
)

# Raw materials that are SOLID at room temperature, handled as powders or
# crystals. The melting point in the comment is why each one is here.
POWDER_MATERIALS: tuple[tuple[str, str], ...] = (
    ("Vanillin", "121-33-5"),            # mp 81-83 C
    ("Ethylvanillin", "121-32-4"),       # mp 76-78 C
    ("Coumarin", "91-64-5"),             # mp 69-71 C
    ("Maltol", "118-71-8"),              # mp 160-164 C
    ("Ethyl maltol", "4940-11-8"),       # mp 89-92 C
    ("Menthol", "2216-51-5"),            # mp 36-38 C
    ("Thymol", "89-83-8"),               # mp 49-51 C
    ("Camphor", "76-22-2"),              # mp 175-177 C
    ("Piperonal", "120-57-0"),           # mp 35-37 C, heliotropin
    ("Indole", "120-72-9"),              # mp 52-54 C
    ("Musk ketone", "81-14-1"),          # mp 135-137 C
    ("Tonalide", "21145-77-7"),          # mp 54 C
    ("Sclareolide", "564-20-5"),         # mp 120-124 C
    ("Cedryl acetate", "77-54-3"),       # mp 44-46 C
    ("Methyl cinnamate", "103-26-4"),    # mp 34-38 C
    ("Benzyl cinnamate", "103-41-3"),    # mp 39 C
    ("Cinnamic acid", "621-82-9"),       # mp 133 C
    ("Diphenyl ether", "101-84-8"),      # mp 27-29 C
    ("Exaltolide", "106-02-5"),          # mp 35 C
    ("Phenylacetic acid", "103-82-2"),   # mp 76-78 C
)


class RegistryError(Exception):
    """Raised when a registry cannot be built, read or resolved."""


@dataclass(frozen=True)
class PhaseSpec:
    """One physical phase and the labware that goes with it.

    Attributes:
        name: ``"liquid"`` or ``"powder"``, as written into the table.
        prefix: Sample-id prefix, ``SMP`` for liquids and ``PWD`` for powders.
        vessel: Vessel noun used to build the detector class name, ``"flask"``
            for liquids and ``"bottle"`` for powders.
        materials: Compounds in this phase, as (name, CAS) pairs.
        containers_ml: Nominal container capacities offered for this phase.
    """

    name: str
    prefix: str
    vessel: str
    materials: tuple[tuple[str, str], ...]
    containers_ml: tuple[float, ...]

    @property
    def size(self) -> int:
        """Number of samples in this phase's grid

        Returns:
            The cross-product size, compounds times container sizes.
        """
        return len(self.materials) * len(self.containers_ml)


LIQUID = PhaseSpec("liquid", "SMP", "flask", LIQUID_MATERIALS, FLASK_VOLUMES_ML)
POWDER = PhaseSpec("powder", "PWD", "bottle", POWDER_MATERIALS, BOTTLE_VOLUMES_ML)

PHASES: tuple[PhaseSpec, ...] = (LIQUID, POWDER)
"""Every phase in the catalogue, in the order they are generated."""

DEFAULT_SAMPLE_COUNT = sum(p.size for p in PHASES)
"""Size of the default catalogue: every compound in every container size.

Derived from PHASES rather than written down, so adding a compound or a
container size cannot leave it stale.
"""


@dataclass(frozen=True)
class Sample:
    """One compound in one container size: a single cell of a phase's grid.

    Each phase's catalogue is the full cross product of its materials and its
    container sizes, so a sample is uniquely identified by (phase, material,
    container). The lot is incidental detail carried for realism.

    Attributes:
        sample_id: Human-facing identifier, ``SMP-0001`` for liquids and
            ``PWD-0001`` for powders.
        material: Raw material the container holds.
        cas: CAS registry number of that material.
        phase: ``"liquid"`` or ``"powder"``. This drives how the robot dispenses
            the contents, and decides the labware: flasks or bottles.
        container_ml: Nominal container capacity in millilitres, from the
            phase's own series: flasks for liquids, bottles for powders.
        lot: Supplier lot reference.
    """

    sample_id: str
    material: str
    cas: str
    phase: str
    container_ml: float
    lot: str

    @property
    def vessel_class(self) -> str:
        """Detector class name, such as ``flask_50ml`` or ``bottle_500ml``

        Derived rather than stored, so it cannot drift from phase or
        container_ml. The vessel noun comes from the phase, so the class name
        gives the phase away but never the compound.

        Returns:
            The class label the vision model would predict. Ten values in all,
            five flasks and five bottles.

        Raises:
            RegistryError: If phase is not a known phase name.

        Example:
            >>> Sample("SMP-1", "Limonene", "5989-27-5", "liquid", 50.0,
            ...        "L1").vessel_class
            'flask_50ml'
            >>> Sample("PWD-1", "Vanillin", "121-33-5", "powder", 1000.0,
            ...        "L1").vessel_class
            'bottle_1000ml'
        """
        for spec in PHASES:
            if spec.name == self.phase:
                return f"{spec.vessel}_{self.container_ml:g}ml"
        raise RegistryError(f"unknown phase: {self.phase!r}")

    def payload(self) -> str:
        """Render the record as the canonical string that gets hashed

        Field order and formatting are fixed here because changing them changes
        every barcode in the catalogue.

        Returns:
            A newline-free, pipe-separated canonical form of the record.

        Example:
            >>> Sample("SMP-0001", "Limonene", "5989-27-5", "liquid", 50.0,
            ...        "LOT-1234").payload()
            'SMP-0001|Limonene|5989-27-5|liquid|50|LOT-1234'
        """
        return "|".join((
            self.sample_id,
            self.material,
            self.cas,
            self.phase,
            f"{self.container_ml:g}",
            self.lot,
        ))


@dataclass(frozen=True)
class Entry:
    """A registry row: one sample, its digest and the barcode that points at it.

    Attributes:
        code: The 13-digit EAN-13 printed on the label.
        sha256: Full hex digest of the sample's canonical payload.
        salt: Re-hash counter used to break a collision; 0 for almost every row.
        sample: The record the code resolves to.
    """

    code: str
    sha256: str
    salt: int
    sample: Sample


def sha256_of(sample: Sample, salt: int = 0) -> str:
    """Hash a sample's canonical payload

    Args:
        sample: The record to hash.
        salt: Re-hash counter, appended to the payload. Only non-zero when an
            earlier attempt collided. Defaults to 0.

    Returns:
        The lowercase hex SHA-256 digest.

    Example:
        >>> s = Sample("SMP-0001", "Limonene", "5989-27-5", "liquid", 50.0, "L1")
        >>> len(sha256_of(s))
        64
    """
    payload = sample.payload() if salt == 0 else f"{sample.payload()}#{salt}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def code_from_digest(digest: str) -> str:
    """Fold a hex digest into a 13-digit EAN-13 under the internal prefix

    Args:
        digest: A hex digest, normally 64 characters of SHA-256.

    Returns:
        The 13-digit EAN-13 code, check digit included.

    Raises:
        RegistryError: If digest is not valid hexadecimal.

    Example:
        >>> code_from_digest("00" * 32)
        '2000000000008'
    """
    try:
        value = int(digest, 16)
    except ValueError as e:
        raise RegistryError(f"digest is not hexadecimal: {digest!r}") from e
    tail = str(value % 10**DIGITS_FROM_HASH).zfill(DIGITS_FROM_HASH)
    return ean13.full_code(INTERNAL_PREFIX + tail)


def build_registry(samples: list[Sample]) -> list[Entry]:
    """Hash every sample into a unique EAN-13 code

    Two distinct samples folding onto the same twelve digits is possible, if
    unlikely. When it happens the later sample is re-hashed with an incrementing
    salt until it lands somewhere free, and the salt is recorded so the mapping
    stays reproducible.

    Args:
        samples: The records to index. Sample ids must be unique.

    Returns:
        One entry per sample, in the order given.

    Raises:
        RegistryError: If two samples share a sample_id, or if a collision
            cannot be resolved within a reasonable number of re-hashes.

    Example:
        >>> entries = build_registry(default_samples(3))
        >>> len({e.code for e in entries})
        3
    """
    seen_ids: set[str] = set()
    for sample in samples:
        if sample.sample_id in seen_ids:
            raise RegistryError(f"duplicate sample_id: {sample.sample_id}")
        seen_ids.add(sample.sample_id)

    entries: list[Entry] = []
    taken: dict[str, str] = {}
    for sample in samples:
        for salt in range(64):
            digest = sha256_of(sample, salt)
            code = code_from_digest(digest)
            if code not in taken:
                taken[code] = sample.sample_id
                entries.append(Entry(code, digest, salt, sample))
                break
            logger.warning(
                "code %s collided between %s and %s, re-hashing with salt %d",
                code, taken[code], sample.sample_id, salt + 1,
            )
        else:
            raise RegistryError(
                f"could not find a free code for {sample.sample_id}"
            )
    return entries


def default_samples(
    count: int = DEFAULT_SAMPLE_COUNT,
    seed: int = DEFAULT_SEED,
) -> list[Sample]:
    """Build the reproducible default catalogue of samples

    For each phase the catalogue is the **full cross product** of its materials
    and its container sizes — every compound in every size. Liquids come first
    (20 compounds x 5 flasks), then powders (20 x 5 bottles), 200 rows in all.
    Material varies slowest, so SMP-0001..0005 are the five flask sizes of the
    first liquid.

    Taking the cross product rather than cycling both lists in step matters:
    cycling 20 materials against 5 sizes locks each compound to one size, which
    would let a vision model infer the compound from container size alone and
    never read the barcode.

    Only the lot is random, under a fixed seed.

    Args:
        count: How many samples to produce, taken from the front of the
            catalogue. Defaults to DEFAULT_SAMPLE_COUNT, the whole of it.
        seed: Seed for the lot draws. Defaults to DEFAULT_SEED.

    Returns:
        The catalogue, liquids then powders, each ordered by sample id.

    Raises:
        ValueError: If count is not positive or exceeds the catalogue size.

    Example:
        >>> s = default_samples()
        >>> s[0].material, s[0].container_ml, s[0].phase
        ('Limonene', 10.0, 'liquid')
        >>> s[100].sample_id, s[100].material, s[100].container_ml
        ('PWD-0001', 'Vanillin', 100.0)
    """
    if count < 1:
        raise ValueError(f"count must be >= 1, got {count}")
    if count > DEFAULT_SAMPLE_COUNT:
        shape = " + ".join(
            f"{len(p.materials)}x{len(p.containers_ml)}" for p in PHASES
        )
        raise ValueError(
            f"count must be <= {DEFAULT_SAMPLE_COUNT} ({shape}), got {count}"
        )
    rng = random.Random(seed)
    samples: list[Sample] = []
    for spec in PHASES:
        for i, (material, cas) in enumerate(spec.materials):
            for j, container_ml in enumerate(spec.containers_ml):
                if len(samples) >= count:
                    return samples
                index = i * len(spec.containers_ml) + j + 1
                samples.append(Sample(
                    sample_id=f"{spec.prefix}-{index:04d}",
                    material=material,
                    cas=cas,
                    phase=spec.name,
                    container_ml=container_ml,
                    lot=f"LOT-{rng.randint(10000, 99999)}",
                ))
    return samples


def to_table(entries: list[Entry]) -> dict[str, object]:
    """Shape a registry into the JSON lookup table

    Args:
        entries: Registry rows, as returned by build_registry.

    Returns:
        A JSON-serialisable table keyed by barcode under ``entries``.

    Example:
        >>> to_table(build_registry(default_samples(1)))["count"]
        1
    """
    return {
        "version": REGISTRY_VERSION,
        "symbology": "EAN-13",
        "id_scheme": (
            f"sha256(sample.payload()) mod 10^{DIGITS_FROM_HASH}, "
            f"prefixed {INTERNAL_PREFIX!r}, EAN-13 check digit appended"
        ),
        "phases": {
            spec.name: {
                "vessel": spec.vessel,
                "prefix": spec.prefix,
                "materials": len(spec.materials),
                "containers_ml": list(spec.containers_ml),
                "count": spec.size,
            }
            for spec in PHASES
        },
        "count": len(entries),
        "entries": {
            e.code: {
                "sha256": e.sha256,
                "salt": e.salt,
                **asdict(e.sample),
                # vessel_class is a property, so asdict does not reach it, but
                # consumers want the detector class name in the table.
                "vessel_class": e.sample.vessel_class,
            }
            for e in entries
        },
    }


def save_table(entries: list[Entry], path: Path) -> Path:
    """Write the lookup table to disk as JSON

    Args:
        entries: Registry rows to serialise.
        path: Destination file. Parent directories are created.

    Returns:
        The path written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_table(entries), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def load_table(path: Path) -> dict[str, dict[str, object]]:
    """Read a lookup table and return its barcode-keyed entries

    Args:
        path: A JSON file previously written by save_table.

    Returns:
        A mapping from 13-digit code to the sample record and its digest.

    Raises:
        RegistryError: If the file is missing, is not valid JSON, or was
            written by an incompatible schema version.

    Example:
        >>> _ = save_table(build_registry(default_samples(2)), Path("/tmp/t.json"))
        >>> len(load_table(Path("/tmp/t.json")))
        2
    """
    if not path.exists():
        raise RegistryError(f"lookup table not found: {path}")
    try:
        table = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise RegistryError(f"lookup table is not valid JSON: {path}") from e
    if table.get("version") != REGISTRY_VERSION:
        raise RegistryError(
            f"lookup table version {table.get('version')} is not "
            f"{REGISTRY_VERSION}: {path}"
        )
    return table["entries"]


def write_label_images(
    entries: list[Entry],
    out_dir: Path,
    module_px: int = 4,
) -> list[Path]:
    """Render one printed label per registry row

    Args:
        entries: Registry rows to render.
        out_dir: Directory for the PNGs. Created if absent.
        module_px: Pixels per module. Defaults to 4.

    Returns:
        The paths written, in entry order.

    Raises:
        RegistryError: If OpenCV refuses to write one of the files.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for entry in entries:
        image = ean13.render_tag(
            entry.code,
            caption=entry.sample.material,
            subcaption=(
                f"{entry.sample.sample_id}  {entry.sample.container_ml:g} ML  "
                f"{entry.sample.phase.upper()}"
            ),
            module_px=module_px,
        )
        path = out_dir / f"{entry.sample.sample_id}_{entry.code}.png"
        if not cv2.imwrite(str(path), image):
            raise RegistryError(f"could not write label image: {path}")
        paths.append(path)
    return paths


def main() -> None:
    """Generate the barcode catalogue and its lookup table."""
    parser = argparse.ArgumentParser(
        description="Generate sample barcodes and their lookup table.",
    )
    parser.add_argument(
        "out_dir", type=Path, nargs="?", default=Path("barcodes"),
        help="Directory for the label PNGs and lookup_table.json.",
    )
    parser.add_argument(
        "--count", type=int, default=DEFAULT_SAMPLE_COUNT,
        help=f"How many samples to generate (default: {DEFAULT_SAMPLE_COUNT}).",
    )
    parser.add_argument(
        "--seed", type=int, default=DEFAULT_SEED,
        help=f"Seed for the catalogue (default: {DEFAULT_SEED}).",
    )
    parser.add_argument(
        "--module-px", type=int, default=4,
        help="Pixels per barcode module (default: 4).",
    )
    parser.add_argument(
        "--no-images", action="store_true",
        help="Write only the lookup table, skipping the label PNGs.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    entries = build_registry(default_samples(args.count, args.seed))
    table_path = save_table(entries, args.out_dir / "lookup_table.json")
    print(f"{len(entries)} codes -> {table_path}")

    if not args.no_images:
        paths = write_label_images(entries, args.out_dir, args.module_px)
        width = ean13.render_symbol(entries[0].code, args.module_px).shape[1]
        print(f"{len(paths)} labels -> {args.out_dir} ({width} px wide)")


if __name__ == "__main__":
    main()
