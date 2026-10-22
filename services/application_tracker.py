
from services.database import SessionLocal, Application


VALID_STATUSES = {
    "Interested",
    "Applied",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
}


def add_application(user_id, company, role, status="Applied"):
    """Save a job or internship application for a user."""

    company = (company or "").strip()
    role = (role or "").strip()
    status = (status or "").strip()

    if not company or not role:
        return False, "Please enter both company and role."

    if status not in VALID_STATUSES:
        return False, "Please select a valid application status."

    db = SessionLocal()

    try:
        application = Application(
            user_id=user_id,
            company=company,
            role=role,
            status=status,
        )

        db.add(application)
        db.commit()

        return True, "Application saved successfully."

    except Exception:
        db.rollback()
        return False, "Could not save the application. Please try again."

    finally:
        db.close()


def get_user_applications(user_id):
    """Return applications belonging only to the specified user."""

    db = SessionLocal()

    try:
        records = (
            db.query(Application)
            .filter(Application.user_id == user_id)
            .order_by(Application.id.desc())
            .all()
        )

        return [
            {
                "id": record.id,
                "company": record.company,
                "role": record.role,
                "status": record.status,
            }
            for record in records
        ]

    finally:
        db.close()


def update_application_status(user_id, application_id, status):
    """Update an application only if it belongs to the current user."""

    if status not in VALID_STATUSES:
        return False, "Please select a valid application status."

    db = SessionLocal()

    try:
        application = (
            db.query(Application)
            .filter(
                Application.id == application_id,
                Application.user_id == user_id,
            )
            .first()
        )

        if application is None:
            return False, "Application not found."

        application.status = status
        db.commit()

        return True, "Application status updated successfully."

    except Exception:
        db.rollback()
        return False, "Could not update the application. Please try again."

    finally:
        db.close()
