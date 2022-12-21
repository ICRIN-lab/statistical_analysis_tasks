import pandas as pd
from scipy import stats

from seven_diff_analysis import SevenDiffAnalysis
from lucifer_analysis import LuciferAnalysis
from where_is_tockie_analysis import WhereIsTockieAnalysis
from symmetry_analysis import SymmetryAnalysis
import numpy as np

import matplotlib.pyplot as plt

result_seven = SevenDiffAnalysis()
result_symmetry = SymmetryAnalysis()
result_lucifer = LuciferAnalysis()
result_where_is_tockie = WhereIsTockieAnalysis()


def significative_group(disorder='ocd'):
    task_feature = []
    p_val = []
    for category in ['Success rate', 'Average reaction time', 'Maximum reaction time']:
        for block in ['all', 'shocking', 'non-shocking', 'calligraphy', 'chess']:
            p = result_seven.group_comparison(block=block, category=category, disorder=disorder, print_status=False)
            p_val.append(p)
            task_feature.append(['seven_diff', block, category])
        for block_lucifer in ['all', 'straight', 'messy']:
            p = result_lucifer.group_comparison(block=block_lucifer, category=category, disorder=disorder,
                                                print_status=False)
            p_val.append(p)
            task_feature.append(['lucifer', block_lucifer, category])
        p = result_symmetry.group_comparison(category=category, disorder=disorder, print_status=False)
        p_val.append(p)
        task_feature.append(['symmetry', category])
    # for block in ['all', 'shocking', 'non-shocking', 'calligraphy', 'chess']:
    # p = result_seven.group_comparison(block=block, category='Average difference', disorder=disorder,
    # print_status)
    # p_val.append(p)
    # task_feature.append(['seven', block, 'Average difference'])

    for category in ['Success rate', 'Average reaction time', 'Maximum reaction time', 'Average count image',
                     'Maximum count image', 'Minimum count image', 'Success/count image']:
        p = result_where_is_tockie.group_comparison(category=category, disorder=disorder, print_status=False)
        p_val.append(p)
        task_feature.append(['where is tockie', category])

    significative_feature = [[task_feature[p_val.index(p)], round(p, 3)] for p in p_val if p < 0.05]
    print('On obtient un p-valeur <0.05 pour les categories suivantes :')
    for i in range(len(significative_feature)):
        tab = significative_feature[i]
        if len(tab[0]) == 3:
            print('Pour la tâche ', tab[0][0], ',block =', tab[0][1], '(category =', tab[0][2], ') avec p=',
                  tab[1])
        if len(tab[0]) == 2:
            print('Pour la tâche ', tab[0][0], '(category =', tab[0][1], ') avec p=', tab[1])
    return significative_feature


def line_tab(task_result, block='all', category1='Success rate', category2='Average reaction time'):
    mean_ocd1 = np.round(np.mean(task_result.get_disorder_stats(block=block)[category1]), 3)
    mean_hc1 = np.round(np.mean(task_result.get_disorder_stats(block=block, disorder='none')[category1]), 3)
    p_value1 = np.round(task_result.group_comparison(block=block, category=category1, print_status=False), 3)
    mean_ocd2 = np.round(np.mean(task_result.get_disorder_stats(block=block)[category2]), 3)
    mean_hc2 = np.round(np.mean(task_result.get_disorder_stats(block=block, disorder='none')[category2]), 3)
    p_value2 = np.round(task_result.group_comparison(block=block, category=category2, print_status=False), 3)
    if block == 'all':
        block = ""
    return [block, mean_ocd1, mean_hc1, p_value1, mean_ocd2, mean_hc2, p_value2]


