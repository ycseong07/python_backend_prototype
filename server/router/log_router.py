from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.database.database import get_db
from server.models.log_models import UserLog
from server.schemas.log_schemas import UserAction

router = APIRouter()

@router.post("/user-action/")
async def log_user_action(action: UserAction, db: Session = Depends(get_db)): 
    new_log = UserLog(user_id=action.user_id, action_type=action.action_type)
    db.add(new_log)
    db.commit()
    return {"유저 행동 로그 기록 성공"}