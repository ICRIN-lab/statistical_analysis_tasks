from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class seven_diff_analysis(Template_Task_Statistics):
    path = '../get_csv_cog_tasks/all_csv/seven_diff'

    def plot_pourcentage(self, mental_disorder=True, disorder='all', type_image="all"):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in
        :param type_image: the type or image you are interested between all, various, calligraphy and chess
        """
        col = ['black', 'red']
        custom_lines = [plt.Line2D([0], [0], color='black', lw=4), plt.Line2D([0], [0], color='red', lw=4)]
        if type_image == 'all':
            lim = np.array([-1, 202])
        if type_image == 'various':
            lim = np.array([0, 100])
        if type_image == 'calligraphy':
            lim = np.array([101, 150])
        if type_image == 'chess':
            lim = np.array([151, 200])

        list_patients = self.get_list_patients(disorder)

        plt.figure()
        plt.title(f'Success rate for the task seven diff regarding trials (part = {type_image})')
        n1 = 0
        n2 = 0
        for df in self.df_files:
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            i = int(list_patients[list_patients[0] == id][1])
            if i != -1:
                tab = self.success_rate_trials(df)
                if mental_disorder:
                    plt.plot(tab, color=col[i])
                    if i == 0:
                        n1 += 1
                    else:
                        n2 += 1
                else:
                    plt.plot(tab, color='k')

            if mental_disorder:
                plt.legend(custom_lines, [f'no-disorder (n={n1})', f'{disorder} (n={n2})'])
        plt.xlim(lim[0], lim[1])
        plt.ylabel('success rate')
        plt.xlabel('number of trials')
        plt.show()

    def boxplot_average(self, category='success_rate', disorder='all', type_image="all"):
        """
        :param type_image: the type or image you are interested between all, various, calligraphy and chess
        """
        stats = self.stats()
        if disorder == 'all':
            success = pd.DataFrame({"No_disorder": stats[stats['disorder'] == 0][category],
                                    disorder: stats[stats['disorder'] != 0][
                                        category]})
            mean_success = success.apply(np.mean, axis=1)
        else:
            success = pd.DataFrame({"No_disorder": stats[stats['disorder'] == 0][category],
                                    disorder: stats[stats['disorder'] == self.list_disorder.index(disorder)][
                                        category]})
            mean_success = [np.mean(stats[stats['disorder'] == 0][category]),
                            np.mean(stats[stats['disorder'] == self.list_disorder.index(disorder)][category])]

        plt.figure()
        success[['No_disorder', disorder]].plot(kind='box', title=f'Boxplot of {category} for the task seven diff')
        plt.show()

        plt.figure()
        plt.title(f'Comparaison of {category} for the task seven diff')
        plt.bar(range(len(mean_success)), mean_success, color=['black', 'darkred'])
        plt.xticks(range(len(mean_success)), ['No-disorder', disorder])
        plt.show()


a = seven_diff_analysis()
stats = a.stats()
a.boxplot_average(category='maximum_reaction_time', disorder='toc')
