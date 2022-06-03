import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np


class where_is_tockie_analysis(Template_Task_Statistics):
    path = '../get_csv_cog_tasks/all_csv/where_is_tockie'

    def stats(self,specific_type=False, type='all'):
        tab = []
        for df in self.df_files:
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
            count_tot = [np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)]
            tab.append([id, np.mean(df['result']) * 100, np.mean(df['reaction_time']), np.max(df['reaction_time']),
                        np.mean(count_tot), np.max(count_tot), np.min(count_tot),
                        np.mean(df['result']) * 100 / np.mean(count_tot), int(disorder_id)])
        tab = pd.DataFrame(tab)
        tab.columns = ['Id', 'success_rate', 'average_reaction_time', 'maximum_reaction_time', 'average_count_image',
                       'maximum_count_image', 'minimum_count_image', 'success/average_count_image', 'disorder']
        return tab

    def plot_pourcentage(self, mental_disorder=True, disorder='ocd'):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in
        """
        custom_lines = [plt.Line2D([0], [0], color=self.col[0], lw=4), plt.Line2D([0], [0], color=self.col[1], lw=4)]
        list_patients = self.get_list_patients(disorder)
        n1 = 0
        n2 = 0
        plt.figure()
        plt.title(f'Success rate for the task where is tockie regarding trials')
        for df in self.df_files:
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            if i != -1:
                tab = self.success_rate_trials(df)
                if mental_disorder:
                    plt.plot(tab, color=self.col[i])
                    if i == 0:
                        n1 += 1
                    else:
                        n2 += 1
                else:
                    plt.plot(tab, color='k')
            if mental_disorder:
                plt.legend(custom_lines, ["Healthy Control", disorder])
        plt.ylabel('success rate')
        plt.xlabel('number of trials')
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
        success[["Healthy Control", disorder]].plot(kind='box', title=f'Boxplot of {category} for the task where is tockie')
        plt.ylabel(f'{category}')
        plt.show()

        plt.figure()
        plt.title(f'Comparison of {category} for the task where is tockie')
        plt.bar(range(len(mean_success)), mean_success, color=self.col)
        plt.xticks(range(len(mean_success)), ["Healthy Control", disorder])
        plt.ylabel(f'{category}')
        plt.show()

    def count_image_analysis(self):
        """ More results regarding the variable count_image
    """

