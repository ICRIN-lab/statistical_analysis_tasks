from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class symmetry_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/symmetry'

    def plot_pourcentage(self, mental_disorder=True, disorder='ocd'):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in
        """
        labels = ["Healthy Control", disorder]
        custom_lines = [plt.Line2D([0], [0], color=self.col[0], lw=4), plt.Line2D([0], [0], color=self.col[1], lw=4)]
        list_patients = self.get_list_patients(disorder)
        n1 = 0
        n2 = 0
        plt.figure()
        plt.title(f'Success rate for the task symmetry regarding trials')
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
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
        plt.plot(mean_HC_group, color=self.col[0])
        plt.plot(mean_dis_group, color=self.col[1])
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
        success[["Healthy Control", disorder]].plot(kind='box', title=f'Boxplot of {category} for the task symmetry')
        plt.ylabel(f'{category}')
        plt.show()

        plt.figure()
        plt.title(f'Comparaison of {category} for the task symmetry')
        plt.bar(range(len(mean_success)), mean_success, color=self.col)
        plt.xticks(range(len(mean_success)), ["Healthy Control", disorder])
        plt.ylabel(f'{category}')
        plt.show()


s=symmetry_analysis()
s.plot_pourcentage()