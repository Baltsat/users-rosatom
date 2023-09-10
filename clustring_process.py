import json

import numpy as np
import tweetnlp
from sentence_transformers import SentenceTransformer

import pandas as pd
from transformers import pipeline

from utils import get_pc
from sklearn.cluster import KMeans
import pickle
import json
import os
import subprocess
# from umap import UMAP
import umap.umap_ as UMAP
import altair as alt

from sklearn.feature_extraction.text import CountVectorizer
from bertopic.representation import KeyBERTInspired
from hdbscan import HDBSCAN
from bertopic import BERTopic


class ModelCluster:
    def __init__(self):
        representation_model = KeyBERTInspired()
        umap_model = UMAP.UMAP(n_neighbors=4, n_components=3, min_dist=0.0, metric='chebyshev',
                               low_memory=True)  # chebyshev manhattan
        embedding_model = pipeline("feature-extraction", model="shibing624/text2vec-base-multilingual")
        hdbscan_model = HDBSCAN(min_cluster_size=2, min_samples=1, metric='euclidean', prediction_data=True)
        vectorizer_model = CountVectorizer(min_df=1, ngram_range=(1, 3))

        self.topic_model = BERTopic(
            # Pipeline models
            embedding_model=embedding_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            vectorizer_model=vectorizer_model,
            representation_model=representation_model,

            # Hyperparameters
            # top_n_words=5,
            # min_topic_size=1,
            low_memory=True,
            verbose=True
        )

    def prediction_cluster(self, question: dict):
        '''
        Предсказывает номера и имена кластеров для 1 вопроса в формате json.load()
        Args:
            question: dict
        Return
            question: dict
        '''
        question['answers'] = self.merge_duplicate_answers(question)
        data = [question['question'] + " " + answer['answer'] for answer in question['answers']]
        topics, probs = self.topic_model.fit_transform(data)
        # top_prob = zip(topics, probs)
        # res = []
        # for i, v in top_prob:
        #     if v >= 0.5:
        #         res.append(i)
        # print()
        # topics = res
        represent = self.topic_model.get_representative_docs()
        topic_dict = {key: value[0] for key, value in represent.items()}

        answers = question['answers']
        proc_answers = []

        for answer, cluster_id, prob in zip(answers, topics, probs):
            # if prob < 0.5:
            #     continue
            answer['cluster_id'] = cluster_id
            answer['topic_name'] = topic_dict.get(cluster_id) + " " + str(prob)

            proc_answers.append(answer)

        question['answers'] = proc_answers

        return question

    def merge_duplicate_answers(self, json_data):
        '''
        Объединяет дублирующиеся ответы и суммирует их количество.
        Args:
            json_data type: dict[list[dict]]: Cловарь с ключом 'asnwers' и вложенными в нём списком словарей с ключами: 'answer' и 'count'.

        Return:
            list: Новый список словарей с уникальными записями 'answer' и их суммированными значениями 'count'.
        '''
        unique_answers = {}

        for item in json_data['answers']:
            answer = item['answer']
            count = item['count']

            if answer in unique_answers:
                unique_answers[answer] += count
            else:
                unique_answers[answer] = count

        answers = [{'answer': answer, 'count': count} for answer, count in unique_answers.items()]

        return answers


