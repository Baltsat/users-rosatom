import streamlit as st
import pandas as pd


class ShowClasters:

    def _display_content(self, df, cluster_count: int):
        # Чтение данных из CSV строки
        # df = pd.read_csv(pd.compat.StringIO(csv_data))
        i = 0

        grouped = df.groupby('cluster_id')

        for cluster_id, group_data in grouped:
            if (i < cluster_count):
                with st.expander(f'Кластер {cluster_id}'):
                    for index, row in group_data.iterrows():
                        answer = row['answer']
                        st.write(f'Answer: {answer}')
                        # Дополнительные данные о кластере, если они есть, могут быть отображены здесь
                i += 1




