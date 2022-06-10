import numpy as np
import pandas as pd
import glob
import os
import scipy.stats as sps
import seaborn as sns
import matplotlib.pyplot as plt


class Template_Task_Statistics:
    """ The redcap export in csv, change the path to the correct one"""
    redcap_csv = pd.read_csv("D:\Telechargement\STOCADPinelfollowup_DATA_2022-06-02_1846.csv")

    """ List of diminutives of the disorder with index corresponding to the number in the redcap, 
    names can be change except 'all' but the order cannot be changed """
    list_disorder = ['all', 'ocd', 'du', 'db', 'ta', 'tus', 's']

    """ List of names to be shown in graphics"""
    list_graph_name = ['All disorders', 'OCD', 'Unipolar Depression', 'Bipolar Depression', 'Anxiety Disorder',
                       'Substance Use Disorder', 'Schizophrenia']

    """ Color for the graph, respectfully the color for healthy control representation and the color for the considered 
    disorder representation"""
    col = ['royalblue', 'crimson']

    """ Specific lines to get the color and the category to always match in the legend"""
    custom_lines = [plt.Line2D([0], [0], color=col[0], lw=4), plt.Line2D([0], [0], color=col[1], lw=4)]
    """ Path of the file, which should be set in every class analysis"""
    path = ""

    def __init__(self, pratice=False):
        """
        :param pratice: if you want to keep to the pratice in the analysis put pratice=True
        """

        self.csv_files = glob.glob(os.path.join(self.path, "*.csv"))
        self.df_files = [pd.read_csv(f, encoding='ISO-8859-1') for f in self.csv_files]

        """ Deleting all the lines corresponding to the pratice from all the csv
        """
        for j in range(len(self.df_files)):
            if not pratice:
                i = 0
                while self.df_files[j].no_trial[i] != 0:
                    i += 1
                self.df_files[j] = self.df_files[j].drop(np.arange(i))

    def get_id(self, df):
        """ method to get the redcap id from a dataframe
        """
        return int(str(df['id_candidate'].tail(1).item())[8:11])

    def get_list_patients(self, disorder="ocd"):
        """" Get the list of people with the considered disorder
        :return a dataframe with the id of the subject and 1 or 0 if the subject has the considered disorder
        """
        all_disorder = np.array(self.redcap_csv['diagnostic_principal'])
        if disorder == 'all':
            list_patients = np.where(all_disorder == 0, 0, 1)
        else:
            list_patients = np.select([all_disorder == 0, all_disorder == self.list_disorder.index(disorder)],
                                      [0, 1], -1)
        return pd.DataFrame(np.array([np.array(self.redcap_csv.record_id), list_patients]).T)

    def success_rate_trials(self, df):
        """ Get the success_rate regarding trials from the column result of the dataframe
        :param df: resulting dataframe of a task with result regarding trial
        :return: an array with the success rate regarding no_trial for the data of the considered dataframe
        """
        success = [np.mean(df["result"][:n]) * 100 for n in range(1, len(df['result']) + 1)]
        return np.array(success)

    def total_people(self, mental_disorder=True, disorder='ocd'):
        """
        :param mental_disorder : False, if you want the entire data, True otherwise
        :param disorder: the specific disorder you which to look at between the list_disorder (default= 'ocd')
        :return: the number of people suffering from the disorder selected in our data regarding the redcap csv
        """
        if not mental_disorder:
            return self.get_list_patients('all')[1][self.get_list_patients(disorder)[1] == 0]
        else:
            return self.get_list_patients(disorder)[1][self.get_list_patients(disorder)[1] == 1]

    def stats(self, specific_type=False, type='all'):
        """
        :param specific_type : Put True if you want to look at a specific type of trials (default = False)
        :param type : The type you are interested in, change regarding tasks (default = 'all')
        :return: dataframe containing descriptive statistics of the data for every subjects
        """
        numbers_trials = self.get_no_trials(type)
        tab = []

        for df in self.df_files:
            if specific_type:
                df = df[df['no_trial'].isin(numbers_trials)]
            id = self.get_id(df)
            disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
            tab.append([id, np.mean(df['result']) * 100, np.mean(df['reaction_time']), np.max(df['reaction_time']),
                        int(disorder_id)])
        tab = pd.DataFrame(tab)
        tab.columns = ['Id', 'Success rate', 'Average reaction time', 'Maximum reaction time', 'disorder']
        return tab

    def get_no_trials(self, *args):
        """ Get the numbers of trials within a certain category
        """

    def all_success_plot(self, specific_type=False, border=False, type='all', disorder='ocd', max_len=200):
        """
        :return:
        """
        list_patients = self.get_list_patients(disorder)
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            if specific_type:
                numbers_trials = self.get_no_trials(type)
                df = df[df['no_trial'].isin(numbers_trials)]
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            if i != -1:
                tab = self.success_rate_trials(df)
                if len(tab) != max_len:
                    size = len(tab)
                    tab = np.resize(tab, (max_len))
                    tab_empty_val = np.empty(tab[size:max_len].shape)
                    tab_empty_val = tab_empty_val.fill(np.nan)
                    tab[size:max_len] = tab_empty_val
                if i == 0:
                    HC_group.append(tab)
                else:
                    disorder_group.append(tab)
        if border:
            list_group = [HC_group, disorder_group]
            for i in range(2):
                plt.plot(np.nanmin(list_group[i], axis=0), self.col[i], alpha=0.25)
                plt.plot(np.nanmax(list_group[i], axis=0), self.col[i], alpha=0.25)
                plt.fill_between(np.arange(0, 100), np.nanmin(list_group[i], axis=0),
                                 np.nanmax(list_group[i], axis=0),
                                 color=self.col[i], alpha=0.25)
        sns.lineplot(data=np.nanmean(HC_group, axis=0), color=self.col[0])
        sns.lineplot(data=np.nanmean(disorder_group, axis=0), color=self.col[1])

    def plot_pourcentage(self, *args):
        """ Create a graph representing success rate depending on the number of trials
            """

    def boxplot_average(self, category='success_rate', *args):
        """
        :param category: the category of the output of stats that you want to see
        :return: a boxplot and a barplot of the average success result of a certain category (choose among the columns
        of the output of stats()
        """

    def group_comparison(self, specific_type=False, type='all', category='success_rate', disorder='ocd'):
        """" Student test for considered criteria
        :param specific_type : Put True if you want to look at a specific type of trials (default = False)
        :param type : The type you are interested in, change regarding tasks (default = 'ocd')
        :param category: the category of the output of stats that you want to see
        :param disorder: The disorder you want to compare with control group
        """
        X = self.stats(specific_type=specific_type, type=type)
        X1 = np.array(X[X.disorder == 0][category])
        X2 = np.array(X[X.disorder == self.list_disorder.index(disorder)][category])
        if specific_type:
            print(f'Pour le test de student sur la catégorie {category} entre les sujets sains et les sujets {disorder}'
                  f' pour le type {type} , on obtient une p-value de ', sps.ttest_ind(X1, X2)[1])
        else:
            print(f'Pour le test de student sur la catégorie {category} entre les sujets sains et les sujets {disorder}'
                  f' , on obtient une p-value de ', sps.ttest_ind(X1, X2)[1])

        if sps.ttest_ind(X1, X2)[1] > 0.05:
            print("Il n'y a pas de différence significative entre les deux groupes comparés")
        else:
            print("Il y a une différence significative entre les deux groupes comparés")
