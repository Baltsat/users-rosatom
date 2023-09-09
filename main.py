import streamlit as st
import plotly.express as px

from pages_views.claster import ShowNClaterAndMoreInfo

st.markdown("<h1 style='text-align: center; background-color: #000045; color: #ece5f6'>Users Team</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; background-color: #000045; color: #ece5f6'>Улучшение представлений результатов в сервисе \"Мой голос\"</h4>", unsafe_allow_html=True)

# Создаем боковую панель
with st.sidebar:
    st.header("Ввод данных")

    # Вариант 1: Ввод данных вручную
    user_input = st.text_area("Введите JSON данные:")

    # Вариант 2: Загрузка файла JSON
    uploaded_file = st.file_uploader("Загрузите файл JSON", type=["json"])

show_data = False

# Обработка введенных данных или загруженного файла
if user_input:
    st.write("Вы ввели следующие данные:", user_input)
    show_data = True  # Устанавливаем флаг для отображения данных

if uploaded_file:
    st.write("Вы загрузили файл JSON:", uploaded_file)
    show_data = True  # Устанавливаем флаг для отображения данных

# Отображаем элементы только если флаг show_data установлен в True
if show_data:
    __show_N_claster = ShowNClaterAndMoreInfo()
    __show_N_claster._display_content()

data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

fig = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)
st.write(fig)