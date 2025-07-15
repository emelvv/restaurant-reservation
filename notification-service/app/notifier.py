import os
import logging
import requests
from requests.exceptions import RequestException
from .schemas import BookingCreated

# 1) Настроим логгер
logger = logging.getLogger("notification-service.notifier")
logger.setLevel(logging.INFO)

# 2) Подтянем URL и проверим
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
if not USER_SERVICE_URL:
    raise RuntimeError("USER_SERVICE_URL is not set in environment")


def send_notification(event: BookingCreated):
    """
    Получаем контакт пользователя из User-service и логируем уведомление.
    event: экземпляр BookingCreated
    """
    try:
        resp = requests.get(
            f"{USER_SERVICE_URL}/users/{event.user_id}",
            timeout=5  # секунды
        )
        resp.raise_for_status()
    except RequestException as exc:
        logger.error("Failed to fetch user %s: %s", event.user_id, exc)
        return

    user = resp.json()
    email = user.get("email", "<no-email>")

    # 3) Логируем уведомление вместо print
    logger.info(
        "Notify %s: Your booking #%d at restaurant %d for slot %d is confirmed",
        email,
        event.booking_id,
        event.restaurant_id,
        event.slot_id
    )
