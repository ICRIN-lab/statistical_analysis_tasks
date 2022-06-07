import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sps
from scipy.stats import chisquare
from datetime import datetime, date
from seven_diff_analysis import seven_diff_analysis
from lucifer_analysis import lucifer_analysis
from where_is_tockie_analysis import where_is_tockie_analysis
from symmetry_analysis import symmetry_analysis


task = seven_diff_analysis()
redcap_csv = task.redcap_csv


def age(born):
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


def Repartition_age():
    # Age moyen selon les groupes
    plt.title("Age moyen pour selon les groupes")
    plt.boxplot([hc.age, ocd.age, other.age])
    plt.xticks(np.array([1, 2, 3]), ["Healthy Control", "OCD", "Other disorder"])
    plt.show()


def Repartition_sexe():
    # Répartition du sexe dans l'échantillion entier
    plt.title("Répartition du sexe pour l'échantillon en entier")
    plt.pie([len(resume.sexe[resume.sexe == 0]) / len(resume.sexe) * 100,
             len(resume.sexe[resume.sexe == 1]) / len(resume.sexe) * 100], labels=['Femme', 'Homme'], autopct='%1.1f%%')
    plt.show()

    # Répartition selon les groupes
    group = [hc, ocd, other]
    men_means = [repart_sex(df)[1] for df in group]
    women_means = [repart_sex(df)[0] for df in group]
    labels = ["Healthy Control", 'Other disorder', "OCD"]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, men_means, width, label='Men')
    rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    ax.set_ylabel('')
    ax.set_title('Répartition du sexe selon les groupes')
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


plt.title('Répartition des sujets')
plt.pie([len(hc), len(ocd), len(other)],
        labels=["Healthy control", 'Other disorder', 'Toc'],
        autopct='%1.1f%%')


# plt.show()


# Analyse des données manquantes
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


def fill_column(final_name, name_in_csv, i, variable=False):
    if variable == False:
        return ["", final_name, len(redcap_csv[redcap_csv[name_in_csv] == i]), len(hc[hc[name_in_csv] == i]),
                len(ocd[ocd[name_in_csv] == i]),
                len(other[other[name_in_csv] == i])]
    else:
        return [final_name,"", len(redcap_csv[redcap_csv[name_in_csv] == i]), len(hc[hc[name_in_csv] == i]),
                len(ocd[ocd[name_in_csv] == i]),
                len(other[other[name_in_csv] == i])]



def make_data_baseline():
    data_baseline = [['', "", f"(n = {len(redcap_csv['record_id'])})", f"(n = {len(hc)})", f"(n = {len(ocd)})", f"(n = {len(other)})"],
                     ['Age, mean', "", round(np.mean(redcap_csv['ddn'].apply(age))), round(np.mean(hc.age)),
                      round(np.mean(ocd.age)),
                      round(np.mean(other.age))],
                     ['Gender', "", "", "", ""],
                     ["", 'Men', repart_sex(redcap_csv)[1], repart_sex(hc)[1], repart_sex(ocd)[1],
                      repart_sex(other)[1]],
                     ["", 'Women', repart_sex(redcap_csv)[0], repart_sex(hc)[0], repart_sex(ocd)[0],
                      repart_sex(other)[0]]
        , ['Educational level', "", "", "", "", ""]]
    study_name = ['Primary education', 'Secondary education', 'High school diploma', 'Vocational training', 'BTEC Higher National Diploma', 'Bachelor', 'Master', 'PhD']
    for i in np.arange(0, 8):
        data_baseline.append(fill_column(f'{study_name[i]}', 'etudes', i))
    data_baseline.append(['Marital Status', "", "", "", ""])
    marital = ['Single', 'In relationship', 'Maried', 'Divorced', 'Widowed']
    for i in np.arange(0, 5):
        data_baseline.append(fill_column(f'{marital[i]}', 'matrimoniale', i))
    data_baseline.append(fill_column('Current Smoker', 'tabac', 1,variable=True))
    data_baseline.append(fill_column('Current Alcohol Drinker', 'alcool', 1,variable=True))
    data_baseline.append(fill_column('Consumption of cafeine', 'cafeine', 1,variable=True))
    data_baseline.append(fill_column('Bad visual acuity', 'acuite', 1,variable=True))
    data_baseline.append(fill_column('Epilespy antecedent', 'epilepsie', 1,variable=True))
    data_baseline.append(fill_column('Brain stimulation', 'stimulation', 1,variable=True))
    data_baseline.append(['Brain stimulation techniques', "", "", "", "", ""])
    technique_name = ['rTMS', 'tDCS', 'deep TMS', 'TCES']
    for i in np.arange(0, 4):
        data_baseline.append(fill_column(f'{technique_name[i]}', 'technique_stimulation_ni', i))
    data_baseline.append(['Health state score', "", "", "", "", ""])
    data_baseline.append(['VAS score', "", "", "", "", ""])
    data_baseline.append(['HAD anxiety score', "", "", "", "", ""])
    data_baseline.append(['HAD depression score', "", "", "", "", ""])
    data_baseline.append(['Ybocs score', "", "", "", "", ""])
    data_baseline.append(["", "< 7", "", "", len(ocd[ocd.ybocs_score_tot < 7]), ""])
    data_baseline.append(["", "8 - 15", "", "", len(ocd[(ocd.ybocs_score_tot >= 8) & (ocd.ybocs_score_tot <= 15)]), ""])
    data_baseline.append(
        ["", "16 - 23", "", "", len(ocd[(ocd.ybocs_score_tot >= 16) & (ocd.ybocs_score_tot <= 23)]), ""])
    data_baseline.append(
        ["", "24 - 31", "", "", len(ocd[(ocd.ybocs_score_tot >= 24) & (ocd.ybocs_score_tot <= 31)]), ""])
    data_baseline.append(
        ["", "32 - 40", "", "", len(ocd[(ocd.ybocs_score_tot >= 32) & (ocd.ybocs_score_tot <= 40)]), ""])
    data_baseline = pd.DataFrame(data_baseline)
    data_baseline.columns = ['Variable', 'Characteristic', 'All subjects', 'Healthy control', 'OCD patients', 'Other disorder']
    data_baseline.to_csv('Data_baseline.csv', index=False)

make_data_baseline()
data_baseline = pd.read_csv('Data_baseline.csv')
a=data_baseline[data_baseline.Characteristic == 'Men'].iloc[:,2].astype(int)
b=data_baseline[data_baseline.Characteristic == 'Women'].iloc[:,2:].astype(int)
c=data_baseline.iloc[[3,4],2:].astype(int)
print(int(np.array(a)[0]))
