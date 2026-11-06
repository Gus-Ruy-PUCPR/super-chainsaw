from ics import Calendar, Event
from loguru import logger
from pathlib import Path
from database import read
from datetime import datetime
import arrow

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "data/calendar.ics"
TAG = "CALENDAR_GEN:"

# cria o objeto Calendar() e preenche com os Event()
def set_events():
    calendar = Calendar()
    for item in read():
        try:
            event = Event()
            event.name = item["activity_name"]
            event.description = item["course_name"]
            event.begin = datetime.strptime(item["date"], "%d/%m/%Y %H:%M")
            event.make_all_day()
            event.created = arrow.utcnow()
            calendar.events.add(event)
        except Exception as e:
            logger.error(f"{TAG} Could not create event: {e}")
    return calendar

# cria o arquivo com o retorno de set_events(), que é um objeto da classe Calendar()
def create_ics(c):
    with open(FILE_PATH, 'w', encoding="utf-8", newline='') as f:  # newlin
        f.writelines(c.serialize_iter())