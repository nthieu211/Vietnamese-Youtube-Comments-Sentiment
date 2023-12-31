from preprocess import text_preprocess, remove_HTML, convert_unicode
import pandas as pd
import plotly.express as px

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import gdown
from googleapiclient.discovery import build
from flask import Flask, render_template, request, redirect, url_for


# Config
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
PRETRAINED_MODEL = "vinai/phobert-base-v2"
MAX_LEN = 120
API_KEY = ""

# Download PhoBERT model
phobert = AutoModel.from_pretrained(PRETRAINED_MODEL)
tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL)
# Download weights.pt
gdown.download(id="1amzwt-ApWbScxi-85fyGVohsdYaWea-C", output="app/weights.pt")


# Define Sentiment Classifier and load Save Model
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
model = torch.load("app/weights.pt", map_location=device)

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


def get_video_info(video_id, api_key):
    """
    Get video information including title.

    Args:
        video_id (str): The ID of the YouTube video.
        api_key (str): The API key for the YouTube API.

    Returns:
        dict: A dictionary containing video information, including title.
    """
    try:
        # creating youtube resource object
        youtube = build("youtube", "v3", developerKey=api_key)
        # retrieve YouTube video results
        video_response = youtube.videos().list(part="snippet", id=video_id).execute()

        # Extract video title
        video_title = video_response["items"][0]["snippet"]["title"]

        return video_title

    except:
        print("Error getting video information")


def get_video_comments(video_id, api_key):
    """
    Get the comments from a YouTube video and infer the emotion of each comment.

    Args:
        video_id (str): The ID of the YouTube video.
        api_key (str): The API key for the YouTube API.

    Returns:
        pd.DataFrame: A DataFrame containing the comments and their inferred emotions.
    """
    try:
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
                author = item["snippet"]["topLevelComment"]["snippet"][
                    "authorDisplayName"
                ]

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

    except:
        print("Error getting video comments")


app = Flask(__name__)


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="icon.svg"), code=302)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    VIDEO_ID = request.form["video_id"]

    title = get_video_info(VIDEO_ID, API_KEY)
    title_href = f"<a href='https://www.youtube.com/watch?v={VIDEO_ID}' target='_blank'><h3>{title}</h3></a>"

    comments_df = get_video_comments(VIDEO_ID, API_KEY)

    emotion_counts = comments_df["Emotion"].value_counts()
    all_counts = pd.Series(0, index=class_names)
    all_counts.update(emotion_counts)

    # Create a bar chart using Plotly
    fig = px.bar(
        x=class_names,
        y=all_counts,
        color=class_names,
        labels={"x": "Emotion", "y": "Number of Comments", "color": "Emotion"},
        text=all_counts,
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Emotion: %{x}",
                "Quantity: %{y}",
            ]
        )
    )
    # Convert the Plotly figure to HTML
    chart_html = fig.to_html(full_html=False).replace(
        "<div>", '<div class="col-6" style="height: 320px">'
    )
    return render_template(
        "analyze.html",
        video_title=title_href,
        total_comments=len(comments_df),
        dataframe=comments_df.to_html(index=False, escape=False)
        .replace(
            '<table border="1" class="dataframe">',
            '<table class="table table-fixed" style="table-layout: fixed; width: 100%;">',
        )
        .replace('<tr style="text-align: right;">', '<tr style="text-align: left;">')
        .replace("<thead>", '<thead style="background-color: #ff0000;">')
        .replace("<th>Author", '<th scope="col" style="width: 15%">Author')
        .replace("<th>Comment", '<th scope="col" style="width: 70%">Comment')
        .replace("<th>Emotion", '<th scope="col" style="width: 15%">Emotion'),
        chart=chart_html,
    )


if __name__ == "__main__":
    from waitress import serve
    import os

    port = os.environ.get("PORT", 80)
    serve(app, host="0.0.0.0", port=port)