def redcap_tab():
    tab = [["", 'Success rate', "", "", 'Average reaction time', "", ""],
           ["", 'OCD', 'Controls', "", 'OCD', 'Controls', ""],
           ['Seven_diff', 'Mean', 'Mean', "p-value", 'Mean', 'Mean', "p-value"]]
    for block in ['all', 'shocking', 'non-shocking', 'calligraphy', 'chess']:
        tab.append(line_tab(task_result=result_seven, block=block))
    tab.append(['Lucifer', '', '', "", '', '', ""])
    for block_lucifer in ['all', 'straight', 'messy', 'special']:
        tab.append(line_tab(task_result=result_lucifer, block=block_lucifer))
    tab.append(['Symmetry', '', '', "", '', '', ""])
    tab.append(line_tab(task_result=result_symmetry))
    tab.append(['Where Is Tockie', '', '', "", '', '', ""])
    tab.append(line_tab(task_result=result_where_is_tockie))
    tab = pd.DataFrame(tab)
    tab.to_csv('../statistical_analysis_tasks/other/overview_tab.csv', index=False)
    return tab


def summary_stats():
    lucifer_all = pd.read_csv('stats_jpg/lucifer/stats_lucifer_all.csv')
    lucifer_messy = pd.read_csv('stats_jpg/lucifer/stats_lucifer_messy.csv')
    lucifer_special = pd.read_csv('stats_jpg/lucifer/stats_lucifer_special.csv')
    lucifer_straight = pd.read_csv('stats_jpg/lucifer/stats_lucifer_straight.csv')
    symmetry = pd.read_csv('stats_jpg/symmetry/stats_symmetry.csv')
    seven_diff_all = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_all.csv')
    seven_diff_shocking = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_shocking.csv')
    seven_diff_non_shocking = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_non-shocking.csv')
    seven_diff_calligraphy = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_calligraphy.csv')
    seven_diff_chess = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_chess.csv')
    where_is_tockie_all = pd.read_csv('stats_jpg/where_is_tockie/stats_where_is_tockie.csv')

    summary_data = [["Lucifer", "", "", "", "", ""],
                    ["", "Success rate all (%)",
                     round(float(np.mean(lucifer_all[lucifer_all.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(lucifer_all[lucifer_all.disorder == 0]["Success rate"])), 2), round(
                        stats.ttest_ind(lucifer_all[lucifer_all.disorder == 1]["Success rate"],
                                        lucifer_all[lucifer_all.disorder == 0]["Success rate"])[0], 2), round(
                        stats.ttest_ind(lucifer_all[lucifer_all.disorder == 1]["Success rate"],
                                        lucifer_all[lucifer_all.disorder == 0]["Success rate"])[1], 3)],
                    ["", "Success rate messy (%)",
                     round(float(np.mean(lucifer_messy[lucifer_messy.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(lucifer_messy[lucifer_messy.disorder == 0]["Success rate"])), 2), round(
                        stats.ttest_ind(lucifer_messy[lucifer_messy.disorder == 1]["Success rate"],
                                        lucifer_messy[lucifer_messy.disorder == 0]["Success rate"])[0], 2), round(
                        stats.ttest_ind(lucifer_messy[lucifer_messy.disorder == 1]["Success rate"],
                                        lucifer_messy[lucifer_messy.disorder == 0]["Success rate"])[1], 3)],
                    ["", "Success rate special (%)",
                     round(float(np.mean(lucifer_special[lucifer_special.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(lucifer_special[lucifer_special.disorder == 0]["Success rate"])), 2), round(
                        stats.ttest_ind(lucifer_special[lucifer_special.disorder == 1]["Success rate"],
                                        lucifer_special[lucifer_special.disorder == 0]["Success rate"])[0], 2), round(
                        stats.ttest_ind(lucifer_special[lucifer_special.disorder == 1]["Success rate"],
                                        lucifer_special[lucifer_special.disorder == 0]["Success rate"])[1], 3)],
                    ["", "Success rate straight (%)",
                     round(float(np.mean(lucifer_straight[lucifer_straight.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(lucifer_straight[lucifer_straight.disorder == 0]["Success rate"])), 2), round(
                        stats.ttest_ind(lucifer_straight[lucifer_straight.disorder == 1]["Success rate"],
                                        lucifer_straight[lucifer_straight.disorder == 0]["Success rate"])[0], 2), round(
                        stats.ttest_ind(lucifer_straight[lucifer_straight.disorder == 1]["Success rate"],
                                        lucifer_straight[lucifer_straight.disorder == 0]["Success rate"])[1], 3)],
                    ["", "", "", "", "", "", ],
                    ["Symmetry", "", "", "", "", ""],
                    ["", "Success rate symmetry (%)",
                     round(float(np.mean(symmetry[symmetry.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(symmetry[symmetry.disorder == 0]["Success rate"])), 2), round(
                        stats.ttest_ind(symmetry[symmetry.disorder == 1]["Success rate"],
                                        symmetry[symmetry.disorder == 0]["Success rate"])[0], 2), round(
                        stats.ttest_ind(symmetry[symmetry.disorder == 1]["Success rate"],
                                        symmetry[symmetry.disorder == 0]["Success rate"])[1], 3)],
                    ["", "", "", "", "", ""],
                    ["Seven Diff", "", "", "", "", ""],
                    ["", "Success rate all (%)",
                     round(float(np.mean(seven_diff_all[seven_diff_all.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(seven_diff_all[seven_diff_all.disorder == 0]["Success rate"])), 2), round(
                        stats.ttest_ind(seven_diff_all[seven_diff_all.disorder == 1]["Success rate"],
                                        seven_diff_all[seven_diff_all.disorder == 0]["Success rate"])[0], 2), round(
                        stats.ttest_ind(seven_diff_all[seven_diff_all.disorder == 1]["Success rate"],
                                        seven_diff_all[seven_diff_all.disorder == 0]["Success rate"])[1], 5)],
                    ["", "Success rate shocking (%)",
                     round(float(np.mean(seven_diff_shocking[seven_diff_shocking.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(seven_diff_shocking[seven_diff_shocking.disorder == 0]["Success rate"])), 2),
                     round(stats.ttest_ind(seven_diff_shocking[seven_diff_shocking.disorder == 1]["Success rate"],
                                           seven_diff_shocking[seven_diff_shocking.disorder == 0]["Success rate"])[0],
                           2), round(
                        stats.ttest_ind(seven_diff_shocking[seven_diff_shocking.disorder == 1]["Success rate"],
                                        seven_diff_shocking[seven_diff_shocking.disorder == 0]["Success rate"])[1], 3)],
                    ["", "Success rate non-shocking (%)", round(
                        float(np.mean(seven_diff_non_shocking[seven_diff_non_shocking.disorder == 1]["Success rate"])),
                        2), round(
                        float(np.mean(seven_diff_non_shocking[seven_diff_non_shocking.disorder == 0]["Success rate"])),
                        2), round(
                        stats.ttest_ind(seven_diff_non_shocking[seven_diff_non_shocking.disorder == 1]["Success rate"],
                                        seven_diff_non_shocking[seven_diff_non_shocking.disorder == 0]["Success rate"])[
                            0], 2), round(
                        stats.ttest_ind(seven_diff_non_shocking[seven_diff_non_shocking.disorder == 1]["Success rate"],
                                        seven_diff_non_shocking[seven_diff_non_shocking.disorder == 0]["Success rate"])[
                            1], 3)],
                    ["", "Success rate calligraphy (%)",
                     round(float(np.mean(seven_diff_calligraphy[seven_diff_calligraphy.disorder == 1]["Success rate"])),
                           2),
                     round(float(np.mean(seven_diff_calligraphy[seven_diff_calligraphy.disorder == 0]["Success rate"])),
                           2), round(
                        stats.ttest_ind(seven_diff_calligraphy[seven_diff_calligraphy.disorder == 1]["Success rate"],
                                        seven_diff_calligraphy[seven_diff_calligraphy.disorder == 0]["Success rate"])[
                            0], 2), round(
                        stats.ttest_ind(seven_diff_calligraphy[seven_diff_calligraphy.disorder == 1]["Success rate"],
                                        seven_diff_calligraphy[seven_diff_calligraphy.disorder == 0]["Success rate"])[
                            1], 3)],
                    ["", "Success rate chess (%)",
                     round(float(np.mean(seven_diff_chess[seven_diff_chess.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(seven_diff_chess[seven_diff_chess.disorder == 0]["Success rate"])), 2), round(
                        stats.ttest_ind(seven_diff_chess[seven_diff_chess.disorder == 1]["Success rate"],
                                        seven_diff_chess[seven_diff_chess.disorder == 0]["Success rate"])[0], 2), round(
                        stats.ttest_ind(seven_diff_chess[seven_diff_chess.disorder == 1]["Success rate"],
                                        seven_diff_chess[seven_diff_chess.disorder == 0]["Success rate"])[1], 3)],
                    ["", "", "", "", "", ""],
                    ["Where Is Tockie", "", "", "", "", ""],
                    ["", "Success rate (%)",
                     round(float(np.mean(where_is_tockie_all[where_is_tockie_all.disorder == 1]["Success rate"])), 2),
                     round(float(np.mean(where_is_tockie_all[where_is_tockie_all.disorder == 0]["Success rate"])), 2),
                     round(stats.ttest_ind(where_is_tockie_all[where_is_tockie_all.disorder == 1]["Success rate"],
                                           where_is_tockie_all[where_is_tockie_all.disorder == 0]["Success rate"])[0],
                           2), round(
                        stats.ttest_ind(where_is_tockie_all[where_is_tockie_all.disorder == 1]["Success rate"],
                                        where_is_tockie_all[where_is_tockie_all.disorder == 0]["Success rate"])[1], 3)],
                    ["", "Average count image", round(
                        float(np.mean(where_is_tockie_all[where_is_tockie_all.disorder == 1]["Average count image"])),
                        2), round(
                        float(np.mean(where_is_tockie_all[where_is_tockie_all.disorder == 0]["Average count image"])),
                        2), round(
                        stats.ttest_ind(where_is_tockie_all[where_is_tockie_all.disorder == 1]["Average count image"],
                                        where_is_tockie_all[where_is_tockie_all.disorder == 0]["Average count image"])[
                            0], 2), round(
                        stats.ttest_ind(where_is_tockie_all[where_is_tockie_all.disorder == 1]["Average count image"],
                                        where_is_tockie_all[where_is_tockie_all.disorder == 0]["Average count image"])[
                            1], 3)]
                    ]
    summary_data = pd.DataFrame(summary_data)
    summary_data.columns = ['', '', 'OCD', 'HC', "t", "p"]
    summary_data.to_csv('summary_stats.csv', index=False)
    return summary_data


summary_stats()
# list_patients_eeg = result_seven.get_eeg_patient()
# print("list patients = ", list_patients_eeg)
# result_seven.stats(save_tab=True)
# result_seven.plot_pourcentage(save_fig=True)
# result_seven.plot_pourcentage(block="non-shocking")
# result_seven.plot_pourcentage(block="calligraphy")
# result_seven.plot_pourcentage(block="shocking")
# result_seven.plot_pourcentage(block="non-shocking")
# result_symmetry.stats(save_tab=True)
# result_symmetry.stats()
# result_symmetry.test_success_rate()
# result_seven.stats("shocking", save_tab=True)
# result_lucifer.stats("special")
# result_lucifer.plot_pourcentage()
# significative_group()

# df_count = result_where_is_tockie.count_image_analysis_ilyass(disorder='ocd')
# print(df_count)
# y = stats.ttest_ind(df_count["HC"], df_count["OCD"])
# norm_test_2samples = stats.ks_2samp(df_count["OCD"], df_count["HC"])
# norm_test_1sample_OCD = stats.kstest(df_count["OCD"], "norm")
# norm_test_1sample_HC = stats.kstest(df_count["HC"], "norm")
# norm_test_shapiro = stats.shapiro(df_count["OCD"])
# norm_test_anderson = stats.anderson(df_count["OCD"], dist="norm")
# levene_test = stats.levene(df_count["OCD"], df_count["HC"])
# print(norm_test_1sample_OCD)
# print(norm_test_1sample_HC)
# print(norm_test_shapiro)
# print(norm_test_anderson)
# print(levene_test)

'''
WHERE IS TOCKIE
'''
# result_where_is_tockie.plot_pourcentage(first_try_analysis=False)
#result_where_is_tockie.count_image_analysis_ilyass()

'''
LUCIFER
'''
result_lucifer.average_rt() # + success rate t test
# result_lucifer.plot_pourcentage()

'''
Seven Diff
'''
# result_seven.plot_pourcentage()
# result_seven.tests_seven_diff()
'''
Symmetry
'''
# result_symmetry.plot_pourcentage()
# result_symmetry.test_success_rate()


