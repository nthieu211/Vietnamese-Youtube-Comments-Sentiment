from preprocess import text_preprocess, remove_HTML, convert_unicode
import pandas as pd
import json
import plotly.graph_objects as go

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

from googleapiclient.discovery import build
from flask import Flask, render_template, request, redirect, url_for


# Config
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
PRETRAINED_MODEL = "vinai/phobert-base-v2"
MAX_LEN = 120
API_KEY = "AIzaSyC-klgvTp1PFc7XMAJKypphlJnOqAIUJn4"

# Download PhoBERT model
phobert = AutoModel.from_pretrained(PRETRAINED_MODEL)
tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL)


class SentimentClassifier(nn.Module):
    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = phobert
        self.drop = nn.Dropout(p=0.4)
        self.fc = nn.Linear(self.bert.config.hidden_size, n_classes)
        nn.init.normal_(self.fc.weight, std=0.02)
        nn.init.normal_(self.fc.bias, 0)

    def forward(self, input_ids, attention_mask):
        last_hidden_state, output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False,  # Dropout will errors if without this
        )

        x = self.drop(output)
        x = self.fc(x)
        return x


# Load model from file save
model = torch.load(f"Model\\weights.pt")

class_names = ["Enjoyment", "Disgust", "Sadness", "Anger", "Surprise", "Fear", "Other"]


def infer(text, tokenizer, max_len=MAX_LEN):
    clean_text = text_preprocess(text)
    encoded_review = tokenizer.encode_plus(
        clean_text,
        max_length=max_len,
        truncation=True,
        add_special_tokens=True,
        padding="max_length",
        return_attention_mask=True,
        return_token_type_ids=False,
        return_tensors="pt",
    )

    input_ids = encoded_review["input_ids"].to(device)
    attention_mask = encoded_review["attention_mask"].to(device)

    output = model(input_ids, attention_mask)
    _, y_pred = torch.max(output, dim=1)

    return class_names[y_pred]


# Get video comments from Youtube and infer, then store in Dataframe
def get_video_comments(video_id, api_key):
    comments_list = []
    # creating youtube resource object
    youtube = build("youtube", "v3", developerKey=api_key)
    # retrieve youtube video results
    video_response = (
        youtube.commentThreads().list(part="snippet", videoId=video_id).execute()
    )

    # iterate video response
    while video_response:
        # extracting required info
        # from each result object
        for item in video_response["items"]:
            # Extracting comments
            comment = convert_unicode(
                remove_HTML(
                    item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                )
            )
            author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            # Infer
            emotion = infer(comment, tokenizer)
            # Append comment and author as a dictionary to the list
            comments_list.append(
                {"Author": author, "Comment": comment, "Emotion": emotion}
            )

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

    return pd.DataFrame(comments_list)


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    VIDEO_ID = request.form["video_id"]
    comments_df = get_video_comments(VIDEO_ID, API_KEY)

    emotions = ["Enjoyment", "Disgust", "Sadness", "Anger", "Surprise", "Fear", "Other"]
    emotion_counts = comments_df["Emotion"].value_counts()
    # Create a bar chart using Plotly
    fig = go.Figure(data=go.Bar(x=emotions, y=emotion_counts))
    # Convert the Plotly figure to HTML
    chart_html = fig.to_html(full_html=False)

    return render_template(
        "analyze.html", dataframe=comments_df.to_html(index=False), chart=chart_html
    )


if __name__ == "__main__":
    app.run()
