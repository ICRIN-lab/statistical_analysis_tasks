import pandas as pd
from scipy import stats

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

csv_block_lucifer = pd.read_csv('csv_block_lucifer.csv')


class LuciferAnalysis(Template_Task_Statistics):
    csv_block_lucifer = csv_block_lucifer
    path = '../data_ocd_metacognition/tasks_data/lucifer'

    def get_no_trials(self, block='all'):
        if block == 'all':
            return self.csv_block_lucifer['no_trial']
        else:
            return self.csv_block_lucifer[self.csv_block_lucifer['block'] == block]['no_trial']

    def stats(self, block='all', save_tab=True):
        tab1 = self.base_stats(block=block)
        numbers_trials = self.get_no_trials(block)
        new_column = []
        for df in self.df_files:
            group = df['group'][102]
            if block != 'all':
                df = df[df['no_trial'].isin(numbers_trials)]
            if group == 'pro':
                new_column.append(1)
            else:
                new_column.append(0)
        tab1['group'] = new_column
        if save_tab:
            tab1.to_csv(f'../statistical_analysis_tasks/stats_jpg/lucifer/stats_lucifer_{block}.csv', index=False)
        return tab1

    def plot_pourcentage(self, disorder='ocd', block_lucifer='all', border=False, save_fig=True):
        """ Create a graph representing success rate depending on the number of trials
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param block_lucifer: the arrangement of lucifer you are interested in , between all, straight, messy and special
        :param border: True, if you want margins of the result for each group, False otherwise (default = False)
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """
        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Lucifer Task')
        plt.title(f'(Lucifer Arrangement = {block_lucifer})', fontsize=10)
        self.all_success_plot(disorder='ocd', block=block_lucifer, border=border,
                              max_len=100)
        plt.legend(self.custom_lines,
                   [f"Healthy Control (n={self.total_people('none')})",
                    f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)})'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(False)
        plt.ylim(0, 100)  # change here to change the scale
        plt.tight_layout()
        if save_fig:
            plt.savefig(f'../statistical_analysis_tasks/stats_jpg/lucifer/Success_rate_trials(Lucifer Arrangement = {block_lucifer}).png')
        plt.show()

    def boxplot_average(self, category='Success rate', disorder='ocd', block_lucifer='all', save_fig=True):
        """Create boxplot of the average result from a specific category for HC group and considered disorder group
        :param category: the category of the output of stats that you want to see
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param block_lucifer: the arrangement of lucifer you are interested in , between all, straight, messy and special
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
         """
        if block_lucifer != 'all':
            stats = self.stats(block=block_lucifer)
        else:
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
        my_pal = {"Healthy Control": self.col[0],
                  f'{self.list_graph_name[self.list_disorder.index(disorder)]}': self.col[1]}
        plt.figure()
        plt.suptitle(f'{category} for Lucifer Task')
        plt.title(f'(Lucifer Arrangement = {block_lucifer})', fontsize=10)
        sns.boxplot(data=success, palette=my_pal)
        if category == 'Success rate':
            plt.ylabel(f'{category} (%)')
        else:
            plt.ylabel(f'{category}')
        if save_fig:
            plt.savefig(f'../statistical_analysis_tasks/stats_jpg/lucifer/Boxplot:{category}(block = {block_lucifer}).png')
        plt.show()

    def pourcentage_pro(self, disorder='ocd'):
        """

        """
    def average_rt(self, disorder="ocd"):
        stats_lucifer = pd.read_csv('stats_jpg/lucifer/stats_lucifer_all.csv')
        print(np.mean((stats_lucifer[stats_lucifer["disorder"] == 1]["Average reaction time"])))
        print(np.mean((stats_lucifer[stats_lucifer["disorder"] == 0]["Average reaction time"])))
        print(np.mean((stats_lucifer[stats_lucifer["disorder"] == 1]["Success rate"])))
        print(np.mean((stats_lucifer[stats_lucifer["disorder"] == 0]["Success rate"])))
        print(stats.ttest_ind(stats_lucifer[stats_lucifer["disorder"] == 0]["Average reaction time"],
                              stats_lucifer[stats_lucifer["disorder"] == 1]["Average reaction time"]))
        print(stats.ttest_ind(stats_lucifer[stats_lucifer["disorder"] == 0]["Success rate"],
              stats_lucifer[stats_lucifer["disorder"] == 1]["Success rate"]))

