import numpy as np
import pandas as pd

from stat_functions.bootstrap import bootstrap


# TODO: должна быть выборка 0/1 для КГ и выборка(или среднее значение по ЦГ)
# def _conf_interval_proportion_diff(self, x, conf_level: float, n_bootstrap_samples: int, sample_size_from_data: int):
#     _, mean, se = self.bootstrap(x, n_bootstrap_samples, sample_size_from_data)
#     return mean - conf_level * se, mean + conf_level * se
def conf_interval(tab):
    tab.subheader('Все доверительные интервалы здесь будут рассчитаны для средних значений')

    # TODO: обработать ошибку, чтобы это был файл .csv
    uploaded_file = tab.file_uploader(
        "Загрузите .csv файл с результатами: целевое действие по клиенту."
        "Файл должен содержать одну колонку без заголовка.")

    scale_options = ['Среднее значение(количественная шкала)', 'Средние конверсии(пропорции)',
                     'Разница конверсий(пропорции)']

    scale = tab.selectbox(
        'Выберите для каких данных строим ДИ:',
        scale_options)

    if scale == scale_options[0]:
        tab.latex(r'''
                    \large CI = \overline{x} \pm Z \cdot SE
                   ''')
    elif scale == scale_options[1]:
        tab.latex(r'''
                    \large CI = \overline{x} \pm Z \cdot 
                    \frac{\overline{x} \cdot (1 - \overline{x}) }{n}
                    ''')
    else:
        tab.latex(r'''
                    \large CI = (\overline{x_1} - \overline{x_2}) \pm Z \cdot SE\\
                    где\ SE = \sqrt{\frac{\overline{x_1} \cdot (1 - \overline{x_1})}{N_1} +
                                    \frac{\overline{x_2} \cdot (1 - \overline{x_2})}{N_2}}
                    ''')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, header=None)
        conf_level_options = ['90', '95', '99']

        percent_bootstrap_samples = ['10', '20', '30', '40', '50', '60', '70', '80']

        conf_level = tab.selectbox(
            'Выберите диапазон интервала(Z) в %:', conf_level_options)

        n_bootstrap_samples = tab.text_input(
            'Введите количество бутстрап-выборок:')

        sample_size_for_bootstrap = tab.selectbox(
            'Выберите размер выборок в процентах для бутстрапа:',
            percent_bootstrap_samples)

        a, b = _conf_interval_mean(x=df,
                                   conf_level=int(conf_level),
                                   n_bootstrap_samples=int(n_bootstrap_samples),
                                   sample_size_from_data=int(sample_size_for_bootstrap))
        tab.write(f"Истинное среднее значение находится в пределах интервала {a} и {b}")


def _conf_interval_mean(x, conf_level: float, n_bootstrap_samples: int, sample_size_from_data: int):
    _, mean, se = bootstrap(x, n_bootstrap_samples, sample_size_from_data)
    # print(f" {mean} - {conf_level} * {se}")
    return np.round(mean - conf_level * se, 2), np.round(mean + conf_level * se, 2)
    # return mean, conf_level, se


def _conf_interval_proportion(x, conf_level: float, n_bootstrap_samples: int, sample_size_from_data: int):
    _, mean, se = bootstrap(x, n_bootstrap_samples, sample_size_from_data)
    return mean - conf_level * np.sqrt((mean * (1 - mean)) / sample_size_from_data), mean + conf_level * np.sqrt(
        (mean * (1 - mean)) / sample_size_from_data)
