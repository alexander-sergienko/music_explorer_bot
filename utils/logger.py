import os
from datetime import datetime

def log_message(user_id: int, message: str, sender: str):
    os.makedirs("logs", exist_ok=True)
    filename = f"logs/{user_id}.log"
    now = datetime.now().strftime("[%d.%m.%Y %H:%M]")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{now} {sender}: {message}\n")
