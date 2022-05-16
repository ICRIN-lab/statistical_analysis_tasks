import numpy as np
import pandas as pd
import glob
import os


class Task_result_summary:
    csv_summary = []
    list_disease = []

    def __init__(self, path, disease='all', pratice=False):
        """
        :param pratice: if you want to keep to the pratice in the analysis put pratice=True
        """
        self.disease = disease
        self.csv_files = glob.glob(os.path.join(path, "*.csv"))
        self.df_files = [pd.read_csv(f, encoding='ISO-8859-1') for f in self.csv_files]

        """ Deleting all the lines corresponding to the pratice from all the csv
        """
        if not pratice:
            i = 0
            while self.df_files[1].no_trial[i] != 0:
                i += 1
            for j in range(len(self.df_files)):
                self.df_files[j] = self.df_files[j].drop(np.arange(i))

    def success_rate_trials(self):
        """
        :return: 2 arrays, an array with no_trial in index 0 and an array with the success rate for all subjects
        """
        success = []
        for df in self.df_files:
            new_success_rate = [np.mean(df.loc[:n, "result"]) * 100 for n in range(1, len(df['result']) + 1)]
            success.append(new_success_rate)
        return np.array(success).T

    def stats(self):
        """
        :return: dataframe containing descriptive statistics of the data for all subjects
        """

    def plot_pourcentage(self, *args):
        """ Create a graph representing success rate depending on the number of trials
            """

