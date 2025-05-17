# from sqlalchemy.orm import Session
# from app.models import User, Role
# from typing import Optional
#
#
# class AuthService:
#     def __init__(self, db_session: Session):
#         self.db = db_session
#
#     def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
#         return self.db.query(User).filter(User.telegram_id == telegram_id).first()
#
#     def create_user(self, telegram_id: int, username: str, full_name: str, role_name: str = "visitor") -> User:
#         role = self.db.query(Role).filter(Role.name == role_name).first()
#         if not role:
#             raise ValueError(f"Role '{role_name}' not found")
#
#         user = User(
#             telegram_id=telegram_id,
#             username=username,
#             full_name=full_name,
#             role_id=role.id
#         )
#         self.db.add(user)
#         self.db.commit()
#         return user
#
#     def is_admin(self, user: User) -> bool:
#         return user.role.name == "admin"
#
#     def is_curator(self, user: User) -> bool:
#         return user.role.name == "curator"