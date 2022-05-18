from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class seven_diff(Template_Task_Statistics):
    path = '../seven_diff/csv'

    def plot_pourcentage(self, mental_disorder=True, disorder='all', type_image="all"):
        """
        """
        col = ['black', 'red']
        if type_image == 'all':
            lim = np.array([-1, 202])
        if type_image == 'various':
            lim = np.array([0, 100])
        if type_image == 'calligraphy':
            lim = np.array([101, 150])
        if type_image == 'chess':
            lim = np.array([151, 200])

        list_patients = self.get_list_patients(disorder)
        plt.figure()
        plt.title(f'Success rate for the task seven diff regarding trials (part = {type_image})')
        for df in self.df_files:
            id = str(df['id_candidate'][10])[8:11]
            i = list_patients[list_patients[1, :] == id][2]
            if i != 1:
                tab = self.success_rate_trials(df)
                if mental_disorder:
                    plt.plot(tab, color=col[i])
                else:
                    plt.plot(tab, color='k')
            if mental_disorder:
                plt.legend(['no-disorder', disorder])
        plt.xlim(lim[0], lim[1])
        plt.show()
