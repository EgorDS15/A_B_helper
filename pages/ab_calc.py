import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config("Методология А/Б тестирования")
st.header("Методология А/Б тестирования", divider='rainbow')


class ABCalculator:
    def __init__(self, page_type):
        self.page_type = page_type

    def main_container(self):
        tab_confidence_interval, tab_mde, tab_sample_size, tab_one_side_test, tab_two_side = st.tabs([
            'Доверительный  интервал', 'MDE', 'Размер выборок', 'Односторонний тест', 'Двухсторонний тест'
        ])
        tab_confidence_interval.subheader('Все доверительные интервалы здесь будут рассчитаны для средних значений')

        # TODO: обработать ошибку, чтобы это был файл .csv
        uploaded_file = tab_confidence_interval.file_uploader(
            "Загрузите .csv файл с результатами: целевое действие по клиенту."
            "Файл должен содержать одну колонку без заголовка.")

        scale_options = ['Среднее значение(количественная шкала)', 'Средние конверсии(пропорции)',
                         'Разница конверсий(пропорции)']

        scale = tab_confidence_interval.selectbox(
            'Выберите для каких данных строим ДИ:',
            scale_options)

        if scale == scale_options[0]:
            tab_confidence_interval.latex(r'''
                                    \large CI = \overline{x} \pm Z \cdot SE
                                ''')
        elif scale == scale_options[1]:
            tab_confidence_interval.latex(r'''
                                        \large CI = \overline{x} \pm Z \cdot 
                                        \frac{\overline{x} \cdot (1 - \overline{x}) }{n}
                                        ''')
        else:
            tab_confidence_interval.latex(r'''
                                        \large CI = (\overline{x_1} - \overline{x_2}) \pm Z \cdot SE\\
                                        где\ SE = \sqrt{\frac{\overline{x_1} \cdot (1 - \overline{x_1})}{N_1} +
                                                        \frac{\overline{x_2} \cdot (1 - \overline{x_2})}{N_2}}
                                        ''')
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, header=None)
            conf_level_options = ['90', '95', '99']

            percent_bootstrap_samples = ['10', '20', '30', '40', '50', '60', '70', '80']

            conf_level = tab_confidence_interval.selectbox(
                'Выберите диапазон интервала(Z) в %:', conf_level_options)

            n_bootstrap_samples = tab_confidence_interval.text_input(
                'Введите количество бутстрап-выборок:')

            sample_size_for_bootstrap = tab_confidence_interval.selectbox(
                'Выберите размер выборок в процентах для бутстрапа:',
                percent_bootstrap_samples)

            a, b = self._conf_interval_mean(x=df,
                                            conf_level=int(conf_level),
                                            n_bootstrap_samples=int(n_bootstrap_samples),
                                            sample_size_from_data=int(sample_size_for_bootstrap))
            tab_confidence_interval.write(f"Истинное среднее значение находится в пределах интервала {a} и {b}")

        # tab_sample_size.markdown("""
        # <style>
        # .definitions {
        #     font-size:15px;
        # }
        # </style>
        # """, unsafe_allow_html=True)
        #

        tab_mde.write("`MDE(минимальный детектируемый эффект) - размер эффекта, который можно обнаружить с заданными вероятностями ошибок, стандартными отклонениями и размером групп`")

        tab_mde.markdown('<p>Конкретного алгоритма определения размера ожидаемого эффекта не существует, но есть некоторые подходы, которые могут быть полезны:</p>', unsafe_allow_html=True)
        tab_mde.markdown('<p>1. Оттолкнуться от минимального размера эффекта, который мы сможем распознать при тесте на всех пользователях. Мы не сможем распознать эффект меньшего размера;</p>', unsafe_allow_html=True)
        tab_mde.markdown('<p>2. Использовать опыт прошедших тестов. Если ранее проводились похожие тесты, можем использовать результаты их оценок для определения целевого эффекта;</p>', unsafe_allow_html=True)
        tab_mde.markdown('<p>3. Исходить из затрат на проведение теста. Например, нет смысла выбирать MDE меньше, чем себестоимость эксперимента.</p>', unsafe_allow_html=True)


        n_mde = tab_mde.text_input('Количество наблюдений в Контрольной группе')
        tab_mde.write(n_mde)
        sd_frst_group = tab_mde.text_input('Введите стандартное отклонение метрики ПЕРВОЙ группы по истории')
        tab_mde.write(sd_frst_group)
        sd_scnd_group = tab_mde.text_input('Введите стандартное отклонение метрики метрики ВТОРОЙ группы по истории')
        tab_mde.write(sd_scnd_group)
        alpha_mde = tab_mde.text_input('Введите выбранный уровень значимости(alpha):')
        tab_mde.write(alpha_mde)
        beta_mde = tab_mde.text_input('Введите выбранную стат, мощность(beta):')
        tab_mde.write(beta_mde)

        if (n_mde is not None) & (sd_frst_group is not None) & (sd_scnd_group is not None) & (alpha_mde is not None) & (beta_mde is not None):
            res_mde = None
            tab_mde.write(f"Минимальный детектируемый эффект: {res_mde}")

        # mde = tab_sample_size.text_input('Введите MDE(Минимальный детектируемый эффект)')
        # st.write(mde)
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
