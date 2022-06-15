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
    for block in ['all', 'shocking', 'non-shocking', 'calligraphy', 'chess']:
        p = result_seven.group_comparison(type=block, category='Average difference', disorder=disorder,
                                          print_status=False)
        p_val.append(p)
        task_feature.append(['seven', block, 'Average difference'])

    for category in ['Success rate', 'Average reaction time', 'Maximum reaction time', 'Average count image',
                     'Maximum count image', 'Minimum count image', 'Success/count image']:
        p = result_where_is_tockie.group_comparison(category=category, disorder=disorder, print_status=False)
        p_val.append(p)
        task_feature.append(['where is tockie', category])

    significative_feature = [[task_feature[p_val.index(p)], p] for p in p_val if p < 0.05]
    print(significative_feature)
    return significative_feature


def recap_tab():
    tab = []
    tab.append(["", 'OCD', 'Healthy Control', "", 'OCD', 'Healthy Control', ""])
    tab.append(['Seven_diff', 'Mean', 'Mean', "", 'Mean', 'Mean', ""])
    for block in ['all', 'shocking', 'non-shocking', 'calligraphy', 'chess']:
        category1 = 'Success rate'
        category2 = 'Average reaction time'
        mean_ocd1 = np.round(np.mean(result_seven.get_disorder_stats(type=block)[category1]), 3)
        mean_hc1 = np.round(np.mean(result_seven.get_disorder_stats(type=block, disorder='none')[category1]), 3)
        p_value1 = np.round(result_seven.group_comparison(type=block, category=category1, print_status=False), 3)
        mean_ocd2 = np.round(np.mean(result_seven.get_disorder_stats(type=block)[category2]), 3)
        mean_hc2 = np.round(np.mean(result_seven.get_disorder_stats(type=block, disorder='none')[category2]), 3)
        p_value2 = np.round(result_seven.group_comparison(type=block, category=category2, print_status=False), 3)
        tab.append(["", block, mean_ocd1, mean_hc1, p_value1, mean_ocd2, mean_hc2, p_value2])
    tab.append(['Lucifer', '', '', "", '', '', ""])
    for type_lucifer in ['all', 'straight', 'messy', 'special']:
        category1 = 'Success rate'
        category2 = 'Average reaction time'
        mean_ocd1 = np.round(np.mean(result_lucifer.get_disorder_stats(type=type_lucifer)[category1]), 3)
        mean_hc1 = np.round(np.mean(result_lucifer.get_disorder_stats(type=type_lucifer, disorder='none')[category1]),
                            3)
        p_value1 = np.round(result_lucifer.group_comparison(type=type_lucifer, category=category1, print_status=False),
                            3)
        mean_ocd2 = np.round(np.mean(result_lucifer.get_disorder_stats(type=type_lucifer)[category2]), 3)
        mean_hc2 = np.round(np.mean(result_lucifer.get_disorder_stats(type=type_lucifer, disorder='none')[category2]),
                            3)
        p_value2 = np.round(result_lucifer.group_comparison(type=block, category=category2, print_status=False), 3)
        tab.append(["", block, mean_ocd1, mean_hc1, p_value1, mean_ocd2, mean_hc2, p_value2])
    print(pd.DataFrame(tab))


recap_tab()
# significative_group()
