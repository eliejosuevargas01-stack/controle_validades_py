from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import UserDB

from app.core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido"
        )
    user_id = payload.get("sub")
    user = db.query(UserDB).filter(UserDB.id == int (user_id)).first()

    if user is None: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user