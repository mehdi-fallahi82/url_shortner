from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import traceback

from app.database import Base, engine, get_db
from app.models import URLItem
from app.schemas import url_create, url_response
from app.utils import create_shortcode

Base.metadata.create_all(bind=engine)

app = FastAPI(title="سرویس کوتاه‌کننده لینک")

BASE_DOMAIN = "http://127.0.0.1:8000"


@app.post("/shorten")
def shorten_url(payload: url_create, db: Session = Depends(get_db)):

    try:
        new_url = URLItem(
            original_url=str(payload.url),
            short_code=create_shortcode()
        )
        db.add(new_url)
        db.commit()
        db.refresh(new_url)

        return new_url

    except Exception as e:
        error_msg = str(e)
        full_traceback = traceback.format_exc()
        print("--- خطا در سرور رخ داد ---")
        print(full_traceback)
        raise HTTPException(status_code=500, detail=f"Error: {error_msg}")

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

    url_record.clicks += 1
    db.commit()

    return RedirectResponse(
        url=url_record.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
