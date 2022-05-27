import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def correct_format(path):  # changer correct en result et True/False en 1/0
    df = pd.read_csv(path, encoding='ISO-8859-1')
    if (df['correct'][1] == True) or (df['correct'][1] == False):
        df['correct'] = np.where(df['correct'] == True, 1, 0)
    df.rename(columns={'correct': 'result'}, inplace=True)
    df.to_csv(path, index=False)
    print('Le format a été changé')


def fill_na(df_example_path, id_candidate='n'):
    """ This fonction doesn't change directy the file, you need to save it afterward
    :param df_example_path:
    :param id_candidate:
    :return: the modified csv that need to be saved
    """
    tab = pd.read_csv(df_example_path, encoding='ISO-8859-1')
    out_tab = tab.copy()
    out_tab['id_candidate'] = id_candidate
    for name in out_tab.columns:
        if name != 'id_candidate' and name != 'no_trial':
            out_tab[name] = out_tab.fillna(value='NaN', inplace=True)
    return out_tab


