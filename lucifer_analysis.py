import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np


class lucifer_analysis(Template_Task_Statistics):
    csv_type_lucifer = pd.read_csv('csv_type_lucifer.csv')
    path = '../get_csv_cog_tasks/all_csv/lucifer'

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
        custom_lines = [plt.Line2D([0], [0], color='black', lw=4), plt.Line2D([0], [0], color='red', lw=4)]
        list_patients = self.get_list_patients(disorder)
        plt.figure()
        plt.title(f'Success rate for the task lucifer regarding trials (type_lucifer = {type_lucifer})')
        for df in self.df_files:
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            i = int(list_patients[list_patients[0] == id][1])
            if i != -1:
                tab = self.success_rate_trials(df)
                if mental_disorder:
                    plt.plot(tab, color=col[i])
                else:
                    plt.plot(tab, color='k')
            if mental_disorder:
                plt.legend(custom_lines,['no-disorder', disorder])
        plt.show()