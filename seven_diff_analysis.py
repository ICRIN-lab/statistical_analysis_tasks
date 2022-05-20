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
        for df in self.df_files:
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            i= int(list_patients[list_patients[0] == id][1])
            if i != -1:
                tab = self.success_rate_trials(df)
                if mental_disorder:
                    plt.plot(tab, color=col[i])
                else:
                    plt.plot(tab, color='k')
            if mental_disorder:
                plt.legend(custom_lines, ['no-disorder', disorder])
        plt.xlim(lim[0], lim[1])
        plt.show()

    def boxplot_reaction_time(self, disorder='all', type_image="all"):
        """
        :param type_image: the type or image you are interested between all, various, calligraphy and chess
        """

        success = pd.DataFrame({"No_disorder": self.stats()['disorder_id' == 0]['success_rate'], disorder:
            self.stats()['disorder_id' == self.list_disorder.index(disorder)][
                'success_rate']})
        mean_success = success.apply(np.mean, axis=1)
        plt.figure()
        success[['No_disorder', disorder]].plot(kind='box', title=f'Comparaison of success rate for {disorder}')
        plt.show()
        # plt.boxplot(success)
        plt.figure()
        plt.bar(mean_success)
        plt.show()


a = seven_diff_analysis()
print(a.plot_pourcentage(disorder='toc', type_image='various'))
