"""Tests for the sample registry and the lookup table it writes."""

import json
from pathlib import Path

import pytest

from labvision import ean13, registry


def test_default_catalogue_has_the_expected_size_and_ids() -> None:
    samples = registry.default_samples()
    assert len(samples) == registry.DEFAULT_SAMPLE_COUNT == 200
    assert samples[0].sample_id == "SMP-0001"
    assert samples[99].sample_id == "SMP-0100"
    assert samples[100].sample_id == "PWD-0001"
    assert samples[-1].sample_id == "PWD-0100"
    assert len({s.sample_id for s in samples}) == 200


def test_default_catalogue_is_reproducible() -> None:
    assert registry.default_samples() == registry.default_samples()


@pytest.mark.parametrize("spec", registry.PHASES, ids=lambda s: s.name)
def test_each_phase_is_the_full_cross_product(spec: registry.PhaseSpec) -> None:
    """Every compound must appear in every container size for its phase."""
    samples = [s for s in registry.default_samples() if s.phase == spec.name]
    materials = {name for name, _ in spec.materials}
    volumes = set(spec.containers_ml)

    assert {s.material for s in samples} == materials
    assert {s.container_ml for s in samples} == volumes
    assert len(samples) == spec.size == len(materials) * len(volumes)

    pairs = [(s.material, s.container_ml) for s in samples]
    assert len(set(pairs)) == len(pairs)
    assert set(pairs) == {(m, v) for m in materials for v in volumes}


@pytest.mark.parametrize("spec", registry.PHASES, ids=lambda s: s.name)
def test_compound_is_not_correlated_with_container_size(
    spec: registry.PhaseSpec,
) -> None:
    """Guards the bug the cross product exists to avoid.

    Cycling 20 materials against 5 sizes in step locks each compound to one
    size, which would let a model infer the compound from container size alone.
    """
    samples = registry.default_samples()
    for material, _ in spec.materials:
        sizes = {s.container_ml for s in samples if s.material == material}
        assert sizes == set(spec.containers_ml), material


def test_no_compound_appears_in_both_phases() -> None:
    """A material is either a liquid or a solid; it cannot be catalogued as both."""
    liquids = {name for name, _ in registry.LIQUID_MATERIALS}
    powders = {name for name, _ in registry.POWDER_MATERIALS}
    assert liquids & powders == set()


def test_cas_numbers_are_unique_across_the_catalogue() -> None:
    pairs = registry.LIQUID_MATERIALS + registry.POWDER_MATERIALS
    cas = [c for _, c in pairs]
    assert len(set(cas)) == len(cas)


def test_both_phases_share_one_container_series() -> None:
    """Container size must not give the phase away.

    If powders lived in their own labware, a detector could read "powder" off
    the vessel shape and never decode the barcode -- the same shortcut the
    cross product exists to close.
    """
    samples = registry.default_samples()
    by_phase = {
        phase: {s.container_ml for s in samples if s.phase == phase}
        for phase in {s.phase for s in samples}
    }
    assert len(by_phase) == 2
    assert len(set(map(frozenset, by_phase.values()))) == 1
    assert {s.vessel_class for s in samples} == {
        f"flask_{v:g}ml" for v in registry.FLASK_VOLUMES_ML
    }


def test_there_are_only_five_vessel_classes() -> None:
    classes = {s.vessel_class for s in registry.default_samples()}
    assert len(classes) == 5
    assert all(c.startswith("flask_") for c in classes)


def test_vessel_class_does_not_encode_phase() -> None:
    liquid = registry.Sample("SMP-1", "Limonene", "5989-27-5", "liquid", 50.0, "L1")
    powder = registry.Sample("PWD-1", "Vanillin", "121-33-5", "powder", 50.0, "L1")
    assert liquid.vessel_class == powder.vessel_class == "flask_50ml"


def test_vessel_class_rejects_an_unknown_phase() -> None:
    bad = registry.Sample("X-1", "M", "C", "plasma", 10.0, "L1")
    with pytest.raises(registry.RegistryError, match="unknown phase"):
        _ = bad.vessel_class


def test_default_samples_rejects_a_count_beyond_the_catalogue() -> None:
    with pytest.raises(ValueError, match="must be <="):
        registry.default_samples(registry.DEFAULT_SAMPLE_COUNT + 1)


def test_partial_count_stops_inside_the_liquid_phase() -> None:
    samples = registry.default_samples(7)
    assert len(samples) == 7
    assert {s.phase for s in samples} == {"liquid"}


def test_default_samples_rejects_a_non_positive_count() -> None:
    with pytest.raises(ValueError):
        registry.default_samples(0)


def test_payload_is_stable_and_field_ordered() -> None:
    sample = registry.Sample(
        "SMP-0001", "Limonene", "5989-27-5", "liquid", 50.0, "LOT-1234",
    )
    assert sample.payload() == "SMP-0001|Limonene|5989-27-5|liquid|50|LOT-1234"


