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


def change_id_candidate(path_file, id_candidate):
    tab = pd.read_csv(path_file, encoding='ISO-8859-1')
    tab['id_candidate'] = id_candidate
    tab.to_csv(path_file, index=False)


