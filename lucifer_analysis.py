import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
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

    def plot_pourcentage(self, disorder='ocd', type_lucifer='all', border=False, save_fig=False):
        """ Create a graph representing success rate depending on the number of trials
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param type_lucifer: the arrangement of lucifer you are interested in , between all, straight, messy and special
        :param border: True, if you want margins of the result for each group, False otherwise (default = False)
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """

        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Lucifer Task')
        plt.title(f'(Lucifer Arrangement = {type_lucifer})', fontsize=10)
        self.all_success_plot(disorder='ocd', type=type_lucifer, border=border,
                              max_len=200)
        plt.legend(self.custom_lines,
                   [f'Healthy Control (n={self.total_people(disorder)[0]})', f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)[1]})'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        if save_fig:
            plt.savefig(f'Success rate_number trials Lucifer Task (Lucifer Arrangement = {type_lucifer}).png')
        plt.show()

    def boxplot_average(self, category='Success rate', disorder='ocd', type_lucifer='all', save_fig=False):
        """Create boxplot of the average result from a specific category for HC group and considered disorder group
        :param category: the category of the output of stats that you want to see
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param type_lucifer: the arrangement of lucifer you are interested in , between all, straight, messy and special
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
         """
        if type_lucifer != 'all':
            stats = self.stats(type=type_lucifer)
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
        plt.title(f'(Lucifer Arrangement = {type_lucifer})', fontsize=10)
        sns.boxplot(data=success, palette=my_pal)
        if category == 'Success rate':
            plt.ylabel(f'{category} (%)')
        else:
            plt.ylabel(f'{category}')
        if save_fig:
            plt.savefig(f'Boxplot: {category} for Lucifer Task type = {type_lucifer}.png')
        plt.show()
