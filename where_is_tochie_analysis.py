import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np


class where_is_tochie_analysis(Template_Task_Statistics):
    path = '../get_csv_cog_tasks/all_csv/where_is_tockie'

    def plot_pourcentage(self, mental_disorder=True, disorder='all'):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in
        """
        col = ['black', 'red']
        custom_lines = [plt.Line2D([0], [0], color='black', lw=4), plt.Line2D([0], [0], color='red', lw=4)]
        list_patients = self.get_list_patients(disorder)
        plt.figure()
        plt.title(f'Success rate for the task where is tochie regarding trials')
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
                plt.legend(custom_lines, ['no-disorder', disorder])
        plt.show()

w=where_is_tochie_analysis()
w.plot_pourcentage()