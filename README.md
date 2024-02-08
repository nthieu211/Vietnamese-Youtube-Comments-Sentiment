# Vietnamese-Youtube-Comments-Sentiment

Web application classifies and statistics 7 emotional states such as enjoyment, disgust, sadness, anger, surprise, fear and others from Vietnamese comments on YouTube. The model is based on the pre-trained model of [**VinAI Research - PhoBert**](https://github.com/VinAIResearch/PhoBERT)

Update v2.0: New website

- API: FastAPI(python) + Postgres(Database)
- Web: ReactJS + Bootstrap 5.3

## Dataset

### [UIT-VSMEC (2019)](https://arxiv.org/abs/1911.09339) - **Emotion Recognition for Vietnamese Social Media Text**

The dataset contains **6,927** emotion-annotated sentences with 7 emotions (enjoyment, disgust, sadness, anger, surprise, fear and others). The authors of the article tried to apply machine learning and deep neural network models with UIT-VSMEC. Among the tested models, the Convolutional Neural Network (CNN) model performed the best, achieving a weighted F1-score of **59.74%**.

From 6,927 sentences divided into 3 subset:

- Training set: 5548 sentences
- Validation set: 686 sentences
- Test set: 693 sentences

## Model

### [PhoBERT (2020)](https://arxiv.org/abs/2003.00744) - **Pre-trained language models for Vietnamese**

The first public large-scale monolingual language models pre-trained for Vietnamese. Models using a 20GB word-level Vietnamese corpus with (~1GB ) Vietnamese Wikipedia and (~19GB) generated from Vietnamese news corpus.

Base on pre-trained PhoBERT-base, the model is built to classify 7 emotion labels of the data set.

### Model result

| #              | **First**  | **Second**        | **Third**         |
| -------------- | ---------- | ----------------- | ----------------- |
| Learning rate  | 1e-5       | 1e-5              | 1e-5              |
| Weight decay   | 1e-3       | 1e-2              | 1e-2              |
| LR Scheduler   | OneCycleLR | ReduceLROnPlateau | ReduceLROnPlateau |
| Linear layer   | None       | 512               | 256               |
| Dropout        | 0.3        | 0.4               | 0.5               |
| Batch size     | 16         | 16                | 8                 |
| Valid F1-score | 0.5985     | 0.6179            | 0.6268            |
| Valid Accuracy | 0.6137     | 0.6224            | 0.6283            |
| Test F1-score  | 0.5892     | 0.6291            | 0.6396            |
| Test Accuracy  | 0.5931     | 0.6291            | 0.6407            |

## Website v2.0:

API: using FastAPI(python3) and Postgres database

- Get all comments (limit 500 comments) from Youtube/
- Preprocess text (remove URL, HTML tag, typping error, word segment,...)
- Predict emotions, statistic result.
- Return result with paginated/
- Easily deploy with docker.

Website: build with Vite.js, using ReactJS

- Responsive web design.
- Support language: English and Vietnamese.

# References

1. [Emotion Recognition for Vietnamese Social Media Text](https://arxiv.org/abs/1911.09339)
2. [PhoBERT: Pre-trained language models for Vietnamese](https://arxiv.org/abs/2003.00744)
