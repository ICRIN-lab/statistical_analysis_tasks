import pandas as pd
from scipy import stats

from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class WhereIsTockieAnalysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/where_is_tockie'

    def stats(self, block='all', save_tab=True):
        tab = []
        for df in self.df_files:
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            count_tot = np.array([np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)])
            count_tot = count_tot[~np.isnan(count_tot)]
            disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
            tab.append([id, disorder_id.iloc[0], round(float(np.mean(df['result'])) * 100, 1),
                        round(float(np.mean(df['reaction_time'])), 2),
                        float(np.max(df['reaction_time'])),
                        round(float(np.mean(count_tot)), 2), int(np.max(count_tot)), int(np.min(count_tot)),
                        round(float(np.mean(df['result'])) * 100 / float(np.mean(count_tot)), 2)])
        tab = pd.DataFrame(tab)
        tab.columns = ['Id', 'disorder', 'Success rate', 'Average reaction time', 'Maximum reaction time',
                       'Average count image',
                       'Maximum count image', 'Minimum count image', 'Success/count image']
        tab = tab.sort_values(by="Id")
        if save_tab:
            tab.to_csv('../statistical_analysis_tasks/stats_jpg/where_is_tockie/stats_where_is_tockie.csv')
        return tab

    def all_success_plot(self, border=False, block='all', disorder='ocd', max_len=63, first_try_analysis=False):
        list_patients = self.get_list_patients(disorder)
        HC_group = []
        disorder_group = []
        HC_group = []
        other_group = []
        for df in self.df_files:
            id = self.get_id(df)
            disease = list_patients[list_patients[0] == id][1].iloc[0]
            tab_patient = []
            for i in range(32):
                if first_try_analysis:
                    for j in df[(df['no_trial'] == i) & (df['count_image'] == 1)]["result"]:
                        tab_patient.append(j)
                else:
                    for j in \
                            df[(df['no_trial'] == i) & (
                                    df['count_image'] == np.max(df[df['no_trial'] == i]['count_image']))][
                                "result"]:
                        tab_patient.append(j)
            if disease == 0:
                HC_group.append(tab_patient)
            elif disease == 1:
                disorder_group.append(tab_patient)
            else:
                other_group.append(tab_patient)
        final_patient_pourc = []
        for patient in disorder_group:
            patient_pourc = []
            for i in range(len(patient)):
                patient_pourc.append(sum(patient[:i + 1]) / (len(patient[:i + 1])))
            final_patient_pourc.append(patient_pourc)

        final_hc_pourc = []
        for hc in HC_group:
            hc_pourc = []
            for i in range(len(hc)):
                hc_pourc.append(sum(hc[:i + 1]) / (len(hc[:i + 1])))
            final_hc_pourc.append(hc_pourc)

        # if you want to plot success rate per trial
        '''
        plt.plot(np.mean(HC_group, axis=0), 'royalblue', alpha=0.25)
        plt.plot(np.mean(HC_group, axis=0), 'royalblue', alpha=0.25)

        plt.plot(np.mean(disorder_group, axis=0), 'crimson', alpha=0.25)
        plt.plot(np.mean(disorder_group, axis=0), 'crimson', alpha=0.25)
        '''

        # if you want to plot success rate continuously
        plt.plot(np.mean(final_hc_pourc, axis=0) * 100, 'royalblue', alpha=0.25)
        plt.plot(np.mean(final_hc_pourc, axis=0) * 100, 'royalblue', alpha=0.25)
        plt.plot(np.mean(final_patient_pourc, axis=0) * 100, 'crimson', alpha=0.25)
        plt.plot(np.mean(final_patient_pourc, axis=0) * 100, 'crimson', alpha=0.25)
        print(np.mean(final_hc_pourc, axis=0) * 100)
        print(np.mean(final_patient_pourc, axis=0) * 100)
        print(stats.ttest_ind(np.mean(final_hc_pourc, axis=0) * 100, np.mean(final_patient_pourc, axis=0) * 100))
        return HC_group, disorder_group

    def plot_pourcentage(self, disorder='ocd', border=False, save_fig=True, first_try_analysis=False):
        """ Create a graph representing success rate depending on the number of trials
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param border: True, if you want margins of the result for each group, False otherwise (default = False)
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """

        plt.figure()
        plt.suptitle(f'WIT - Average of good final answer per trial first_try_analysis = {first_try_analysis}')
        self.all_success_plot(disorder='ocd', border=border, max_len=63, block='all',
                              first_try_analysis=first_try_analysis)
        plt.legend(self.custom_lines,
                   [f"Healthy Control (n={self.total_people('none')})",
                    f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)})'])

        plt.legend(self.custom_lines,
                   [f"Healthy Control (n=37)",
                    f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n=24)'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(False)
        plt.ylim(0, 105)  # change here to change the scale
        plt.tight_layout()
        if save_fig:
            if first_try_analysis:
                plt.savefig(
                    f'../statistical_analysis_tasks/stats_jpg/where_is_tockie/success_rate_trials_wit_first_try.png')
            else:
                plt.savefig(
                    f'../statistical_analysis_tasks/stats_jpg/where_is_tockie/success_rate_trials_wit_last_try.png')
        plt.show()

    def boxplot_average(self, category='Success rate', disorder='ocd', save_fig=True):
        """Create boxplot of the average result from a specific category for HC group and considered disorder group
        :param category: the category of the output of stats that you want to see
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
            """
        my_pal = {"Healthy Control": self.col[0],
                  f'{self.list_graph_name[self.list_disorder.index(disorder)]}': self.col[1]}
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

        plt.figure()
        plt.title(f'{category} for Where Is Tockie Task')
        if category == 'Success/count image':
            category = 'Success regarding the average count of image'
        sns.boxplot(data=success, palette=my_pal)
        if category == 'Success rate':
            plt.ylabel(f'{category} (%)')
        else:
            plt.ylabel(f'{category}')
        if save_fig:
            plt.savefig(f'../statistical_analysis_tasks/stats_jpg/where_is_tockie/Boxplot:{category}_wit_new.png')
        plt.show()

    def count_image_analysis(self, disorder='ocd'):
        """ More results regarding the variable count_image _ in progress
    """
        HC_count = []
        disorder_count = []
        for df in self.df_files:
            count_tot = np.array([np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)])
            # contient un vecteur de longueur 32 contenant le max de recheck par essai
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
            if int(disorder_id) == 0:
                HC_count.append(count_tot)
            elif disorder == 'all':
                disorder_count.append(count_tot)
            elif int(disorder_id) == self.list_disorder.index(disorder):
                disorder_count.append(count_tot)
        mean_HC = np.nanmean(HC_count, axis=0)
        mean_disorder = np.nanmean(disorder_count, axis=0)
        # print(mean_HC, mean_disorder)
        return mean_HC, mean_disorder

    def count_image_analysis_ilyass(self, disorder='ocd'):
        """ More results regarding the variable count_image _ in progress"""
        HC_count = [0] * 32
        disorder_count = [0] * 32
        other_count = [0] * 32
        for df in self.df_files:
            count_tot = np.array([np.max(df[df['no_trial'] == i]['count_image']) for i in range(0, 32)])
            # contient un vecteur de longueur 32 contenant le max de recheck par essai
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            if self.list_patients[id - 1] == 0:
                for i in range(len(HC_count)):
                    HC_count[i] = HC_count[i] + count_tot[i]
            elif self.list_patients[id - 1] == 1:
                for i in range(len(HC_count)):
                    disorder_count[i] = disorder_count[i] + count_tot[i]
            else:
                for i in range(len(HC_count)):
                    other_count[i] = other_count[i] + count_tot[i]
        for i in range(len(HC_count)):
            HC_count[i] = round(HC_count[i] / self.list_patients.count(0), 2)
            disorder_count[i] = round(disorder_count[i] / self.list_patients.count(1), 2)
            other_count[i] = round(other_count[i] / self.list_patients.count(2), 2)
            if abs(HC_count[i] - disorder_count[i]) >= 0.3:
                print(i, round(abs(HC_count[i] - disorder_count[i]),
                               2))  # check quelle image a eu bcp plus de count que les autres entre les deux groupes
        df_count = pd.DataFrame({'HC': HC_count, 'OCD': disorder_count, 'Others': other_count}, index=range(32))
        print(np.mean(df_count["HC"]))
        print(np.mean(df_count["OCD"]))
        print(stats.ttest_ind(df_count["HC"], df_count["OCD"]))
        plt.plot(HC_count, 'royalblue', alpha=0.25)
        plt.plot(disorder_count, 'crimson', alpha=0.25)
        plt.legend(self.custom_lines,
                   [f"Healthy Control (n={self.total_people('none')})",
                    f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)})'])

        plt.legend(self.custom_lines,
                   [f"Healthy Control (n=37)",
                    f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n=24)'])
        plt.ylabel('Count average')
        plt.xlabel("N trials")
        plt.grid(False)
        # plt.ylim(0, 100)  # change here to change the scale
        plt.tight_layout()
        plt.savefig(f'../statistical_analysis_tasks/stats_jpg/where_is_tockie/count_average.png')
        plt.show()
        return df_count

    def get_success(self, disorder="ocd"):
        HC_success = [0] * 32
        OCD_success = [0] * 32
        Others_success = [0] * 32

        for df in self.df_files:
            id = int(str(df['id_candidate'].tail(1).item())[8:11])
            for i in range(32):
                # print(df[df['no_trial'] == i]['count_image'])
                if np.max(df[df['no_trial'] == i]['count_image']) == 1:
                    # print(df[df['no_trial'] == i]["result"])
                    # print(np.mean(df[df['no_trial'] == i]["result"]))
                    if self.list_patients[id - 1] == 0:
                        HC_success[i] += int(np.mean(df[df['no_trial'] == i]["result"]))
                    elif self.list_patients[id - 1] == 1:
                        OCD_success[i] += int(np.mean(df[df['no_trial'] == i]["result"]))
                    else:
                        Others_success[i] += int(np.mean(df[df['no_trial'] == i]["result"]))
                else:
                    if self.list_patients[id - 1] == 0:
                        HC_success[i] += np.mean(df[df['no_trial'] == i]["result"].iloc[-(
                            int(len(df[df['no_trial'] == i]['count_image']) / (
                                np.max(df[df['no_trial'] == i]['count_image'])))):])
                    elif self.list_patients[id - 1] == 1:
                        OCD_success[i] += np.mean(df[df['no_trial'] == i]["result"].iloc[-(
                            int(len(df[df['no_trial'] == i]['count_image']) / (
                                np.max(df[df['no_trial'] == i]['count_image'])))):])
                    else:
                        Others_success[i] += np.mean(df[df['no_trial'] == i]["result"].iloc[-(
                            int(len(df[df['no_trial'] == i]['count_image']) / (
                                np.max(df[df['no_trial'] == i]['count_image'])))):])

                    # print(df[df['no_trial'] == i]["result"].iloc[-(int(len(df[df['no_trial'] == i][
                    # 'count_image'])/(np.max(df[df['no_trial'] == i]['count_image'])))):])
                    # print(np.mean(df[df['no_trial'] == i]["result"].iloc[-(int(len(df[df['no_trial'] == i]['count_image'])/(np.max(df[df['no_trial'] == i]['count_image'])))):]))
        for i in range(32):
            HC_success[i] = round(HC_success[i] / self.list_patients.count(0), 2)
            OCD_success[i] = round(OCD_success[i] / self.list_patients.count(1), 2)
            Others_success[i] = round(Others_success[i] / self.list_patients.count(2), 2)
        df_success = pd.DataFrame({'HC': HC_success, 'OCD': OCD_success, 'Others': Others_success}, index=range(32))
        # print(df_success)
        return df_success

    def count_image_plot(self, disorder='ocd', save_fig=True):
        mean_HC, mean_disorder = self.count_image_analysis(disorder)

        data = pd.DataFrame({'Average count image per trial (Healthy control)': mean_HC,
                             f'Average count image per trial ({self.list_graph_name[self.list_disorder.index(disorder)]} group)': mean_disorder})
        sns.lmplot(x='Average count image per trial (Healthy control)',
                   y='Average count image per trial '
                     f'({self.list_graph_name[self.list_disorder.index(disorder)]} group)',
                   data=data, markers='x').fig.suptitle("")
        if save_fig:
            plt.savefig('../statistical_analysis_tasks/stats_jpg/where_is_tockie/mean_count_plot.png')
        plt.show()

    def count_image_plot2(self, disorder='ocd', save_fig=True):
        mean_HC, mean_disorder = self.count_image_analysis(disorder)
        mean_HC = np.sort(mean_HC)
        mean_disorder = np.sort(mean_disorder)
        plt.plot(mean_HC, '*', color=self.col[0])
        plt.plot(mean_disorder, '*', color=self.col[1])
        if save_fig:
            plt.savefig('../statistical_analysis_tasks/stats_jpg/where_is_tockie/mean_count_plot2.png')
        plt.show()
