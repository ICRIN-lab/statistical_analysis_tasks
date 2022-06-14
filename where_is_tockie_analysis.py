import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class where_is_tockie_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/where_is_tockie'

    def stats(self, type='all'):
        tab = []
        for df in self.df_files:
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
            count_tot = np.array([np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)])
            count_tot = count_tot[~np.isnan(count_tot)]
            tab.append([id, np.mean(df['result']) * 100, np.mean(df['reaction_time']), np.max(df['reaction_time']),
                        np.mean(count_tot), np.max(count_tot), np.min(count_tot),
                        np.mean(df['result']) * 100 / np.mean(count_tot), int(disorder_id)])
        tab = pd.DataFrame(tab)
        tab.columns = ['Id', 'Success rate', 'Average reaction time', 'Maximum reaction time', 'Average count image',
                       'Maximum count image', 'Minimum count image', 'Success/count image', 'disorder']
        return tab

    def plot_pourcentage(self, disorder='ocd', border=False, save_fig=False):
        """ Create a graph representing success rate depending on the number of trials
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param border: True, if you want margins of the result for each group, False otherwise (default = False)
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """

        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Where Is Tockie Task')
        self.all_success_plot(disorder='ocd', border=border, max_len=200, type='all')
        plt.legend(self.custom_lines,
                   [f'Healthy Control (n={self.total_people(disorder)[0]})',
                    f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)[1]})'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        if save_fig:
            plt.savefig(f'Success rate_number trials Where is tockie Task.png')
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
        plt.title(f'{category} for Where Is Tockie Task')
        if category == 'Success/count image':
            category = 'Success regarding the average count of image'
        sns.boxplot(data=success, palette=my_pal)
        if category == 'Success rate':
            plt.ylabel(f'{category} (%)')
        else:
            plt.ylabel(f'{category}')
        if save_fig:
            plt.savefig(f'Boxplot: {category} for Where Is Tockie Task.png')
        plt.show()

    def count_image_analysis(self, disorder='ocd'):
        """ More results regarding the variable count_image _ in progress
    """
        HC_count = []
        disorder_count = []
        for df in self.df_files:
            count_tot = np.array([np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)])
            count_tot = count_tot[~np.isnan(count_tot)]
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
            if int(disorder_id) == 0:
                HC_count.append(count_tot)
            if disorder == 'all' and int(disorder_id) != 0:
                disorder_count.append(count_tot)
            if disorder != 'all' and int(disorder_id) == self.get_disorder_stats(disorder):
                disorder_count.append(count_tot)
        return count_tot

    def count_image_plot(self, disorder='ocd'):
        plt.plot(np.sort(self.get_disorder_stats('none')['Average count image'])[0:9],
                 np.sort(self.get_disorder_stats(disorder)['Average count image']))
        plt.show()
