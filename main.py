import pandas as pd

from seven_diff_analysis import seven_diff_analysis
from lucifer_analysis import lucifer_analysis
from where_is_tockie_analysis import where_is_tockie_analysis
from symmetry_analysis import symmetry_analysis
import numpy as np

result_seven = seven_diff_analysis()
result_lucifer = lucifer_analysis()
result_where_is_tockie = where_is_tockie_analysis()
result_symmetry = symmetry_analysis()


def significative_group(disorder='ocd'):
    task_feature = []
    p_val = []
    for category in ['Success rate', 'Average reaction time', 'Maximum reaction time']:
        for block in ['all', 'shocking', 'non-shocking', 'calligraphy', 'chess']:
            p = result_seven.group_comparison(type=block, category=category, disorder=disorder, print_status=False)
            p_val.append(p)
            task_feature.append(['seven_diff', block, category])
        for type_lucifer in ['all', 'straight', 'messy']:
            p = result_lucifer.group_comparison(type=type_lucifer, category=category, disorder=disorder,
                                                print_status=False)
            p_val.append(p)
            task_feature.append(['lucifer', type_lucifer, category])
        p = result_symmetry.group_comparison(category=category, disorder=disorder, print_status=False)
        p_val.append(p)
        task_feature.append(['symmetry', category])
    #for block in ['all', 'shocking', 'non-shocking', 'calligraphy', 'chess']:
        #p = result_seven.group_comparison(type=block, category='Average difference', disorder=disorder,
                                          #print_status)
        #p_val.append(p)
        #task_feature.append(['seven', block, 'Average difference'])

    for category in ['Success rate', 'Average reaction time', 'Maximum reaction time', 'Average count image',
                     'Maximum count image', 'Minimum count image', 'Success/count image']:
        p = result_where_is_tockie.group_comparison(category=category, disorder=disorder, print_status=False)
        p_val.append(p)
        task_feature.append(['where is tockie', category])

    significative_feature = [[task_feature[p_val.index(p)], round(p,3)] for p in p_val if p < 0.05]
    print('On obtient un p-valeur <0.05 pour les categories suivantes :')
    for i in range(len(significative_feature)):
        tab=significative_feature[i]
        if len(tab[0]) == 3:
             print('Pour la tâche ', tab[0][0], ',block =', tab[0][1], '(category =', tab[0][2], ') avec p=',
                      tab[1])
        if len(tab[0]) == 2:
            print('Pour la tâche ', tab[0][0], '(category =', tab[0][1], ') avec p=', tab[1])
    return significative_feature


def line_tab(task_result, type='all', category1='Success rate', category2='Average reaction time'):
    mean_ocd1 = np.round(np.mean(task_result.get_disorder_stats(type=type)[category1]), 3)
    mean_hc1 = np.round(np.mean(task_result.get_disorder_stats(type=type, disorder='none')[category1]), 3)
    p_value1 = np.round(task_result.group_comparison(type=type, category=category1, print_status=False), 3)
    mean_ocd2 = np.round(np.mean(task_result.get_disorder_stats(type=type)[category2]), 3)
    mean_hc2 = np.round(np.mean(task_result.get_disorder_stats(type=type, disorder='none')[category2]), 3)
    p_value2 = np.round(task_result.group_comparison(type=type, category=category2, print_status=False), 3)
    if type == 'all':
        type = ""
    return [type, mean_ocd1, mean_hc1, p_value1, mean_ocd2, mean_hc2, p_value2]


def recap_tab():
    tab = [["", 'Success rate', "", "", 'Average reaction time', "", ""]]
    tab.append(["", 'OCD', 'Healthy Control', "", 'OCD', 'Healthy Control', ""])
    tab.append(['Seven_diff', 'Mean', 'Mean', "p-value", 'Mean', 'Mean', "p-value"])
    for block in ['all', 'shocking', 'non-shocking', 'calligraphy', 'chess']:
        tab.append(line_tab(task_result=result_seven, type=block))
    tab.append(['Lucifer', '', '', "", '', '', ""])
    for type_lucifer in ['all', 'straight', 'messy', 'special']:
        tab.append(line_tab(task_result=result_lucifer, type=type_lucifer))
    tab.append(['Symmetry', '', '', "", '', '', ""])
    tab.append(line_tab(task_result=result_symmetry))
    tab.append(['Where Is Tockie', '', '', "", '', '', ""])
    tab.append(line_tab(task_result=result_where_is_tockie))
    tab = pd.DataFrame(tab)
    tab.to_csv('../statistical_analysis_tasks/other/overview_tab.csv', index=False)
    return tab



