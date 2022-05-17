from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np

class symmetry(Template_Task_Statistics):

    def plot_pourcentage(self, mental_disorder=True, disorder='all'):
        """
        """
        col = ['black', 'red']
        plt.figure()
        plt.title(f'Success rate for the task symmetry regarding trials ')
        for (df, i) in zip(self.df_files, self.get_list_patients(disorder)):
            tab = self.success_rate_trials(df)
            if mental_disorder:
                plt.plot(tab, color=col[i])
            else:
                plt.plot(tab, color='k')
        plt.legend(['no-disorder', disorder])
        plt.show()