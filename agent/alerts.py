from sqlalchemy.orm import Session
from typing import List, Optional

from agent.config.models import AlertEntry, Level


def create_alert(db: Session, level: Level, message: str) -> AlertEntry:
    alert = AlertEntry(level=level, message=message)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_alert(db: Session, alert_id: int) -> Optional[AlertEntry]:
    return db.query(AlertEntry).filter(AlertEntry.id == alert_id).first()


def get_alerts(
    db: Session, limit: int = 10, severity: Optional[Level] = None
) -> List[AlertEntry]:

    query = db.query(AlertEntry)

    if severity:
        query = query.filter(AlertEntry.level == severity)

    return query.order_by(AlertEntry.timestamp.desc()).limit(limit).all()
