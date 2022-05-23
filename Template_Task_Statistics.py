import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


class Template_Task_Statistics:
    """ The redcap export in csv, change the path to the correct one"""
    redcap_csv = pd.read_csv('/Users/melissamarius/Downloads/STOCADPinelfollowup_DATA_2022-05-19_1532.csv')

    """ List of diminutives of the disorder with index corresponding to the number in the redcap, 
    names can be change except 'all' but the order cannot be changed """
    list_disorder = ['all', 'toc', 'du', 'db', 'ta', 'tus', 's']

    """ Color for the graph, respectfully the color for no_disorder representation and the color for disorder 
    representation"""
    col = ['black', 'darkred']

    """ Path of the file, which should be set in every class analysis"""
    path = '../get_csv_cog_tasks/all_csv/seven_diff'

    def __init__(self, pratice=False):
        """
        :param pratice: if you want to keep to the pratice in the other put pratice=True
        """
        self.csv_files = glob.glob(os.path.join(self.path, "*.csv"))
        self.df_files = [pd.read_csv(f, encoding='ISO-8859-1') for f in self.csv_files]

        """ Deleting all the lines corresponding to the pratice from all the csv
        """
        if not pratice:
            i = 0
            while self.df_files[0].no_trial[i] != 0:
                i += 1
            for j in range(len(self.df_files)):
                self.df_files[j] = self.df_files[j].drop(np.arange(i))

    def get_id(self, df):
        """ method to get the redcap id from a dataframe
        """
        return int(str(df['id_candidate'].tail(1).item())[8:11])

    def get_list_patients(self, disorder="all"):
        """"
        :return an array with the id of the subject and 1 if the subject has the considered disorder and 0 otherwise
        """
        all_disorder = np.array(self.redcap_csv['diagnostic_principal'])
        if disorder == 'all':
            list_patients = np.where(all_disorder == 0, 0, 1)
        else:
            list_patients = np.select([all_disorder == 0, all_disorder == self.list_disorder.index(disorder)],
                                      [0, 1], -1)
        return pd.DataFrame(np.array([np.array(self.redcap_csv.record_id), list_patients]).T)

    def success_rate_trials(self, df):
        """
        :return: 2 arrays, an array with no_trial in index 0 and an array with the success rate for all subjects
        """
        success = [np.mean(df["result"][:n]) * 100 for n in range(1, len(df['result']) + 1)]
        return np.array(success)

    def total_people(self, mental_disorder=True, disorder='all'):
        """
        :param disorder:
        :return: the number of people suffering from the disorder selected in our data regarding the redcap csv
        """
        if not mental_disorder:
            return self.get_list_patients('all')[1][self.get_list_patients(disorder)[1] == 0]
        else:
            return self.get_list_patients(disorder)[1][self.get_list_patients(disorder)[1] == 1]

    def get_no_trials(self, *args):
        """ Get the numbers of trials within a certain category
        """

    def plot_pourcentage(self, *args):
        """ Create a graph representing success rate depending on the number of trials
            """

    def stats(self, wit=False, type=False, numbers_trials=[]):
        """
        :return: dataframe containing descriptive statistics of the data for every subjects
        """
        tab = []
        if wit:
            for df in self.df_files:
                if type == True:
                    df = df[df['no_trial'].isin(numbers_trials)]
                id = int(str(df['id_candidate'].tail(1).item())[8:11])
                disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
                count_tot = [np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)]
                tab.append([np.mean(df['result']) * 100, np.mean(df['reaction_time']), np.max(df['reaction_time']),
                            sum(count_tot) / len(count_tot), np.max(count_tot), np.min(count_tot), int(disorder_id)])
            tab = pd.DataFrame(tab)
            tab.columns = ['success_rate', 'average_reaction_time', 'maximum_reaction_time', 'average_count_image',
                           'maximum_count_image', 'minimum_count_image', 'disorder']
        else:
            for df in self.df_files:
                if type == True:
                    df = df[df['no_trial'].isin(numbers_trials)]
                id = int(str(df['id_candidate'].tail(1).item())[8:11])
                disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
                tab.append([np.mean(df['result']) * 100, np.mean(df['reaction_time']), np.max(df['reaction_time']),
                            int(disorder_id)])
            tab = pd.DataFrame(tab)
            tab.columns = ['success_rate', 'average_reaction_time', 'maximum_reaction_time', 'disorder']
        return tab

    def boxplot_average(self, category='success_rate', *args):
        """
        :param category: the category of the output of stats that you want to see
        :return: a boxplot and a barplot of the average success result of a certain category (choose among the columns
        of the output of stats()
        """


a = Template_Task_Statistics()
