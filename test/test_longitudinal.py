import pytest

from tesla_sim.longitudinal import LongitudinalModel

DT = 0.032   # tesla_city basicTimeStep


def run(model, target, seconds, brake=False):
    for _ in range(int(seconds / DT)):
        model.update(target, DT, brake)
    return model.speed


def test_throttle_reaches_target_with_lag():
    m = LongitudinalModel(drive_time_constant=1.0)
    assert 0.3 < run(m, 5 / 3.6, 1.0) < 1.2          # not instant
    assert run(m, 5 / 3.6, 6.0) == pytest.approx(5 / 3.6, rel=0.02)


def test_releasing_throttle_coasts_at_coast_decel():
    m = LongitudinalModel(coast_decel=0.4)
    run(m, 5 / 3.6, 10.0)
    v0 = m.speed
    assert run(m, 0.0, 1.0) == pytest.approx(v0 - 0.4, abs=0.02)   # friction only, not a stop
    assert run(m, 0.0, 10.0) == 0.0
    assert m.coast_distance(5 / 3.6) == pytest.approx((5 / 3.6) ** 2 / 0.8)


def test_lower_target_cannot_slow_faster_than_coasting():
    m = LongitudinalModel(coast_decel=0.4)
    run(m, 3.0, 10.0)
    assert run(m, 1.0, 1.0) == pytest.approx(2.6, abs=0.02)
    assert run(m, 1.0, 10.0) == pytest.approx(1.0)


def test_emergency_brake_stops_instantly_and_holds():
    m = LongitudinalModel()
    run(m, 2.0, 10.0)
    assert m.update(2.0, DT, brake=True) == 0.0
    assert run(m, 2.0, 2.0, brake=True) == 0.0


def test_direction_change_coasts_through_zero():
    m = LongitudinalModel(coast_decel=0.5)
    run(m, 1.0, 10.0)
    run(m, -1.0, 1.0)
    assert m.speed >= 0.0                              # still rolling forward, slowing
    run(m, -1.0, 6.0)
    assert m.speed < 0.0


def test_rejects_bad_parameters():
    with pytest.raises(ValueError):
        LongitudinalModel(coast_decel=0.0)
