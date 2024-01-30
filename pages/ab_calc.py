import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config("Методология А/Б тестирования")
st.header("Методология А/Б тестирования", divider='rainbow')


class ABCalculator:
    def __init__(self, page_type):
        self.page_type = page_type

    def main_container(self):
        confidence_interval, tab_sample_size, tab_one_side_test, tab_two_side = st.tabs([
            'Доверительный  интервал', 'Размер выборок', 'Односторонний тест', 'Двухсторонний тест'
        ])
        confidence_interval.subheader('Все доверительные интервалы здесь будут рассчитаны для средних значений')

        # TODO: обработать ошибку, чтобы это был файл .csv
        uploaded_file = confidence_interval.file_uploader(
            "Загрузите .csv файл с результатами: целевое действие по клиенту."
            "Файл должен содержать одну колонку без заголовка.")

        scale_options = ['Среднее значение(количественная шкала)', 'Средние конверсии(пропорции)',
                         'Разница конверсий(пропорции)']

        scale = confidence_interval.selectbox(
            'Выберите для каких данных строим ДИ:',
            scale_options)

        if scale == scale_options[0]:
            confidence_interval.latex(r'''
                                    \large CI = \overline{x} \pm Z \cdot SE
                                ''')
        elif scale == scale_options[1]:
            confidence_interval.latex(r'''
                                        \large CI = \overline{x} \pm Z \cdot 
                                        \frac{\overline{x} \cdot (1 - \overline{x}) }{n}
                                        ''')
        else:
            confidence_interval.latex(r'''
                                        \large CI = (\overline{x_1} - \overline{x_2}) \pm Z \cdot SE\\
                                        где\ SE = \sqrt{\frac{\overline{x_1} \cdot (1 - \overline{x_1})}{N_1} +
                                                        \frac{\overline{x_2} \cdot (1 - \overline{x_2})}{N_2}}
                                        ''')
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, header=None)
            conf_level_options = ['90', '95', '99']

            percent_bootstrap_samples = ['10', '20', '30', '40', '50', '60', '70', '80']

            conf_level = confidence_interval.selectbox(
                'Выберите диапазон интервала(Z) в %:', conf_level_options)

            n_bootstrap_samples = confidence_interval.text_input(
                'Введите количество бутстрап-выборок:')

            sample_size_for_bootstrap = confidence_interval.selectbox(
                'Выберите размер выборок в процентах для бутстрапа:',
                percent_bootstrap_samples)

            a, b = self._conf_interval_mean(x=df,
                                            conf_level=int(conf_level),
                                            n_bootstrap_samples=int(n_bootstrap_samples),
                                            sample_size_from_data=int(sample_size_for_bootstrap))
            confidence_interval.write(f"Истинное среднее значение находится в пределах интервала {a} и {b}")

        mde = tab_sample_size.text_input('Введите MDE(Минимальный детектируемый эффект)')
        st.write(mde)
        stat_frst_group = tab_sample_size.text_input('Введите среднее значение метрики ПЕРВОЙ группы из истории')
        st.write(stat_frst_group)
        stat_scnd_group = tab_sample_size.text_input('Введите среднее значение метрики ВТОРОЙ группы из истории')
        st.write(stat_scnd_group)
        alpha = tab_sample_size.text_input('Введите выбранный уровень значимости(alpha)')
        st.write(alpha)
        beta = tab_sample_size.text_input('Введите выбранную стат, мощность(beta)')
        st.write(beta)

    def bootstrap(self, x: pd.DataFrame, n_bootstrap_samples: int, sample_size_from_data: int):
        """
        Function calculate bootstrap statistics
        :param x: data
        :param n_bootstrap_samples: n smaller data samples from original data
        :param sample_size_from_data: count of observations in bootstrap sample
        :return: data len: int, mean of means from bootstrap samples: float, standard error: float
        """
        means = []
        n = x.shape[0]
        df = x.reset_index()
        sample_size = int(n / 100 * int(sample_size_from_data))

        for i in range(n_bootstrap_samples):
            means.append(df.iloc[:, 1].sample(sample_size).mean())

        mean_means = np.mean(means)
        se = np.std(means) / np.sqrt(sample_size_from_data)
        return n, mean_means, se

    def _conf_interval_mean(self, x, conf_level: float, n_bootstrap_samples: int, sample_size_from_data: int):
        _, mean, se = self.bootstrap(x, n_bootstrap_samples, sample_size_from_data)
        # print(f" {mean} - {conf_level} * {se}")
        return np.round(mean - conf_level * se, 2), np.round(mean + conf_level * se, 2)
        # return mean, conf_level, se

    def _conf_interval_proportion(self, x, conf_level: float, n_bootstrap_samples: int, sample_size_from_data: int):
        _, mean, se = self.bootstrap(x, n_bootstrap_samples, sample_size_from_data)
        return mean - conf_level * np.sqrt((mean * (1 - mean)) / sample_size_from_data), mean + conf_level * np.sqrt(
            (mean * (1 - mean)) / sample_size_from_data)

    # TODO: должна быть выборка 0/1 для КГ и выборка(или среднее значение по ЦГ)
    # def _conf_interval_proportion_diff(self, x, conf_level: float, n_bootstrap_samples: int, sample_size_from_data: int):
    #     _, mean, se = self.bootstrap(x, n_bootstrap_samples, sample_size_from_data)
    #     return mean - conf_level * se, mean + conf_level * se


ABCalculator("АБ").main_container()
