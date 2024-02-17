def sample_size(tab):
    stat_frst_group = tab.text_input('Введите среднее значение метрики ПЕРВОЙ группы из истории')
    stat_scnd_group = tab.text_input('Введите среднее значение метрики ВТОРОЙ группы из истории')
    alpha = tab.text_input('Введите выбранный уровень значимости(alpha)')
    beta = tab.text_input('Введите выбранную стат, мощность(beta)')