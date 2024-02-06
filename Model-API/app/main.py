import os
import json
import pathlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel
from typing import Annotated, Optional
from app import models
from app.database import engine, SessionLocal
from app.utils.YoutubeAPI import get_video_comments, get_video_info
from app.sentimentmodel.Task import TaskPredict
from sqlalchemy import desc
from sqlalchemy.orm import Session

load_dotenv()
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

BASE_DIR = pathlib.Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "model-weight"
MODEL_METADATA = MODEL_DIR / "model-metadata.json"
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def statistics(videoId: str, db: db_dependency):
    totalComments = (
        db.query(models.Comment).filter(models.Comment.videoId == videoId).count()
    )

    totalEnjoment = (
        db.query(models.Comment)
        .filter(
            models.Comment.videoId == videoId, models.Comment.sentiment == "Enjoyment"
        )
        .count()
    )
    totalDisgust = (
        db.query(models.Comment)
        .filter(
            models.Comment.videoId == videoId, models.Comment.sentiment == "Disgust"
        )
        .count()
    )
    totalSadness = (
        db.query(models.Comment)
        .filter(
            models.Comment.videoId == videoId, models.Comment.sentiment == "Sadness"
        )
        .count()
    )
    totalAnger = (
        db.query(models.Comment)
        .filter(models.Comment.videoId == videoId, models.Comment.sentiment == "Anger")
        .count()
    )
    totalSurprise = (
        db.query(models.Comment)
        .filter(
            models.Comment.videoId == videoId, models.Comment.sentiment == "Surprise"
        )
        .count()
    )
    totalFear = (
        db.query(models.Comment)
        .filter(models.Comment.videoId == videoId, models.Comment.sentiment == "Fear")
        .count()
    )
    totalOther = (
        db.query(models.Comment)
        .filter(models.Comment.videoId == videoId, models.Comment.sentiment == "Other")
        .count()
    )
    try:
        video_info = get_video_info(videoId, YOUTUBE_API_KEY)
    except Exception as e:
        video_info = {
            "title": "Unknown",
            "totalViews": 0,
            "totalLikes": 0,
            "totalComments": 0,
        }

    video_info.update(
        {
            "totalCommentAnalyzed": totalComments,
            "totalEnjoment": totalEnjoment,
            "totalDisgust": totalDisgust,
            "totalSadness": totalSadness,
            "totalAnger": totalAnger,
            "totalSurprise": totalSurprise,
            "totalFear": totalFear,
            "totalOther": totalOther,
        }
    )
    return video_info


@app.on_event("startup")
async def on_startup():
    global T
    T = TaskPredict(MODEL_DIR / "sentiment-model.pth", MODEL_METADATA)
    await delete_old_comments()


@app.get("/")
async def root():
    return {"message": "Vietnamese Youtube Comments Sentiment"}


@app.post("/analyze")  # ?videoId=videoId
async def analyze(videoId: str, db: db_dependency):
    try:
        comments = get_video_comments(videoId, YOUTUBE_API_KEY, max_results=500)
    except Exception as e:
        return {"EC": 1, "EM": str(e), "data": {}}
    list_text = [comment["comment"] for comment in comments]
    predictions = T.predict(list_text)
    # Check if there are comments already analyzed
    threshold_time = datetime.now() - timedelta(hours=1)
    if (
        db.query(models.Comment)
        .filter(
            models.Comment.videoId == videoId,
            models.Comment.timeCreated_inDB > threshold_time,
        )
        .count()
        > 0
    ):
        return {
            "EC": 0,
            "EM": "Comments already analyzed in database",
            "data": {},
        }
    else:
        db.query(models.Comment).filter(models.Comment.videoId == videoId).delete()
    for i, comment in enumerate(comments):
        comment["sentiment"] = predictions[i]
        db_comment = models.Comment(
            id=str(comment["id"]),
            videoId=videoId,
            username=str(comment["username"]),
            comment=str(comment["comment"]),
            sentiment=str(comment["sentiment"]),
            like=int(comment["like"]),
            timeCommented=datetime.fromisoformat(comment["timeCommented"][:-1]),
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
    return {"EC": 0, "EM": "Successfully analyze video", "data": {}}


@app.get("/result")  # ?videoId=videoId&page=page&limit=limit&sortby=sortby
async def result(
    videoId: str,
    db: db_dependency,
    page: int = 1,
    limit: int = 10,
    sortby: Optional[str] = "like",
):
    if page < 1 or limit < 1:
        return {"EC": 1, "EM": "Invalid page or limit", "data": {}}
    if sortby not in ["like", "timeCommented"]:
        return {"EC": 1, "EM": "Invalid sort by", "data": {}}
    if sortby == "like":
        sortby = models.Comment.like
    else:
        sortby = models.Comment.timeCommented
    data = {}
    data["totalPages"] = (
        db.query(models.Comment).filter(models.Comment.videoId == videoId).count()
        // limit
    )
    if page > data["totalPages"]:
        return {"EC": 1, "EM": "Invalid page", "data": {}}
    info = statistics(videoId, db)
    data.update(info)
    comments = (
        db.query(models.Comment)
        .filter(models.Comment.videoId == videoId)
        .order_by(sortby.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    data["comments"] = comments
    return {"EC": 0, "EM": "Successfully get result", "data": data}


@repeat_every(hours=6)
def delete_old_comments(background_tasks=BackgroundTasks):
    db = SessionLocal()
    try:
        threshold_time = datetime.now() - timedelta(hours=1)
        db.query(models.Comment).filter(
            models.Comment.timeCreated_inDB < threshold_time
        ).delete()
        db.commit()
        print(f"{datetime.now()} - Deleted old comments")
        return {"EC": 0, "EM": "Deleted old comments", "data": {}}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
