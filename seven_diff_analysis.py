from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class seven_diff_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/seven_diff'

    def get_no_trials(self, block='all'):
        if block == 'all':
            numbers_trials = np.arange(0, 201)
        elif block == 'shocking':
            numbers_trials = np.arange(0, 50)
        elif block == 'non-shocking':
            numbers_trials = np.arange(51, 101)
        elif block == 'calligraphy':
            numbers_trials = np.arange(101, 151)
        elif block == 'chess':
            numbers_trials = np.arange(151, 201)
        return numbers_trials

    def success_rate_trials(self, df):
        """ Get the success_rate regarding trials from the column result of the dataframe"""
        diff = abs(df['ans_candidate'] - df['good_ans'])
        condlist = [diff == 0, diff == 1, diff == 4, diff == 5, diff == 6]
        choicelist = [1, 2 / 3, 2 / 3, 1 / 3, 0]
        resultat = np.select(condlist, choicelist)
        success = [np.mean(resultat[:n]) * 100 for n in range(1, len(resultat) + 1)]
        return np.array(success)

    def plot_pourcentage(self, disorder='ocd', block="all", border=False):
        """
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param block: the block of images you are interested in between all, shocking, non-shocking, calligraphy and chess
        """
        if block != "all":
            specific_type = True
        else:
            specific_type = False

        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Seven Differences Task')
        plt.title(f'(Block = {block})', fontsize=10)
        self.all_success_plot(disorder='ocd', specific_type=specific_type, type=block, border=border, max_len=200)
        plt.legend(self.custom_lines,
                   [f'Healthy Control', f'{self.list_graph_name[self.list_disorder.index(disorder)]}'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def boxplot_average(self, category='success_rate', disorder='ocd', block="all"):
        """
            :param disorder:
            :param category:
            :param block: the type or image you are interested between all, various, calligraphy and chess
            """
        if block != 'all':
            stats = self.stats(specific_type=True, type=block)
        else:
            stats = self.stats()

        success = pd.DataFrame({"Healthy Control": stats[stats['disorder'] == 0][category],
                                disorder: stats[stats['disorder'] == self.list_disorder.index(disorder)][
                                    category]})
        mean_success = success.apply(np.mean, axis=0)
        # mean_success = [np.mean(stats[stats['disorder'] == 0][category]),
        #                np.mean(stats[stats['disorder'] == self.list_disorder.index(disorder)][category])]

        plt.figure()
        success[["Healthy Control", disorder]].plot(kind='box', title=f'Boxplot of {category} '
                                                                      f'for the task seven diff (part = {block})')
        plt.ylabel(f'{category}')
        plt.tight_layout()
        plt.show()

        plt.figure()
        plt.title(f'Comparaison of {category} for the task seven diff (block = {block})')
        plt.bar(range(len(mean_success)), mean_success, color=self.col)
        plt.xticks(range(len(mean_success)), ["Healthy Control", disorder])
        plt.ylabel(f'{category}')
        plt.tight_layout()
        plt.show()
