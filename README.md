# Statistical Analysis Tasks



## How to use the project

### _Baseline to do statistical analysis of tasks_
1 - Git pull your project **data_ocd_metacognition**

2 - Download the new redcap and change the directory in the file **Template_Task_Statistics.py**
```python
class Template_Task_Statistics:
    """ The redcap export in csv, change the path every time with the correct one"""
    redcap_csv = pd.read_csv("Your_path", sep=',')
```
3 - Go to the **main.py** to plot and manipulate data

Using the name **result_seven** if you wish to look at the task Seven differences (and **result_lucifer, result_symmetry, result_where_is_tockie** for the other tasks)




### _How to update Data_baseline.csv_
1 - Download the new redcap and change the directory in the file **make_data_baseline.py**

2 - run **make_data_baseline.py**