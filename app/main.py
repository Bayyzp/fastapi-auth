from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from .database import SessionLocal, engine
from . import models, schemas, crud, auth
from .config import SECRET_KEY, ALGORITHM

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_admin(username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if user is None or user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user)

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UserOut)
def read_own_profile(username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/me", response_model=schemas.UserOut)
def update_profile(updates: schemas.UserUpdate, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, username, updates)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/me")
def delete_profile(username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    success = crud.delete_user(db, username)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": "Account successfully deleted"}

@app.get("/admin/users", response_model=list[schemas.UserOut])
def get_all_users(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.delete("/admin/users/{user_id}")
def delete_user_by_id(user_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}
