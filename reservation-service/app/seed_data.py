# reservation-service/seed_data.py

from models import Base, engine, SessionLocal, Restaurant, Slot
from datetime import datetime, date, time, timedelta

def seed():
    db = SessionLocal()
    try:
        # 1) Создаём таблицы, если их нет
        Base.metadata.create_all(bind=engine)

        # 2) Проверяем — если ресторанов ещё нет, добавляем пример
        if db.query(Restaurant).count() == 0:
            r1 = Restaurant(name="Italiano Delight")
            r2 = Restaurant(name="Sushi World")
            db.add_all([r1, r2])
            db.commit()

            # 3) Для каждого ресторана создаём слоты на ближайшие 3 дня
            restaurants = db.query(Restaurant).all()
            for rest in restaurants:
                for d in range(3):
                    day = date.today() + timedelta(days=d)
                    # завтрак, обед, ужин
                    for hour in (9, 13, 19):
                        start = datetime.combine(day, time(hour, 0))
                        end   = start + timedelta(hours=2)
                        slot = Slot(
                            restaurant_id=rest.id,
                            start_time=start,
                            end_time=end,
                            is_available=True
                        )
                        db.add(slot)
            db.commit()
            print("Seed completed: added restaurants and slots.")
        else:
            print("Seed skipped: restaurants already exist.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
