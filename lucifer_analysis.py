import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np


class lucifer(Template_Task_Statistics):
    csv_type_lucifer = pd.read_csv('csv_type_lucifer.csv')
    path = '../lucifer/csv'

    def get_no_trial(self, type_lucifer='all'):
        if type_lucifer == 'all':
            return self.csv_type_lucifer['no_trial']
        else:
            return self.csv_type_lucifer[self.csv_type_lucifer['type_lucifer'] == type_lucifer]['no_trial']

    def plot_pourcentage(self, mental_disorder=True, disorder='all', type_lucifer='all'):
        """
        :param mental_disorder:
        :param disorder:
        :param type_lucifer: the arrangement of lucifer you are interested in , between all, straight and messy
        :return:
        """
        col = ['black', 'red']
        list_patients = self.get_list_patients(disorder)
        plt.figure()
        plt.title(f'Success rate for the task lucifer regarding trials (type_lucifer = {type_lucifer})')
        for df in self.df_files:
            id = str(df['id_candidate'][10])[8:11]
            i = list_patients[list_patients[0, :] == id][1]
            df = df[df['no_trials'] == self.get_no_trial(type_lucifer)]
            if i != -1:
                tab = self.success_rate_trials(df)
                if mental_disorder:
                    plt.plot(tab, color=col[i])
                else:
                    plt.plot(tab, color='k')
            if mental_disorder:
                plt.legend(['no-disorder', disorder])
