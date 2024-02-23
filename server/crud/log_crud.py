from sqlalchemy.orm import Session
from server.models.log_models import Auth
from server.schemas.log_schemas import AuthCreate
from datetime import datetime

# 유저 인증 로그 생성
def create_user(db: Session, user: AuthCreate):
    db_user = Auth(user_id=user.user_id, email=user.email, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user