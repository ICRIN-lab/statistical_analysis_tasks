from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class symmetry_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/symmetry'

    def stats(self, type='all', save_tab=False):
        tab = self.base_stats()
        if save_tab:
            tab.to_csv('../statistical_analysis_tasks/stats_jpg/symmetry/stats_symmetry.csv',index=False)
        return tab

    def plot_pourcentage(self, disorder='ocd', border=False, save_fig=False):
        """ Create a graph representing success rate depending on the number of trials
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param border: True, if you want margins of the result for each group, False otherwise (default = False)
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """
        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Symmetry Task')
        self.all_success_plot(disorder='ocd', border=border, max_len=100, type='all')
        plt.legend(self.custom_lines,
                   [f"Healthy Control (n={self.total_people('none')})", f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)})'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        if save_fig:
            plt.savefig(f'../statistical_analysis_tasks/stats_jpg/symmetry/Success_rate_trials_symmetry.png')
        plt.show()

    def boxplot_average(self, category='Success rate', disorder='ocd', save_fig=False):
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

