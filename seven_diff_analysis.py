from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class seven_diff_analysis(Template_Task_Statistics):
    # path = '../get_csv_cog_tasks/all_csv/seven_diff'
    path = '/Users/melissamarius/Documents/all_csv_provisoire/seven_diff'

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

    def plot_pourcentage(self, mental_disorder=True, disorder='all', type_image="all"):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in
        :param type_image: the type or image you are interested between all, various, calligraphy and chess
        """
        custom_lines = [plt.Line2D([0], [0], color=self.col[0], lw=4), plt.Line2D([0], [0], color=self.col[1], lw=4)]
        list_patients = self.get_list_patients(disorder)

        plt.figure()
        plt.title(f'Success rate for the task seven diff regarding trials (part = {type_image})')
        n1 = 0
        n2 = 0
        numbers_trials = self.get_no_trials(type_image)
        for df in self.df_files:
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            df = df[df['no_trial'].isin(numbers_trials)]
            if i != -1:
                tab = pd.DataFrame(self.success_rate_trials(df))
                if mental_disorder:
                    plt.plot(tab, color=self.col[i])
                    if i == 0:
                        n1 += 1
                    else:
                        n2 += 1
                else:
                    plt.plot(tab, color='k')

            if mental_disorder:
                plt.legend(custom_lines, [f'no-disorder (n={n1})', f'{disorder} (n={n2})'])
        plt.ylabel('success rate')
        plt.xlabel('number of trials')
        plt.tight_layout()
        plt.show()

    def boxplot_average(self, category='success_rate', disorder='all', type_image="all"):
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
            success = pd.DataFrame({"No_disorder": stats[stats['disorder'] == 0][category],
                                    disorder: stats[stats['disorder'] != 0][
                                        category]})
            mean_success = success.apply(np.mean, axis=0)
        else:
            success = pd.DataFrame({"No_disorder": stats[stats['disorder'] == 0][category],
                                    disorder: stats[stats['disorder'] == self.list_disorder.index(disorder)][
                                        category]})
            mean_success = [np.mean(stats[stats['disorder'] == 0][category]),
                            np.mean(stats[stats['disorder'] == self.list_disorder.index(disorder)][category])]

        plt.figure()
        success[['No_disorder', disorder]].plot(kind='box', title=f'Boxplot of {category} '
                                                                  f'for the task seven diff (part = {type_image})')
        plt.ylabel(f'{category}')
        plt.tight_layout()
        plt.show()

        plt.figure()
        plt.title(f'Comparaison of {category} for the task seven diff (part = {type_image})')
        plt.bar(range(len(mean_success)), mean_success, color=self.col)
        plt.xticks(range(len(mean_success)), ['No-disorder', disorder])
        plt.ylabel(f'{category}')
        plt.tight_layout()
        plt.show()


a = seven_diff_analysis()

a.plot_pourcentage()
a.boxplot_average(category='average_reaction_time')
