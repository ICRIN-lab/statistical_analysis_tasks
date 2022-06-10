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
        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Seven Differences Task')
        plt.title(f'(Block = {block})', fontsize=10)
        self.all_success_plot(disorder='ocd', type=block, border=border, max_len=200)
        plt.legend(self.custom_lines,
                   [f'Healthy Control', f'{self.list_graph_name[self.list_disorder.index(disorder)]}'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def boxplot_average(self, category='Success rate', disorder='ocd', block="all"):
        """
            :param disorder:
            :param category:
            :param block: the type or image you are interested between all, various, calligraphy and chess
            """
        if block != 'all':
            stats = self.stats(type=block)
        else:
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

        my_pal = {"Healthy Control": self.col[0],
                  f'{self.list_graph_name[self.list_disorder.index(disorder)]}': self.col[1]}
        plt.figure()
        plt.suptitle(f'{category} for Seven Differences Task')
        plt.title(f'(Block = {block})', fontsize=10)
        sns.boxplot(data=success, palette=my_pal)
        if category == 'Success rate':
            plt.ylabel(f'{category} (%)')
        else:
            plt.ylabel(f'{category}')
        plt.show()

s=seven_diff_analysis()
print(s.df_files[0])