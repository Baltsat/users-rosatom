# My Voice — clustering open-ended survey answers by meaning

Hackathon solution for Rosatom's "My Voice" service, by team **Users**. The service collects free-text answers from employees; the problem is grouping thousands of differently-worded answers that mean the same thing.

We group them with multilingual BERT embeddings and a layered clustering pipeline, then present the result in a web interface. The approach is robust to typos and misspellings, and it keeps latent signal that naive matching throws away — emoji and punctuation.

![demo](https://github.com/Baltsat/users-rosatom/blob/main/data/gf.gif)

## Model comparison

| Model | F1 macro | Time |
| --- | --- | --- |
| Naive — every word is its own cluster | 0.81 | 10 ms |
| Levenshtein similarity — answers >63% similar form one cluster | 0.87 | 102 ms |
| Levenshtein + preprocessing (lemmatisation, punctuation removal) | 0.89 | 1 s |
| SelfClusterModel #1 + sentiment transformer (BERT-multilingual + PCA + KMeans, TweetNLP + XLM-RoBERTa) | 0.92 | |
| SelfClusterModel #2 | 0.94 | 6 s |
| **SelfClusterModel #2 + sentiment transformer** | **0.97** | |

## How it works

-   Preprocessing of raw answers: punctuation removal, profanity filtering, lemmatisation.
-   Fine-tuned deep-learning models on the processed data: TweetNLP, XLM-RoBERTa multilingual sentiment classification, BERTopic.
-   Multi-stage clustering: UMAP → HDBSCAN → CountVectorizer → TF-IDF.
-   Sentiment scoring with XLM-RoBERTa trained on user comments.
-   Clustering visualised through a Streamlit interface.

The combination of BERT-based text processing, Streamlit visualisation, and handling of both Russian and English gives accuracy without costing usability.

## Stack

`Python 3`, `git`, `GitHub` — development
`HF Transformers`, `TweetNLP`, `BERTopic` — deep learning
`Scikit-Learn`, `UMAP`, `KMeans` — machine learning
`Plotly`, `Streamlit`, `AltChart` — visualisation

## Install and run

Requires Python 3.9 or newer.

```bash
git clone https://github.com/Baltsat/users-rosatom.git
pip install -r requirements.txt
streamlit run main.py
```

## Notebooks

-   `research_models_visualization.ipynb` — gradient-boosting model experiments
-   `data_preprocess.ipynb` — data preprocessing

## Django API

The project uses Django and Django REST Framework to expose the question-and-answer data.

### `/api/qaitems`

-   `GET` — list all QA items
-   `POST` — create a new QA item

### Data structure

-   `question` — question text
-   `answer` — answer text
-   `sentiment` — sentiment of the item
-   `j` — J value
-   `cluster_id` — cluster identifier
-   `topic_name` — topic name

### Running the API

1. Clone the repository.
2. Create and activate a virtual environment.
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`

Example request: `http://localhost:8000/api/qaitems/`

## Team

| Name | Role | Contact |
| --- | --- | --- |
| Konstantin Baltsat | Data analysis | [t.me/baltsat](https://t.me/baltsat) |
| Aleksandr Serov | Machine learning | [t.me/thegoldian](https://t.me/thegoldian) |
| Artem Tarasov | Full stack | [t.me/tarasovxx](https://t.me/tarasovxx) |
| Sergey Vandanov | Machine learning | [t.me/rapid76](https://t.me/rapid76) |
| Daniil Galimov | Data analysis | [t.me/Dan_Gan](https://t.me/Dan_Gan) |
