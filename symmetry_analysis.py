from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np

class symmetry(Template_Task_Statistics):
    path = '../symmetry/csv'

    def plot_pourcentage(self, mental_disorder=True, disorder='all'):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in
        """
        col = ['black', 'red']
        list_patients = self.get_list_patients(disorder)
        plt.figure()
        plt.title(f'Success rate for the task symmetry regarding trials')
        for df in self.df_files:
            id = str(df['id_candidate'][10])[8:11]
            i = list_patients[list_patients[0, :] == id][1]
            if i != -1:
                tab = self.success_rate_trials(df)
                if mental_disorder:
                    plt.plot(tab, color=col[i])
                else:
                    plt.plot(tab, color='k')
            if mental_disorder:
                plt.legend(['no-disorder', disorder])
        plt.show()
