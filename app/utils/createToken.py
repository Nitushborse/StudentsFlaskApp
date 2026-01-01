import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def create_tokens(staff_id):
    access_token = jwt.encode(
        {
            "id": staff_id,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    refresh_token = jwt.encode(
        {
            "id": staff_id,
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return access_token, refresh_token
