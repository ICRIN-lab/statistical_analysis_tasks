import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

csv_type_lucifer = pd.read_csv('csv_type_lucifer.csv')


class lucifer_analysis(Template_Task_Statistics):
    csv_type_lucifer = csv_type_lucifer
    path = '../data_ocd_metacognition/tasks_data/lucifer'

    def get_no_trials(self, type='all'):
        if type == 'all':
            return self.csv_type_lucifer['no_trial']
        else:
            return self.csv_type_lucifer[self.csv_type_lucifer['type'] == type]['no_trial']

    def plot_pourcentage(self, disorder='ocd', type_lucifer='all', group='all', border=False):
        """
        :param disorder:
        :param type_lucifer: the arrangement of lucifer you are interested in , between all, straight, messy and special
        :return:
        """
        if type_lucifer != "all":
            specific_type = True
        else:
            specific_type = False

        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Lucifer Task')
        plt.title(f'(Lucifer Arrangement = {type_lucifer})', fontsize=10)
        self.all_success_plot(disorder='ocd', specific_type=specific_type, type=type_lucifer, border=border, max_len=200)
        plt.legend(self.custom_lines,
                   [f'Healthy Control', f'{self.list_graph_name[self.list_disorder.index(disorder)]}'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def boxplot_average(self, category='success_rate', disorder='ocd', type_lucifer='all'):
        if type_lucifer != 'all':
            stats = self.stats(specific_type=True, type=type_lucifer)
        else:
            stats = self.stats()
        success = pd.DataFrame({"Healthy Control": stats[stats['disorder'] == 0][category],
                                    f'{self.list_graph_name[self.list_disorder.index(disorder)]}': stats[stats['disorder'] == self.list_disorder.index(disorder)][
                                        category]})
        mean_success = [np.mean(stats[stats['disorder'] == 0][category]),
                            np.mean(stats[stats['disorder'] == self.list_disorder.index(disorder)][category])]

        plt.figure()
        sns.boxplot(data=success, palette ="PuBuGn")
        plt.ylabel(f'{category}')
        plt.show()



    def scatter_pourcentage(self, category='success_rate', disorder='ocd', type_lucifer='all'):
        if type_lucifer != 'all':
            stats = self.stats(specific_type=True, type=type_lucifer)
        else:
            stats = self.stats()
        stats1 = stats[stats.disorder == 1]
        plt.scatter(np.arange(0, len(stats1[category]), stats1[category], color=self.col[1]))
        stats2 = stats[stats.disorder == 0]
        plt.scatter(np.arange(0, len(stats2[category])), stats2[category], color=self.col[0])
        plt.grid(True)
        plt.show()


l = lucifer_analysis()
l.boxplot_average()
