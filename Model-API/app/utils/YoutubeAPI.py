from googleapiclient.discovery import build
from app.utils.Preprocess import remove_HTML_URL
import html
from ftlangdetect import detect
import pandas as pd
import regex as re


def comment_preprocess(comment):
    comment = html.unescape(remove_HTML_URL(comment))
    comment = re.sub(r"\s+", " ", comment).strip()  # Remove spacing > 1
    return comment


def get_video_comments(video_id, api_key, max_results=100):
    comments_list = []
    # creating youtube resource object
    youtube = build("youtube", "v3", developerKey=api_key)
    # retrieve youtube video results
    video_response = (
        youtube.commentThreads().list(part="snippet", videoId=video_id).execute()
    )

    while video_response:
        for item in video_response["items"]:
            cmt_id = item["id"]
            comment = comment_preprocess(
                item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            )
            detected_lang = detect(text=comment, low_memory=True)["lang"]
            if detected_lang != "vi":
                continue
            author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            likeCount = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            timeCommented = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            comments_list.append(
                {
                    "id": cmt_id,
                    "username": author,
                    "comment": comment,
                    "like": likeCount,
                    "timeCommented": timeCommented,
                }
            )
            if len(comments_list) >= max_results:
                return comments_list

        # Again repeat
        if "nextPageToken" in video_response:
            video_response = (
                youtube.commentThreads()
                .list(
                    part="snippet",
                    videoId=video_id,
                    pageToken=video_response["nextPageToken"],
                )
                .execute()
            )
        else:
            break
    return comments_list


def get_video_info(video_id, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    video_response = (
        youtube.videos().list(part="snippet,statistics", id=video_id).execute()
    )
    video_info = video_response["items"][0]
    return {
        "title": video_info["snippet"]["title"],
        "totalViews": video_info["statistics"]["viewCount"],
        "totalLikes": video_info["statistics"]["likeCount"],
        "totalComments": video_info["statistics"]["commentCount"],
    }
