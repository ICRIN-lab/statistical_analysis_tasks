import pandas as pd

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np

csv_type_lucifer = pd.read_csv('csv_type_lucifer.csv')


class lucifer_analysis(Template_Task_Statistics):
    csv_type_lucifer = csv_type_lucifer
    path = '../data_ocd_metacognition/tasks_data/lucifer'

    def get_no_trials(self, type='all'):
        if type == 'all':
            return self.csv_type_lucifer['no_trial']
        else:
            return self.csv_type_lucifer[self.csv_type_lucifer['type'] == type]['no_trial']

    def plot_pourcentage(self, mental_disorder=True, disorder='ocd', type_lucifer='all', group='all', border=False):
        """
        :param mental_disorder:
        :param disorder:
        :param type_lucifer: the arrangement of lucifer you are interested in , between all, straight, messy and special
        :return:
        """
        custom_lines = [plt.Line2D([0], [0], color=self.col[0], lw=4), plt.Line2D([0], [0], color=self.col[1], lw=4)]
        list_patients = self.get_list_patients(disorder)
        plt.figure()
        numbers_trials = self.get_no_trials(type_lucifer)
        plt.title(f'Success rate for the task lucifer regarding trials (type_lucifer = {type_lucifer})')
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            df = df[df['no_trial'].isin(numbers_trials)]
            if i != -1:
                tab = self.success_rate_trials(df)
                if len(tab) != 100:
                    size = len(tab)
                    tab = np.resize(tab, (100))
                    tab_empty_val = np.empty(tab[size:100].shape)
                    tab_empty_val = tab_empty_val.fill(np.nan)
                    tab[size:100] = tab_empty_val
                if i == 0:
                    HC_group.append(tab)
                else:
                    disorder_group.append(tab)
        mean_HC_group = np.nanmean(HC_group, axis=0)
        mean_dis_group = np.nanmean(disorder_group, axis=0)

        if mental_disorder:
            plt.legend(custom_lines, [f'Healthy Control (n=)', f'{disorder} (n=)'])
        if border == True:
            min_HC_group = np.nanmin(HC_group, axis=0)
            max_HC_group = np.nanmax(HC_group, axis=0)
            min_disorder = np.nanmin(disorder_group, axis=0)
            max_disorder = np.nanmax(disorder_group, axis=0)
            plt.plot(max_disorder, color='grey', alpha=0.25)
            plt.plot(min_disorder, color='grey', alpha=0.25)
            plt.plot(min_HC_group, color='cyan', alpha=0.25)
            plt.plot(max_HC_group, color='cyan', alpha=0.25)
            plt.fill_between(np.arange(0, 100), min_HC_group, max_HC_group, color='steelblue', alpha=0.25)
            plt.fill_between(np.arange(0, 100), min_disorder, max_disorder, color='grey', alpha=0.25)
        plt.plot(mean_HC_group, color=self.col[0])
        plt.plot(mean_dis_group, color=self.col[1])
        plt.ylabel('success rate')
        plt.xlabel('number of trials')
        plt.show()

    def boxplot_average(self, category='success_rate', disorder='ocd', type_lucifer='all'):
        if type_lucifer != 'all':
            stats = self.stats(specific_type=True, type=type_lucifer)
        else:
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
        success[["Healthy Control", disorder]].plot(kind='box', title=f'Boxplot of {category} '
                                                                      f'for the task lucifer (type_lucifer = {type_lucifer})')
        plt.ylabel(f'{category}')
        plt.show()

        plt.figure()
        plt.title(f'Comparaison of {category} for the task lucifer (type_lucifer = {type_lucifer})')
        plt.bar(range(len(mean_success)), mean_success, color=self.col)
        plt.xticks(range(len(mean_success)), ["Healthy Control", disorder])
        plt.ylabel(f'{category}')
        plt.show()

    def scatter_pourcentage(self, category='success_rate', disorder='ocd', type_lucifer='all'):
        if type_lucifer != 'all':
            stats = self.stats(specific_type=True, type=type_lucifer)
        else:
            stats = self.stats()
        stats1 = stats[stats.disorder == 1]
        plt.scatter(np.arange(0, len(stats1[category])), stats1[category], color=self.col[1])
        stats2 = stats[stats.disorder == 0]
        plt.scatter(np.arange(0, len(stats2[category])), stats2[category], color=self.col[0])
        plt.show()


l = lucifer_analysis()
l.plot_pourcentage(border=True)
