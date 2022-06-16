from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class seven_diff_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/seven_diff'
    csv_block_shocking = pd.read_csv('../statistical_analysis_tasks/other/csv_block_shocking.csv')

    def get_no_trials(self, block='all'):
        """
        :param block: The block of image you are interested in, between all, shocking, non-shocking, calligraphy and
        chess
        :return: numbers of corresponding trials
        """
        if block == 'all':
            numbers_trials = np.arange(0, 201)
        elif block == 'shocking' or block == 'non-shocking':
            numbers_trials = self.csv_block_shocking[self.csv_block_shocking['type'] == block]['no_trial']
        elif block == 'calligraphy':
            numbers_trials = np.arange(101, 151)
        elif block == 'chess':
            numbers_trials = np.arange(151, 201)
        return numbers_trials

    def success_rate_trials(self, df):
        diff = abs(df['ans_candidate'] - df['good_ans'])
        condlist = [diff == 0, diff == 1, diff == 4, diff == 5, diff == 6]
        choicelist = [1, 2 / 3, 2 / 3, 1 / 3, 0]
        resultat = np.select(condlist, choicelist)
        success = [np.mean(resultat[:n]) * 100 for n in range(1, len(resultat) + 1)]
        return np.array(success)

    def stats(self, type='all',save_tab=False, title='stats_seven_diff'):
        """

        :param type : The type you are interested in, change regarding tasks (default = 'all')
        :return: dataframe containing descriptive statistics of the data for every subjects
        """
        numbers_trials = self.get_no_trials(type)
        tab = []
        choicelist = [0, 1, 2, 3]
        for df in self.df_files:
            if type != 'all':
                df = df[df['no_trial'].isin(numbers_trials)]
            ans = df['ans_candidate']
            condlist = [ans == 0, ans == 1, ans == 5, ans == 6]
            res = np.select(condlist, choicelist)
            id = self.get_id(df)
            disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
            tab.append([id, np.mean(df['result']) * 100, np.mean(df['reaction_time']), np.max(df['reaction_time']),
                        np.mean(res), int(disorder_id)])

        tab = pd.DataFrame(tab)
        tab.columns = ['Id', 'Success rate', 'Average reaction time', 'Maximum reaction time', 'Average difference',
                       'disorder']
        if save_tab:
            tab.to_csv(title)
        return tab

    def plot_pourcentage(self, disorder='ocd', block="all", border=False, save_fig=False):
        """ Create a graph representing success rate depending on the number of trials
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param block: the block of images you are interested in between all, shocking, non-shocking, calligraphy and chess
        :param border: True, if you want margins of the result for each group, False otherwise (default = False)
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """
        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Seven Differences Task')
        plt.title(f'(Block = {block})', fontsize=10)
        self.all_success_plot(disorder='ocd', type=block, border=border, max_len=200)
        plt.legend(self.custom_lines,
                   [f'Healthy Control (n={self.total_people(disorder)[0]})',
                    f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)[1]})'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        if save_fig:
            print('Done')
            plt.savefig(f'Success rate_number trials Seven Differences Task (Block = {block}).jpg')
        plt.show()

    def boxplot_average(self, category='Success rate', disorder='ocd', block='all', save_fig=False):
        """Create boxplot of the average result from a specific category for HC group and considered disorder group
        :param category: the category of the output of stats that you want to see
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param block: the block of images you are interested in between all, shocking, non-shocking, calligraphy and chess
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
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
        if save_fig:
            plt.savefig(f'Boxplot :{category} for Seven Differences Task (Block = {block}).png')
        plt.show()

    def average_diff(self):
        df = self.df_files[0]
        good_ans = df['good_ans']
        condlist = [good_ans == 0, good_ans == 1, good_ans == 5, good_ans == 6]
        choicelist = [0, 1, 2, 3]
        df['good_ans'] = np.select(condlist, choicelist)
        return np.mean(df['good_ans'])


    def plot_reaction_time(self,type='all',disorder='ocd',border=False,max_len=200):
        list_patients = self.get_list_patients(disorder)
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            if type != 'all':
                numbers_trials = self.get_no_trials(type)
                df = df[df['no_trial'].isin(numbers_trials)]
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            if i != -1:
                tab = df['reaction_time']
                if len(tab) != max_len:
                    size = len(tab)
                    tab = np.resize(tab, max_len)
                    tab_empty_val = np.empty(tab[size:max_len].shape)
                    tab_empty_val = tab_empty_val.fill(np.nan)
                    tab[size:max_len] = tab_empty_val
                if i == 0:
                    HC_group.append(tab)
                else:
                    disorder_group.append(tab)
        if border:
            list_group = [HC_group, disorder_group]
            for i in range(2):
                plt.plot(np.nanmin(list_group[i], axis=0), self.col[i], alpha=0.25)
                plt.plot(np.nanmax(list_group[i], axis=0), self.col[i], alpha=0.25)
                plt.fill_between(np.arange(0, max_len), np.nanmin(list_group[i], axis=0),
                                 np.nanmax(list_group[i], axis=0),
                                 color=self.col[i], alpha=0.25)
        sns.lineplot(data=np.nanmean(HC_group, axis=0), color=self.col[0])
        sns.lineplot(data=np.nanmean(disorder_group, axis=0), color=self.col[1])
        plt.show()


