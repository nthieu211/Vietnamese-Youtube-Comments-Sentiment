import os
import json
from pathlib import Path
from app.sentimentmodel.SentimentClassifier import *
from app.sentimentmodel.SentimentDataset import *


class TaskPredict:
    def __init__(self, model_path, metadata_path):
        self.model_path = model_path
        self.metadata_path = metadata_path
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError(f"Metadata file not found at {metadata_path}")
        self.device = torch.device("cpu")
        # Load metadata
        with open(self.metadata_path) as json_file:
            self.config = json.load(json_file)
        self.model = SentimentClassifier(self.config["MODEL"])
        self.model.load_state_dict(
            torch.load(self.model_path, map_location=self.device)
        )
        self.model.to(self.device)
        self.model.eval()

    def predict(self, list_text):
        # Preprocess input
        dataset = SentimentDataset(list_text, self.config)
        dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

        # Predict
        predictions = []
        for data in dataloader:
            input_ids = data["input_ids"].to(self.device)
            attention_mask = data["attention_mask"].to(self.device)
            with torch.no_grad():
                output = self.model(input_ids, attention_mask)
                _, pred = torch.max(output, 1)
                predictions.append(self.config["id2label"][str(pred.item())])

        return predictions
