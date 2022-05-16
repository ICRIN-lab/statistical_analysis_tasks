from Task_result_summary import Task_result_summary
import matplotlib as plt
import numpy as np
import pandas as pd


class seven_diff(Task_result_summary):
    """ the type of image we want to look at either all, various, calligraphy or chess"""
    type_image = 'all'

    def plot_pourcentage(self, index_sick=[], disease='all', type_image="all"):
        """
        """
        tab = self.success_rate_trials()

        if type_image == 'various':
            tab = map(tab.__getitem__, np.arange(0, 101))
        if type_image == 'calligraphy':
            tab = map(tab.__getitem__, np.arange(101, 151))
        if type_image == 'chess':
            tab = map(tab.__getitem__, np.arange(151, 201))

        plt.figure()
        plt.title(f'Pourcentages de réussites en fonction des essais pour la tâche seven_diff')
        if disease != 'all':
            col = []
            for i in range(1,len(index_sick)):
                if i in index_sick:
                    plt.plot(tab[i], color='r', label='malade')
                else:
                    plt.plot(tab[i], color='k', label='non-malade')
        else:
            plt.plot(tab, color='k')
        plt.legend()
        plt.show()
