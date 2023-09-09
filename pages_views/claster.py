import streamlit as st

class ShowNClaterAndMoreInfo():
    def _display_content(self):
        # Список элементов
        elements = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5", "Элемент 6", "Элемент 7", "Элемент 8", "Элемент 9", "Элемент 10"]

        # Определите количество элементов, которые будут отображаться по умолчанию
        default_display_count = 5


        # Отображение списка элементов
        for i in range(default_display_count):
            with st.expander(elements[i]):
                # Весь контент, который будет отображаться внутри элемента, должен быть в этом блоке
                st.write("Здесь находится информация о элементе.")


        show_all_elements = st.checkbox("Показать остальные элементы")

        # Если выбрано больше элементов, чем отображается по умолчанию
        if show_all_elements:
            remaining_elements = elements[default_display_count:]

            for element in remaining_elements:
                with st.expander(element):
                    # Весь контент, который будет отображаться внутри элемента, должен быть в этом блоке
                    st.write("Здесь находится информация о элементе.")



