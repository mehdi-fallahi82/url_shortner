from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.auth import verify_password, crate_access_token, hash_password
from app.database import Base, engine, get_db
from app.models import URLItem, User
from app.schemas import url_create, url_response, user_create_account, user_response, token
from app.utils import create_shortcode

Base.metadata.create_all(bind=engine)
app = FastAPI(title="سرویس کوتاه‌کننده لینک")
BASE_DOMAIN = "http://127.0.0.1:8080"


@app.post("/register", response_model=user_response, status_code=status.HTTP_201_CREATED)
def create_user(User_data: user_create_account, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == User_data.email).first()

    if existing_user: raise HTTPException(status_code=400, detail="already exists")

    hashed_pwd = hash_password(User_data.password)

    new_user = User(username=User_data.username, email=User_data.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز اشتباه است .",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = crate_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post("/shorten")
def shorten_url(payload: url_create, db: Session = Depends(get_db)):
    if payload.custom_code:
        chose_code = payload.custom_code
        if len(chose_code) < 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="کد دلخواه باید حداقل 4 کاراگتر باشد ."
            )
        exists = db.query(URLItem).filter(URLItem.short_code == chose_code).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این کد کوتاه قبلاً رزرو شده است لطفاً کد دیگری انتخاب کنید."
            )

    else:
        chose_code = create_shortcode(length=6)
        exists = db.query(URLItem).filter(URLItem.short_code == chose_code).first()
        if exists:
            raise HTTPException()


    new_url = URLItem(
    original_url=str(payload.original_url),
    short_code=chose_code
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return  {
        "original_url": new_url.original_url,
        "short_code": new_url.short_code,
        "short_url": f"{BASE_DOMAIN}/{new_url.short_code}"
    }

@app.get("/stats/{short_code}", response_model=url_response)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    url_record = db.query(URLItem).filter(URLItem.short_code == short_code).first()

    if not url_record:
        raise HTTPException(status_code=404, detail="لینک مورد نظر یافت نشد!")

    return url_response(
        id=url_record.id,
        original_url=url_record.original_url,
        short_code=url_record.short_code,
        short_url=f"{BASE_DOMAIN}/{url_record.short_code}",
        clicks=url_record.clicks,
        created_at=url_record.created_at,
    )


@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    url_record = db.query(URLItem).filter(URLItem.short_code == short_code).first()

    if not url_record:
        raise HTTPException(status_code=404, detail="لینک مورد نظر یافت نشد!")

    if url_record.created_at:
        now = datetime.now(timezone.utc)
        record_time = url_record.created_at

        if record_time.tzinfo is None:
            record_time = record_time.replace(tzinfo=timezone.utc)

        if now - record_time > timedelta(days=1):
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="لینک مورد نظر نظر منقضی شده است ."
            )

    url_record.clicks += 1
    db.commit()

    return RedirectResponse(
        url=url_record.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
