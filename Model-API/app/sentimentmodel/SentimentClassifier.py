import torch
import torch.nn as nn
from transformers import AutoConfig, AutoModel


# Define model
class SentimentClassifier(nn.Module):
    def __init__(self, config):
        super(SentimentClassifier, self).__init__()
        phobert_config = AutoConfig.from_pretrained(config["PRETRAINED_NAME"])
        self.basemodel = AutoModel.from_config(phobert_config)
        self.drop1 = nn.Dropout(p=config["DROPOUT"])
        self.fc1 = nn.Linear(self.basemodel.config.hidden_size, config["LINEAR_SIZE"])
        self.drop2 = nn.Dropout(p=config["DROPOUT"])
        self.fc2 = nn.Linear(config["LINEAR_SIZE"], config["NUM_CLASSES"])

    def forward(self, input_ids, attention_mask):
        last_hidden_state, output = self.basemodel(
            input_ids=input_ids, attention_mask=attention_mask, return_dict=False
        )
        x = self.drop1(output)
        x = self.fc1(x)
        x = self.drop2(x)
        x = self.fc2(x)
        return x