class ClusteringAndProcessing:
    def __init__(self):
        self.sent_model = tweetnlp.Classifier("cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual",
                                              max_length=128)
        self.emb_model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2')

    def get_prediction_stats(self, json_data):
        """
        :param json_data: Train data to calculate metrics
        :return: GT and predicted array : neutral positive negative unknown
        """
        data = []
        prediction_label = [0, 0, 0, 0]  # neutral positive negative unknown
        gt = [0, 0, 0, 0]  # neutral positive negative unknown
        di = {"neutrals": 0, "positives": 1, "negatives": 2, "unknown": 3}
        sentiment_mapping = {
            'neutral': ('neutrals', 0),
            'positive': ('positives', 1),
            'negative': ('negatives', 2)
        }
        for batch in json_data:
            for batch_answer in batch['answers']:
                answer = batch_answer['answer']
                sentiment = batch_answer['sentiment']

                if self.sent_model is not None:
                    prediction = self.sent_model.predict(str(answer))
                else:
                    prediction = {'label': 'negatives'}
                prediction_label_idx = sentiment_mapping.get(prediction['label'], ('unknown', 3))
                result, prediction_label[prediction_label_idx[1]] = prediction_label_idx[0], 1

                gt_idx = di.get(sentiment, 3)
                gt[gt_idx] += 1

                batch_answer['cluster'] = answer  # TODO: processed answer
                batch_answer['sentiment_our'] = result

            data.append(batch)

            # print("GT: ", gt)
            # print("prediction_label: ", prediction_label)
            return gt, prediction_label

    def _get_cluster_id(self, embeds_pc, n_clusters):
        # Cluster the embeddings
        kmeans_model = KMeans(n_clusters=n_clusters, random_state=0)
        classes = kmeans_model.fit_predict(embeds_pc).tolist()
        return list(map(str, classes))

    def _get_topic_name(self, json_data):
        print(f"!!!!!!!!!!!!!!!!!! {json_data}")
        return ModelCluster().prediction_cluster(json_data)  # ["Topic_name"]

    def _generate_chart(self, df_c, xcol, ycol, lbl='on', color='basic', title=''):
        chart = alt.Chart(df_c).mark_circle(size=500).encode(
            x=
            alt.X(xcol,
                  scale=alt.Scale(zero=False),
                  axis=alt.Axis(labels=False, ticks=False, domain=False)
                  ),

            y=
            alt.Y(ycol,
                  scale=alt.Scale(zero=False),
                  axis=alt.Axis(labels=False, ticks=False, domain=False)
                  ),

            color=alt.value('#333293') if color == 'basic' else color,
            tooltip=['answer', 'sentiment']
        )

        if lbl == 'on':
            text = chart.mark_text(align='left', baseline='middle', dx=15, size=13, color='black').encode(text='answer',
                                                                                                          color=alt.value(
                                                                                                              'black'))
        else:
            text = chart.mark_text(align='left', baseline='middle', dx=10).encode()

        result = (chart + text).configure(background="#FDF7F0"
                                          ).properties(
            width=800,
            height=500,
            title=title
        ).configure_legend(
            orient='bottom', titleFontSize=18, labelFontSize=18)
        return result
    def get_processed_file_in_CSV(self, json_data, cluster_count: int = 5):
        """
        :param json_data: Json data
        :param cluster_count: Cluster count
        :return: data frame with result
        """
        PCA_EMB = 3
        df = pd.DataFrame(columns=['question', 'answer', 'sentiment', 'j', 'cluster_id', 'topic_name'])

        prediction_label = [0, 0, 0, 0]  # neutral positive negative unknown
        sentiment_mapping = {
            'neutral': ('neutrals', 0),
            'positive': ('positives', 1),
            'negative': ('negatives', 2)
        }

        new_row = None
        embedings = []
        answers = []
        js = []
        sentiments = []
        print(json_data)
        for idx, batch_answer in enumerate(json_data['answers']):
            print(batch_answer)
            answer = batch_answer['answer']

            if self.sent_model is not None:
                prediction = self.sent_model.predict(str(answer))
            else:
                prediction = {'label': 'negatives'}
            prediction_label_idx = sentiment_mapping.get(prediction['label'], ('unknown', 3))
            result, prediction_label[prediction_label_idx[1]] = prediction_label_idx[0], 1
            embedings.append(np.asarray(self.emb_model.encode(answer)))

            answers.append(answer)
            sentiments.append(result)
            js.append(idx)

        embeds_pc2 = get_pc(embedings, PCA_EMB)
        clusters = self._get_cluster_id(embeds_pc2, cluster_count)
        newchart_df = pd.DataFrame(columns=['answer','cluster','embed'])
        for i in range(len(clusters)):
            chart_df = {
                           'answer': answers[i],
                           'sentiment': sentiments[i],
                           'cluster': clusters[i],  # cluster_id
                           'embed': embeds_pc2[i]
                           }

            newchart_df = pd.concat([newchart_df, pd.DataFrame([chart_df])], ignore_index=True)
        newchart_df = pd.concat([newchart_df, pd.DataFrame(embeds_pc2)], axis=1)
        newchart_df.columns = newchart_df.columns.astype(str)
        #newchart_df.to_csv("./data/test.csv")
        alt_charts = self._generate_chart(newchart_df, '0', '1', lbl='on', color='cluster', title='Кластеризация')
        # alt_charts.save('./data/chart.html')
        topics = self._get_topic_name(json_data)
        print(f"&&&&&&&&&&&&&&&&& {topics}")
        print('\n\n\n\n')
        for i in range(len(answers)):
            topic_name = None
            cluster_id = -1
            for ans in topics['answers']:
                if ans['answer'] == answers[i]:
                    topic_name = ans['topic_name']
                    cluster_id = ans['cluster_id']
            new_row = {'question': json_data['question'],
                       'answer': answers[i],
                       'sentiment': sentiments[i],
                       'j': js[i],
                       'cluster_id': clusters[i],  # cluster_id
                       'topic_name': topic_name
                       # topics['answers'] == answers[i] # TODO: fix topics clustering to assign name
                       }
            print(f"^^^^^^^^^^^^^^ {new_row}")
            new_row_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_row_df], ignore_index=True)

        return df, alt_charts

if __name__ == "__main__":
    mc = ClusteringAndProcessing()
    with open("./data/all_649.json", encoding='utf-8-sig') as json_file:
        loaded = json.load(json_file)
        df, alt_charts = mc.get_processed_file_in_CSV(loaded)
        df.to_csv("./data/result_649.csv", index=False)
