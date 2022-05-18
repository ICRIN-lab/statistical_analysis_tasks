import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


class Template_Task_Statistics:
    csv_summary = []
    redcap_csv = pd.read_csv('/Users/melissamarius/Downloads/STOCADPinelfollowup_DATA_2022-05-17_1439.csv', encoding='ISO-8859-1')
    list_disorder = ['all', 'toc', 'du', 'db', 'ta', 'tus', 's']
    path = '/Users/melissamarius/Documents/all_csv/where_is_tockie'

    def __init__(self, disorder='all', pratice=False):
        """
        :param pratice: if you want to keep to the pratice in the analysis put pratice=True
        """
        self.disorder = disorder
        self.csv_files = glob.glob(os.path.join(self.path, "*.csv"))
        self.df_files = [pd.read_csv(f, encoding='ISO-8859-1') for f in self.csv_files]

        """ Deleting all the lines corresponding to the pratice from all the csv
        """
        if not pratice:
            i = 0
            while self.df_files[1].no_trial[i] != 0:
                i += 1
            for j in range(len(self.df_files)):
                self.df_files[j] = self.df_files[j].drop(np.arange(i))

    def get_list_patients(self, disorder="all"):
        """"
        :return an array with the id of the subject and 1 if the subject has the considered disorder and 0 otherwise
        """
        all_disorder = np.array(self.redcap_csv['diagnostic_principal'])
        if disorder == 'all':
            list_patients = np.where(all_disorder == 0, 0, 1)
        else:
            list_patients = np.where(all_disorder != self.list_disorder.index(disorder), -1)
            list_patients = np.where(list_patients == self.list_disorder.index(disorder), 1)
        return [self.redcap_csv['record_id'], list_patients]

    def success_rate_trials(self, df):
        """
        :return: 2 arrays, an array with no_trial in index 0 and an array with the success rate for all subjects
        """
        success = [np.mean(df.loc[:n, "result"]) * 100 for n in range(1, len(df['result']) + 1)]
        return np.array(success)

    def plot_pourcentage(self, *args):
        """ Create a graph representing success rate depending on the number of trials
            """

    def stats(self, wit=False):
        """
        :return: dataframe containing descriptive statistics of the data for every subjects
        """
        tab = []
        list_patients = self.get_list_patients()
        if wit:
            for df in self.df_files:
                id = str(df['id_candidate'][10])[8:11]
                disorder = list_patients[list_patients[1, :] == id][2]
                count_tot = [np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)]
                tab.append([np.mean(df['result']), np.mean(df['reaction_time']), np.max(df['reaction_time']),
                                     sum(count_tot) / len(count_tot), np.max(count_tot), np.min(count_tot), disorder])
            tab = pd.DataFrame(tab)
            tab.columns = ['success_rate', 'average_reaction_time', 'maximum_reaction time', 'average_count_image',
                           'maximum_count_image', 'minimum_count_image', 'disorder']
        else:
            for df in self.df_files:
                id = str(df['id_candidate'][10])[8:11]
                disorder = list_patients[list_patients[1, :] == id][2]
                tab.append([np.mean(df['result']), np.mean(df['reaction_time']), np.max(df['reaction_time']), 'disorder'])
            tab = pd.DataFrame(tab)
            tab.columns = ['success_rate', 'average_reaction_time', 'maximum_reaction time', 'disorder']
        return tab

    def boxplot_success_rate(self, wit=False, disorder='all'):
        """
        :return:  a barplot of the average success_rate per disorder
        """
        success = pd.DataFrame(self.stats(wit)['success_rate'], self.get_list_patients(disorder))
        plt.boxplot(success)
        plt.barplot(success)

    def boxplot_reaction_time(self, disorder='all'):
        """
        :return: a barplot of the average reaction time per disorder
        """
