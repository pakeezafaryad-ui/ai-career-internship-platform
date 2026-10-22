
import re

from pwdlib import PasswordHash
from services.database import SessionLocal, User


password_hash = PasswordHash.recommended()


def register_user(email, password):
    """Create a user account with a securely hashed password."""

    email = (email or "").strip().lower()
    password = password or ""

    # Validate email format
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        return False, "Please enter a valid email address."

    # Require a strong password
    if len(password) < 12:
        return False, "Password must contain at least 12 characters."

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            return False, "An account with this email already exists."

        hashed_password = password_hash.hash(password)

        new_user = User(
            email=email,
            password_hash=hashed_password,
        )

        db.add(new_user)
        db.commit()

        return True, "Account created successfully. You can now log in."

    except Exception:
        db.rollback()
        return False, "Account creation failed. Please try again."

    finally:
        db.close()


def authenticate_user(email, password):
    """Verify credentials and return basic user information."""

    email = (email or "").strip().lower()
    password = password or ""

    if not email or not password:
        return None

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user is None:
            return None

        if not password_hash.verify(password, user.password_hash):
            return None

        return {
            "id": user.id,
            "email": user.email,
        }

    except Exception:
        return None

    finally:
        db.close()
