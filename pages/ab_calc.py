import streamlit as st
import pandas as pd
import numpy as np

from stat_functions.conf_interval import conf_interval
from stat_functions.lift import lift
from stat_functions.mde import mde
from stat_functions.sample_size import sample_size

st.set_page_config("Методология А/Б тестирования")
st.header("Методология А/Б тестирования", divider='rainbow')


class ABCalculator:
    def __init__(self, page_type):
        self.page_type = page_type

    def main_container(self):
        tab_confidence_interval, tab_mde, tab_lift, tab_sample_size, tab_one_side_test, tab_two_side = st.tabs([
            'Доверительный  интервал', 'MDE', 'Lift', 'Размер выборок', 'Односторонний тест', 'Двухсторонний тест'
        ])

        conf_interval(tab_confidence_interval)
        mde(tab_mde)
        lift(tab_lift)
        sample_size(tab_sample_size)




ABCalculator("АБ").main_container()
