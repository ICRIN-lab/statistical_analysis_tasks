import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np


class where_is_tockie_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/where_is_tockie'

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

    def plot_pourcentage(self, mental_disorder=True, disorder='ocd',border=False):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in
        """
        custom_lines = [plt.Line2D([0], [0], color=self.col[0], lw=4), plt.Line2D([0], [0], color=self.col[1], lw=4)]
        list_patients = self.get_list_patients(disorder)
        plt.figure()
        plt.title(f'Success rate for the task where is tockie regarding trials')
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            if i != -1:
                tab = self.success_rate_trials(df)
                if len(tab) != 300:
                    size = len(tab)
                    tab = np.resize(tab, (300))
                    tab_empty_val = np.empty(tab[size:300].shape)
                    tab_empty_val = tab_empty_val.fill(np.nan)
                    tab[size:300] = tab_empty_val
                if i == 0:
                    HC_group.append(tab)
                else:
                    disorder_group.append(tab)

        mean_HC_group = np.nanmean(HC_group, axis=0)
        mean_dis_group = np.nanmean(disorder_group, axis=0)
        if mental_disorder:
            plt.legend(custom_lines, [f'Healthy Control', f'{disorder} ']).get_frame().set_alpha(0)
        plt.plot(mean_HC_group, color=self.col[0])
        plt.plot(mean_dis_group, color=self.col[1])
        if border ==True:
            min_HC_group = np.nanmin(HC_group, axis=0)
            max_HC_group = np.nanmax(HC_group, axis=0)
            min_disorder= np.nanmin(disorder_group, axis=0)
            max_disorder = np.nanmax(disorder_group, axis=0)
            plt.plot(max_disorder,color='grey',alpha=0.25)
            plt.plot(min_disorder,color='grey',alpha=0.25)
            plt.plot(min_HC_group, color='cyan',alpha=0.25)
            plt.plot(max_HC_group, color='cyan',alpha=0.25)
            plt.fill_between(np.arange(0, len(min_HC_group)), min_HC_group, max_HC_group, color='steelblue',alpha=0.25)
            plt.fill_between(np.arange(0, len(min_disorder)), min_disorder, max_disorder, color='grey',alpha=0.25)
        plt.grid(True)
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

w=where_is_tockie_analysis()
