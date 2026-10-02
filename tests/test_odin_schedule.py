from datetime import datetime, time

import pytest

from src.runtime.odin_schedule import (
    OdinSchedule,
    ScheduleWindow,
)


def test_schedule_window_detects_time_inside_window():
    window = ScheduleWindow(
        start=time(4, 0),
        end=time(13, 0),
    )

    assert window.contains(time(8, 0))
    assert window.contains(time(4, 0))
    assert window.contains(time(13, 0))


def test_schedule_window_rejects_time_outside_window():
    window = ScheduleWindow(
        start=time(4, 0),
        end=time(13, 0),
    )

    assert not window.contains(time(3, 59))
    assert not window.contains(time(13, 1))


def test_schedule_supports_multiple_windows():
    schedule = OdinSchedule(
        bot_id="worker_1"
    )

    schedule.set_windows(
        weekday=0,
        windows=[
            ScheduleWindow(
                start=time(4, 0),
                end=time(13, 0),
            ),
            ScheduleWindow(
                start=time(14, 0),
                end=time(22, 10),
            ),
        ],
    )

    morning = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    pause = datetime(
        2026,
        9,
        28,
        13,
        30,
    )

    evening = datetime(
        2026,
        9,
        28,
        18,
        0,
    )

    assert schedule.is_active(morning)
    assert not schedule.is_active(pause)
    assert schedule.is_active(evening)


def test_weekday_schedule_creates_pause():
    schedule = OdinSchedule(
        bot_id="worker_1"
    )

    schedule.set_weekday_schedule()

    before_pause = datetime(
        2026,
        9,
        28,
        12,
        59,
    )

    during_pause = datetime(
        2026,
        9,
        28,
        13,
        30,
    )

    after_pause = datetime(
        2026,
        9,
        28,
        14,
        1,
    )

    assert schedule.is_active(before_pause)
    assert not schedule.is_active(during_pause)
    assert schedule.is_active(after_pause)


def test_weekend_schedule_ends_at_20():
    schedule = OdinSchedule(
        bot_id="worker_1"
    )

    schedule.set_weekend_schedule()

    saturday_before_end = datetime(
        2026,
        9,
        26,
        19,
        59,
    )

    saturday_after_end = datetime(
        2026,
        9,
        26,
        20,
        1,
    )

    assert schedule.is_active(
        saturday_before_end
    )

    assert not schedule.is_active(
        saturday_after_end
    )


def test_schedule_can_be_disabled():
    schedule = OdinSchedule(
        bot_id="worker_1"
    )

    schedule.set_weekday_schedule()
    schedule.disable()

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    assert not schedule.is_active(current)


def test_schedule_can_be_enabled_again():
    schedule = OdinSchedule(
        bot_id="worker_1"
    )

    schedule.set_weekday_schedule()
    schedule.disable()
    schedule.enable()

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    assert schedule.is_active(current)


def test_invalid_bot_id_is_rejected():
    with pytest.raises(ValueError):
        OdinSchedule(bot_id="")


def test_invalid_weekday_is_rejected():
    schedule = OdinSchedule(
        bot_id="worker_1"
    )

    with pytest.raises(ValueError):
        schedule.set_windows(
            weekday=7,
            windows=[
                ScheduleWindow(
                    start=time(4, 0),
                    end=time(10, 0),
                )
            ],
        )


def test_invalid_pause_configuration_is_rejected():
    schedule = OdinSchedule(
        bot_id="worker_1"
    )

    with pytest.raises(ValueError):
        schedule.set_weekday_schedule(
            start=time(4, 0),
            end=time(22, 10),
            pause_start=time(14, 0),
            pause_end=time(13, 0),
  )
