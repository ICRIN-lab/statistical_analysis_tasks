import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
from seven_diff_analysis import seven_diff_analysis
from lucifer_analysis import lucifer_analysis
from where_is_tockie_analysis import where_is_tockie_analysis
from symmetry_analysis import symmetry_analysis

task = seven_diff_analysis()
redcap_csv = task.redcap_csv


def age(born):
    """
    Determine age from a date of birth
    """
    born = datetime.strptime(born, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month,
                                      today.day) < (born.month,
                                                    born.day))


def repart_sex(df):
    return [len(df.sexe[df.sexe == 0]),
            len(df.sexe[df.sexe == 1])]


hc = redcap_csv[redcap_csv.diagnostic_principal == 0]
ocd = redcap_csv[redcap_csv.diagnostic_principal == 1]
redcap_without_control = redcap_csv[redcap_csv.diagnostic_principal != 0]
other = redcap_without_control[redcap_without_control.diagnostic_principal != 1]

hc = hc.assign(age=hc['ddn'].apply(age))
ocd = ocd.assign(age=ocd['ddn'].apply(age))
other = other.assign(age=other['ddn'].apply(age))

resume = pd.DataFrame(
    {'age': redcap_csv['ddn'].apply(age), 'gender': redcap_csv['sexe'], 'disorder': redcap_csv['diagnostic_principal']})


def repartition_age():
    plt.title("Age regarding group")
    df = pd.DataFrame({"Healthy Control": hc.age, "OCD": ocd.age, "Other disorder": other.age})
    sns.boxplot(data=df)
    plt.show()


def repartition_sexe():
    group = [hc, ocd, other]
    men_means = [repart_sex(df)[1] for df in group]
    women_means = [repart_sex(df)[0] for df in group]
    labels = ["Healthy Control", 'Other disorder', "OCD"]
    x = np.arange(len(labels))
    width = 0.35

    plt.title("Sex distribution of our data")
    plt.pie([len(resume.gender[resume.gender == 0]) / len(resume.gender) * 100,
             len(resume.gender[resume.gender == 1]) / len(resume.gender) * 100], labels=['Women', 'Men'],
            autopct='%1.1f%%')
    plt.show()
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, men_means, width, label='Men')
    rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    ax.set_ylabel('')
    ax.set_title('Sex distribution regarding group')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    plt.show()


def all_missing_csv():
    task = [seven_diff_analysis, lucifer_analysis, where_is_tockie_analysis, symmetry_analysis]
    task_name = ['seven_diff', 'lucifer', 'where_is_tockie', 'symmetry']
    for analysis, name in zip(task, task_name):
        task_analysis = analysis()
        print(f"Le nombre de données manquantes pour {name} est de :",
              len(task_analysis.redcap_csv['record_id']) - len(task_analysis.df_files))
        all_id = []
        for df in task_analysis.df_files:
            all_id.append(task_analysis.get_id(df))
        missing_csv_id = []
        for id in task_analysis.redcap_csv['record_id']:
            if id not in all_id:
                missing_csv_id.append(id)
        print(f"Il n'y a pas de csv pour la tâche {name} pour les individus", missing_csv_id)


def exact_value(x):
    return round(x,2)


plt.title('Distribution of our data')
plt.pie([len(hc), len(ocd), len(other)],
        labels=["Healthy control", 'Other disorder', 'Toc'], autopct=exact_value)
plt.show()

repartition_age()
repartition_sexe()
all_missing_csv()
