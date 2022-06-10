from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class symmetry_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/symmetry'

    def plot_pourcentage(self, disorder='ocd', border=False):
        """
        :param disorder: the disorder you are interested in
        """

        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Symmetry Task')
        self.all_success_plot(disorder='ocd', border=border, max_len=100)
        plt.legend(self.custom_lines,
                   [f'Healthy Control', f'{self.list_graph_name[self.list_disorder.index(disorder)]}'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def boxplot_average(self, category='Success rate', disorder='ocd'):
        my_pal = {"Healthy Control": self.col[0],
                  f'{self.list_graph_name[self.list_disorder.index(disorder)]}': self.col[1]}
        stats = self.stats()

        if disorder == 'all':
            tab = [stats[stats['disorder'] == 0][category], stats[stats['disorder'] != 0][
                category]]
        else:
            tab = [stats[stats['disorder'] == 0][category],
                   stats[stats['disorder'] == self.list_disorder.index(disorder)][
                       category]]
        success = pd.DataFrame({"Healthy Control": tab[0],
                                f'{self.list_graph_name[self.list_disorder.index(disorder)]}': tab[1]
                                })

        plt.figure()
        plt.title(f'{category} for Symmetry Task')
        sns.boxplot(data=success, palette=my_pal)
        if category == 'Success rate':
            plt.ylabel(f'{category} (%)')
        else:
            plt.ylabel(f'{category}')
        plt.show()
