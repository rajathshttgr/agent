from agent.config.db import SessionLocal
from agent.config.models import Level
from agent.alerts import create_alert


def add_alert(message: str, level: Level = Level.critical):
    """
    Internal function.
    """
    db = SessionLocal()
    try:
        print("updating alert")
        return create_alert(db, level, message)
    finally:
        db.close()


if __name__ == "__main__":
    alert = add_alert(Level.critical, "This is a critical alert")
    print(f"Created alert: {alert.id} - {alert.level} - {alert.message}")
