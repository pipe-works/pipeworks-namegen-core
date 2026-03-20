from pipeworks_namegen_core import healthcheck


def test_healthcheck_returns_ok() -> None:
    assert healthcheck() == "ok"
