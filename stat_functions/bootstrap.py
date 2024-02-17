import numpy as np
import pandas as pd


def bootstrap(x: pd.DataFrame, n_bootstrap_samples: int, sample_size_from_data: int):
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
