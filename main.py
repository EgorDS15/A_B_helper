import streamlit as st
from st_pages import Page, show_pages, add_page_title
import base64
# Для изменения наименования на странице и добавления иконок, но не работает отображение
# show_pages(
#     [
#         Page("main.py", "Home", "🏠"),
#         Page("pages/ab_calc.py", "А/Б тесты", ":books:"),
#         Page("pages/machine_learning.py", "Машинное обучение", ":brain:")
#     ]
# )
st.header("Страничка временно пустует", divider='rainbow')
st.subheader("Пока все движ на других страницах")

file_ = open("kangoroo.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="kangoroo gif">',
    unsafe_allow_html=True,
)


