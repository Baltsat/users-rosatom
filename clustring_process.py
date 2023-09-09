import json

import numpy as np
import tweetnlp
from sentence_transformers import SentenceTransformer

import pandas as pd
from utils import get_pc
from sklearn.cluster import KMeans
import pickle
import json
import os
import subprocess


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

                batch_answer['cluster'] = answer # TODO: processed answer
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
        # df_clust.columns = df_clust.columns.astype(str)
        # generate_chart(df_clust.iloc[:sample], '0', '1', lbl='on', color='cluster', title='Clustering with 2 Clusters')

    def _get_topic_name(self):
        return "Topic_name"

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

            new_row = {'question': json_data['question'],
                       'answer': answer,
                       'sentiment': result,
                       'j': idx}

        embeds_pc2 = get_pc(embedings, PCA_EMB)

        new_row['cluster_id'] = self._get_cluster_id(embeds_pc2, cluster_count)
        new_row['topic_name'] = self._get_topic_name()
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)

        print(df)
        return df


if __name__ == "__main__":
    mc = ClusteringAndProcessing()
    with open("./data/all_324.json", encoding='utf-8-sig') as json_file:
        loaded = json.load(json_file)
        mc.get_processed_file_in_CSV(loaded)
