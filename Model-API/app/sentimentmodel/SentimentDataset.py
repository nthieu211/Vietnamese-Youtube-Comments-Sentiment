from transformers import AutoTokenizer
from torch.utils.data import Dataset, DataLoader
from app.utils.Preprocess import text_preprocess


# Define dataset:
class SentimentDataset(Dataset):
    def __init__(self, list_text, config):
        self.list_text = list_text
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(
            config["MODEL"]["PRETRAINED_NAME"]
        )

    def __len__(self):
        return len(self.list_text)

    def __getitem__(self, idx):
        text = str(self.list_text[idx])
        text = text_preprocess(text)
        encoding = self.tokenizer.encode_plus(
            text,
            truncation=self.config["TOKENIZER"]["TRUNCATION"],
            add_special_tokens=self.config["TOKENIZER"]["ADD_SPECIAL_TOKENS"],
            max_length=self.config["TOKENIZER"]["MAX_INPUT_LENGTH"],
            padding=self.config["TOKENIZER"]["PADDING"],
            return_attention_mask=self.config["TOKENIZER"]["RETURN_ATTENTION_MASK"],
            return_tensors="pt",
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
        }
