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
        self.all_success_plot(disorder='ocd',border=border, max_len=100)
        plt.legend(self.custom_lines,[f'Healthy Control', f'{self.list_graph_name[self.list_disorder.index(disorder)]}'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def boxplot_average(self, category='success_rate', disorder='ocd'):
        stats = self.stats()
        if disorder == 'all':
            success = pd.DataFrame({"Healthy Control": stats[stats['disorder'] == 0][category],
                                    disorder: stats[stats['disorder'] != 0][
                                        category]})
            mean_success = success.apply(np.mean, axis=0)
        else:
            success = pd.DataFrame({"Healthy Control": stats[stats['disorder'] == 0][category],
                                    disorder: stats[stats['disorder'] == self.list_disorder.index(disorder)][
                                        category]})
            mean_success = [np.mean(stats[stats['disorder'] == 0][category]),
                            np.mean(stats[stats['disorder'] == self.list_disorder.index(disorder)][category])]
        plt.figure()
        success[["Healthy Control", disorder]].plot(kind='box', title=f'Boxplot of {category} for the task symmetry')
        plt.ylabel(f'{category}')
        plt.show()

        plt.figure()
        plt.title(f'Comparaison of {category} for the task symmetry')
        plt.bar(range(len(mean_success)), mean_success, color=self.col)
        plt.xticks(range(len(mean_success)), ["Healthy Control", disorder])
        plt.ylabel(f'{category}')
        plt.show()


s = symmetry_analysis()
s.plot_pourcentage(border=True)
