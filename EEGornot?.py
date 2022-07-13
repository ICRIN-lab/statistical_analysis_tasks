import numpy as np
import pandas as pd
import glob
import os
import scipy.stats as sps
import seaborn as sns
import matplotlib.pyplot as plt


def get_list_patients(self, EEG ="    "):
    """" Get the list of people with or without EEG"
    """
    all_EEG = np.array(self.redcap_csv['type_etude___1'])
    if disorder == 'all':
        list_patients = np.where(all_disorder == 0, 0, 1)
    else:
        list_patients = np.select([all_disorder == 0, all_disorder == self.list_disorder.index(disorder)],
                                  [0, 1], -1)
    return pd.DataFrame(np.array([np.array(self.redcap_csv.record_id), list_patients]).T)

    success = [np.mean(df['type_etude___1'][:n]) * 100 for n in range(1, len(df['type_etude___1']) + 1)]
    return np.array(success)