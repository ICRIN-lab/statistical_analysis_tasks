from seven_diff_analysis import seven_diff_analysis
from lucifer_analysis import lucifer_analysis
from where_is_tockie_analysis import where_is_tockie_analysis
from symmetry_analysis import symmetry_analysis


result_seven =seven_diff_analysis()


result_lucifer = lucifer_analysis()
result_lucifer.boxplot_average(disorder='all',type_lucifer='messy')