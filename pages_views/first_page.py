import streamlit as st
from PIL import Image


class MainPage:
    def visualizeMainPage(self):
        # Фотографии и описания
        photos_with_descriptions = [
            "Frontend", "Machine Learning", "Data Analyse"
        ]

        # Отображение фотографий
        col1, col2, col3 = st.columns(3)
        col4, col5 = st.columns(2)
        with col1:
            image = Image.open('pages_views/image/artyom.jpg')
            st.image('pages_views/image/kostya.jpg', caption=photos_with_descriptions[2], use_column_width=True)
            #st.write(photos_with_descriptions[3])


        with col2:
            st.image('pages_views/image/sergey.jpg', caption=photos_with_descriptions[1], use_column_width=True)
            #st.write(photos_with_descriptions[1])

        with col3:
            st.image('pages_views/image/daniil.jpg', caption=photos_with_descriptions[2], use_column_width=True)
            #st.write(photos_with_descriptions[2])

        with col4:
            st.image(image, caption=photos_with_descriptions[0], use_column_width=True)
            #st.write(photos_with_descriptions[0])

        with col5:
            st.image('pages_views/image/sasha.jpg', caption=photos_with_descriptions[1], use_column_width=True)
            #st.write(photos_with_descriptions[4])