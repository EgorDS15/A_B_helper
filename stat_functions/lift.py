import numpy as np


def lift(tab):
    tab.write('`Lift – это отличие метрики теста от метрики контроля.`')

    metric_kg = tab.number_input('Введите итоговое значение метрики КГ:', step=0.01, format="%.3f")
    tab.write(metric_kg)
    metric_cg = tab.number_input('Введите итоговое значение метрики ЦГ:', step=0.01, format="%.3f")
    tab.write(metric_cg)

    if (metric_kg != 0) & (metric_cg != 0):
        LIFT = ((metric_kg - metric_cg) / metric_cg) * 100

        tab.write(f"Разница между метрикой контрольной группы и целевой: {np.round(LIFT, 3)}%")
