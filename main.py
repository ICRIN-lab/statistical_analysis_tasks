import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

# test
paths = ['/Users/melissamarius/Documents/all_csv/lucifer', '/Users/melissamarius/Documents/all_csv/seven_diff',
         '/Users/melissamarius/Documents/all_csv/symmetry', '/Users/melissamarius/Documents/all_csv/where_is_tockie']
tasks = ['lucifer', 'seven_diff', 'symmetry', 'wit']


def stats(df, task):
    df = df.drop([0, 1, 2])
    if task == 'wit':
        count_tot = [np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)]
        tab = pd.DataFrame(np.array(
            [df['id_candidate'][3], np.mean(df['result']), np.mean(df['reaction_time']),
             np.max(df['reaction_time']), np.min(df['reaction_time']),
             sum(count_tot) / len(count_tot), np.max(count_tot), np.min(count_tot)])).T
        tab.columns = ['Id', 'Success_rate', 'Average_reaction_time', 'max_reaction_time', 'min_reaction_time',
                       'Average_count_image', 'max_count_image', 'min_count_image']
    else:
        tab = pd.DataFrame(np.array(
            [df['id_candidate'][3], np.mean(df['result']), np.mean(df['reaction_time']),
             np.max(df['reaction_time']), np.min(df['reaction_time'])])).T
        tab.columns = ['Id', 'Success_rate', 'Average_reaction_time', 'max_reaction_time', 'min_reaction_time']

    return tab


def success_rate_with_time(df):
    return [np.mean(df.loc[:n, "result"]) * 100 for n in range(1, len(df['result']))]


def plot_success_rate(df):
    return plt.plot(np.arange(0, len(success_rate_with_time(df))), success_rate_with_time(df),
                    label=df['id_candidate'][3])


for path, task in zip(paths, tasks):
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    plt.figure()
    plt.title(f'Pourcentages de réussites en fonction des essais pour la tache {task}')
    for f in csv_files:
        df_csv = pd.read_csv(f, encoding='ISO-8859-1')
        plot_success_rate(df_csv)
    plt.legend()
    plt.show()


    def stats(self, wit=False):
        """
        :return: dataframe containing descriptive statistics of the data for every subjects
        """
        tab = []
        if wit:
            for df in self.df_files:
                count_tot = [np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)]
                tab = tab.happen(
                    np.array([np.mean(df['result']), np.mean(df['reaction_time']), np.max(df['reaction_time']),
                              sum(count_tot) / len(count_tot), np.max(count_tot), np.min(count_tot)])).T
            tab = pd.DataFrame(tab)
            tab.columns = ['success_rate', 'average_reaction_time', 'maximum_reaction time', 'average_count_image',
                           'maximum_count_image', 'minimum_count_image']
        else:
            for df in self.df_files:
                tab = tab.happen(
                    np.array([np.mean(df['result']), np.mean(df['reaction_time']), np.max(df['reaction_time'])])).T
                tab = pd.DataFrame(tab)
            tab.columns = ['success_rate', 'average_reaction_time', 'maximum_reaction time']
        return tab

a = pd.read_csv('/Users/melissamarius/Documents/all_csv/where_is_tockie/QUI_KEV_001_2022-05-11_18h07.csv',
                encoding='ISO-8859-1')
print(int(str(a['id_candidate'][1])[8:11]))