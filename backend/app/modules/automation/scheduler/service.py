from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from croniter import CroniterBadCronError, croniter
from fastapi import HTTPException


def next_schedule_run(
    expression: str,
    timezone_name: str = "UTC",
    base: datetime | None = None,
) -> datetime:
    try:
        zone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise HTTPException(status_code=422, detail="Unknown schedule timezone") from exc
    reference = (base or datetime.now(timezone.utc)).astimezone(zone)
    try:
        return croniter(expression, reference).get_next(datetime)
    except (CroniterBadCronError, ValueError) as exc:
        raise HTTPException(status_code=422, detail="Invalid cron schedule expression") from exc
