import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from seven_diff_analysis import seven_diff_analysis
from lucifer_analysis import lucifer_analysis
from where_is_tockie_analysis import where_is_tockie_analysis
from symmetry_analysis import symmetry_analysis

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

    for category in ['Success rate', 'Average reaction time', 'Maximum reaction time', 'Average count image',
                     'Maximum count image', 'Minimum count image', 'Success/count image']:
        p = result_where_is_tockie.group_comparison(category=category, disorder=disorder, print_status=False)
        p_val.append(p)
        task_feature.append(['where is tockie', category])
    significative_feature = [[task_feature[p_val.index(p)], p] for p in p_val if p < 0.05]
    print(significative_feature)
    return significative_feature


#significative_group()
result_where_is_tockie.count_image_plot()


