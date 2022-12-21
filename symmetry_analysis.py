from scipy.stats import stats

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


class SymmetryAnalysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/symmetry'

    def stats(self, block='all', save_tab=True):
        tab = self.base_stats()
        if save_tab:
            tab.to_csv('../statistical_analysis_tasks/stats_jpg/symmetry/stats_symmetry.csv', index=False)
        return tab

    def plot_pourcentage(self, disorder='ocd', border=False, save_fig=True):
        """ Create a graph representing success rate depending on the number of trials
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param border: True, if you want margins of the result for each group, False otherwise (default = False)
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """
        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Symmetry Task')
        self.all_success_plot(disorder='ocd', border=border, max_len=100, block='all')
        plt.legend(self.custom_lines,
                   [f"Healthy Control (n={self.total_people('none')})", f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)})'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.ylim(0, 100)  # change here to change the scale
        plt.grid(False)
        plt.tight_layout()
        if save_fig:
            plt.savefig(f'../statistical_analysis_tasks/stats_jpg/symmetry/Success_rate_trials_symmetry.png')
        plt.show()

    def test_success_rate(self, *args):
        HC_group, disorder_group = self.all_success_plot(max_len=100)
        # print(HC_group)
        # print(disorder_group)
        stats_symmetry = pd.read_csv('stats_jpg/symmetry/stats_symmetry.csv')
        print(np.mean((stats_symmetry[stats_symmetry["disorder"] == 1]["Average reaction time"])))
        print(np.mean((stats_symmetry[stats_symmetry["disorder"] == 0]["Average reaction time"])))
        print(np.mean((stats_symmetry[stats_symmetry["disorder"] == 1]["Success rate"])))
        print(np.mean((stats_symmetry[stats_symmetry["disorder"] == 0]["Success rate"])))
        print(stats.ttest_ind(stats_symmetry[stats_symmetry["disorder"] == 0]["Average reaction time"],
                              stats_symmetry[stats_symmetry["disorder"] == 1]["Average reaction time"]))
        print(stats.ttest_ind(stats_symmetry[stats_symmetry["disorder"] == 0]["Success rate"],
              stats_symmetry[stats_symmetry["disorder"] == 1]["Success rate"]))

        # print(np.mean(HC_group, axis=0), np.mean(disorder_group, axis=0))  # 86% vs 80%
        # print("t-test symmetry : ", stats.ttest_ind(HC_group, disorder_group))  # t = 20, p = 1.52e-50


    def boxplot_average(self, category='Success rate', disorder='ocd', save_fig=True):
        """Create boxplot of the average result from a specific category for HC group and considered disorder group
        :param category: the category of the output of stats that you want to see
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """
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
        if save_fig:
            plt.savefig(f'../statistical_analysis_tasks/stats_jpg/symmetry/Boxplot:{category}_Symmetry.png')
        plt.show()

