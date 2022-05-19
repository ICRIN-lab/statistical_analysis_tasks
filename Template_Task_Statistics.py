import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


class Template_Task_Statistics:
    csv_summary = []
    redcap_csv = pd.read_csv('/Users/melissamarius/Downloads/STOCADPinelfollowup_DATA_2022-05-17_1439.csv',
                             encoding='ISO-8859-1')
    list_disorder = ['all', 'toc', 'du', 'db', 'ta', 'tus', 's']
    path = '/Users/melissamarius/Documents/all_csv/where_is_tockie'

    def __init__(self, disorder='all', pratice=False):
        """
        :param pratice: if you want to keep to the pratice in the other put pratice=True
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
                disorder_id = list_patients[list_patients[1, :] == id][2]
                count_tot = [np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)]
                tab.append([np.mean(df['result']), np.mean(df['reaction_time']), np.max(df['reaction_time']),
                            sum(count_tot) / len(count_tot), np.max(count_tot), np.min(count_tot), disorder_id])
            tab = pd.DataFrame(tab)
            tab.columns = ['success_rate', 'average_reaction_time', 'maximum_reaction time', 'average_count_image',
                           'maximum_count_image', 'minimum_count_image', 'disorder']
        else:
            for df in self.df_files:
                id = str(df['id_candidate'][10])[8:11]
                disorder_id = list_patients[list_patients[0, :] == id][1]
                tab.append([np.mean(df['result']), np.mean(df['reaction_time']), np.max(df['reaction_time']),
                            disorder_id])
            tab = pd.DataFrame(tab)
            tab.columns = ['success_rate', 'average_reaction_time', 'maximum_reaction time', 'disorder']
        return tab

    def boxplot_success_rate(self, disorder='all'):
        """
        :return:  a boxplot and a barplot of the average success_rate per disorder
        """
        success = pd.DataFrame({"No_disorder": self.stats()['disorder_id' == 0]['success_rate'], disorder:
            self.stats()['disorder_id' == self.list_disorder.index(disorder)][
                'success_rate']})
        mean_success = success.apply(np.mean, axis=1)
        plt.figure()
        success[['No_disorder', disorder]].plot(kind='box', title=f'Comparaison of success rate for {disorder}')
        plt.show()
        # plt.boxplot(success)
        plt.figure()
        plt.bar(mean_success)
        plt.show()

    def boxplot_reaction_time(self, disorder='all'):
        """
        :return: a boxplot and a barplot of the average reaction time per disorder
        """
        time = pd.DataFrame({"No_disorder": self.stats()['disorder_id' == 0]['average_reaction_time'], disorder:
            self.stats()['disorder_id' == self.list_disorder.index(disorder)][
                'average_reaction_time']})
        mean_time = time.apply(np.mean, axis=1)

        plt.figure()
        time[['No_disorder', disorder]].plot(kind='box', title=f'Comparaison of average reaction time for {disorder}')
        plt.show()
        # plt.boxplot(time)
        plt.figure()
        plt.bar(mean_time)
        plt.show()


a = Template_Task_Statistics()
a.get_list_patients()