def test_payload_change_changes_the_code() -> None:
    """The barcode is derived from the record, so a differing record differs."""
    a = registry.Sample("SMP-0001", "Limonene", "5989-27-5", "liquid", 50.0, "L1")
    b = registry.Sample("SMP-0001", "Limonene", "5989-27-5", "liquid", 100.0, "L1")
    assert registry.sha256_of(a) != registry.sha256_of(b)


def test_sha256_is_deterministic_and_salt_sensitive() -> None:
    sample = registry.default_samples(1)[0]
    assert registry.sha256_of(sample) == registry.sha256_of(sample)
    assert registry.sha256_of(sample) != registry.sha256_of(sample, salt=1)
    assert len(registry.sha256_of(sample)) == 64


def test_code_from_digest_is_a_valid_prefixed_ean13() -> None:
    code = registry.code_from_digest("00" * 32)
    assert code == "2000000000008"
    assert ean13.is_valid(code)
    assert code.startswith(registry.INTERNAL_PREFIX)


def test_code_from_digest_rejects_non_hex() -> None:
    with pytest.raises(registry.RegistryError):
        registry.code_from_digest("not-a-digest")


def test_every_code_in_the_catalogue_is_valid_and_unique() -> None:
    entries = registry.build_registry(registry.default_samples())
    assert len(entries) == 200
    codes = [e.code for e in entries]
    assert len(set(codes)) == 200
    assert all(ean13.is_valid(c) for c in codes)
    assert all(c.startswith(registry.INTERNAL_PREFIX) for c in codes)


def test_registry_is_reproducible() -> None:
    a = registry.build_registry(registry.default_samples())
    b = registry.build_registry(registry.default_samples())
    assert [e.code for e in a] == [e.code for e in b]


def test_registry_preserves_input_order() -> None:
    samples = registry.default_samples(10)
    entries = registry.build_registry(samples)
    assert [e.sample for e in entries] == samples


def test_registry_rejects_duplicate_sample_ids() -> None:
    sample = registry.default_samples(1)[0]
    with pytest.raises(registry.RegistryError, match="duplicate sample_id"):
        registry.build_registry([sample, sample])


def test_collisions_are_resolved_by_salting(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force every unsalted hash onto one code and check the salt breaks the tie."""
    real = registry.code_from_digest
    calls = {"n": 0}

    def fold(digest: str) -> str:
        calls["n"] += 1
        # First two samples both want the same code; later attempts fall through
        # to the real fold, which the salted re-hash will reach.
        return "2000000000008" if calls["n"] <= 2 else real(digest)

    monkeypatch.setattr(registry, "code_from_digest", fold)
    entries = registry.build_registry(registry.default_samples(2))
    assert entries[0].code == "2000000000008"
    assert entries[0].salt == 0
    assert entries[1].code != entries[0].code
    assert entries[1].salt == 1
    assert registry.sha256_of(entries[1].sample, 1) == entries[1].sha256


def test_table_roundtrips_through_disk(tmp_path: Path) -> None:
    entries = registry.build_registry(registry.default_samples())
    path = registry.save_table(entries, tmp_path / "lookup_table.json")
    loaded = registry.load_table(path)

    assert len(loaded) == 200
    for entry in entries:
        record = loaded[entry.code]
        assert record["sample_id"] == entry.sample.sample_id
        assert record["material"] == entry.sample.material
        assert record["vessel_class"] == entry.sample.vessel_class
        assert record["sha256"] == entry.sha256


def test_saved_table_carries_its_schema(tmp_path: Path) -> None:
    entries = registry.build_registry(registry.default_samples(3))
    path = registry.save_table(entries, tmp_path / "t.json")
    table = json.loads(path.read_text(encoding="utf-8"))
    assert table["version"] == registry.REGISTRY_VERSION
    assert table["symbology"] == "EAN-13"
    assert table["count"] == 3
    assert "sha256" in table["id_scheme"]


def test_load_table_reports_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(registry.RegistryError, match="not found"):
        registry.load_table(tmp_path / "absent.json")


def test_load_table_rejects_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(registry.RegistryError, match="not valid JSON"):
        registry.load_table(path)


def test_load_table_rejects_a_future_schema_version(tmp_path: Path) -> None:
    path = tmp_path / "future.json"
    path.write_text(json.dumps({"version": 999, "entries": {}}), encoding="utf-8")
    with pytest.raises(registry.RegistryError, match="version"):
        registry.load_table(path)


def test_write_label_images_writes_one_png_per_entry(tmp_path: Path) -> None:
    entries = registry.build_registry(registry.default_samples(5))
    paths = registry.write_label_images(entries, tmp_path)
    assert len(paths) == 5
    assert all(p.exists() and p.stat().st_size > 0 for p in paths)
    for entry, path in zip(entries, paths, strict=True):
        assert entry.code in path.name
        assert entry.sample.sample_id in path.name
