import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def correct_format(df):  # changer correct en result
    df['correct'] = np.where(df['correct'] == True, 1, 0)
    df.rename(columns={'correct': 'result'}, inplace=True)
    return df
