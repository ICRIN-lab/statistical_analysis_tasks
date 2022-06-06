from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class seven_diff_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/seven_diff'

    def get_no_trials(self, type_image='all'):
        if type_image == 'all':
            numbers_trials = np.arange(0, 201)
        elif type_image == 'various':
            numbers_trials = np.arange(0, 101)
        elif type_image == 'calligraphy':
            numbers_trials = np.arange(101, 151)
        elif type_image == 'chess':
            numbers_trials = np.arange(151, 201)
        return numbers_trials

    def plot_pourcentage(self, mental_disorder=True, disorder='ocd', type_image="all"):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param type_image: the type or image you are interested between all, various, calligraphy and chess
        """
        custom_lines = [plt.Line2D([0], [0], color=self.col[0], lw=4), plt.Line2D([0], [0], color=self.col[1], lw=4)]
        list_patients = self.get_list_patients(disorder)

        plt.figure()
        plt.title(f'Success rate for the task seven diff regarding trials (part = {type_image})')
        numbers_trials = self.get_no_trials(type_image)
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            df = df[df['no_trial'].isin(numbers_trials)]
            if i != -1:
                tab = self.success_rate_trials(df)
                if len(tab) != 200:
                    size = len(tab)
                    tab =np.resize(tab,(200))
                    tab_empty_val =np.empty(tab[size:200].shape)
                    tab_empty_val = tab_empty_val.fill(np.nan)
                    tab[size:200] = tab_empty_val
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
        plt.tight_layout()
        plt.show()

    def boxplot_average(self, category='success_rate', disorder='ocd', type_image="all"):
        """
        :param disorder:
        :param category:
        :param type_image: the type or image you are interested between all, various, calligraphy and chess
        """
        if type_image != 'all':
            stats = self.stats(specific_type=True, type=type_image)
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
                                                                  f'for the task seven diff (part = {type_image})')
        plt.ylabel(f'{category}')
        plt.tight_layout()
        plt.show()

        plt.figure()
        plt.title(f'Comparaison of {category} for the task seven diff (part = {type_image})')
        plt.bar(range(len(mean_success)), mean_success, color=self.col)
        plt.xticks(range(len(mean_success)), ["Healthy Control", disorder])
        plt.ylabel(f'{category}')
        plt.tight_layout()
        plt.show()


a=seven_diff_analysis()
a.plot_pourcentage()
