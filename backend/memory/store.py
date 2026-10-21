"""Persist profiles in the existing memory table; no extra model calls."""

from sqlalchemy import delete, select

from backend.database import SessionLocal
from backend.database.models import Memory, User
from backend.memory.models import UserProfile
from backend.repositories.conversation import conversation_repository


class MemoryStore:
    def exists(self, user_id):
        with SessionLocal() as db:
            return db.scalar(select(User.id).where(User.external_id == user_id)) is not None

    def get(self, user_id):
        with SessionLocal() as db:
            rows = db.scalars(
                select(Memory).join(User).where(User.external_id == user_id, Memory.is_active.is_(True))
            )
            fields = {
                m.key: m.value.get("value") for m in rows if isinstance(m.value, dict) and "value" in m.value
            }
            return UserProfile.model_validate(
                {k: v for k, v in fields.items() if k in UserProfile.model_fields}
            )

    def save(self, user_id, profile):
        values = profile.model_dump(exclude_none=True)
        if not values:
            return
        with SessionLocal() as db:
            user = conversation_repository.get_or_create_user(db, user_id)
            for key, value in values.items():
                row = db.scalar(select(Memory).where(Memory.user_id == user.id, Memory.key == key))
                if row:
                    row.value, row.is_active = {"value": value}, True
                else:
                    db.add(Memory(user_id=user.id, key=key, value={"value": value}, category="profile"))
            db.commit()

    def delete(self, user_id):
        with SessionLocal() as db:
            user = db.scalar(select(User).where(User.external_id == user_id))
            if user:
                db.execute(delete(Memory).where(Memory.user_id == user.id))
                db.commit()

    def clear(self):
        with SessionLocal() as db:
            db.execute(delete(Memory))
            db.commit()


memory_store = MemoryStore()
