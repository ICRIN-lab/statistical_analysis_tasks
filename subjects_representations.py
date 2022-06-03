import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    # Répartition de l'age
    plt.title("Répartition de l'âge pour l'échantillon en entier")
    plt.boxplot(resume.age)
    plt.show()

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
plt.show()

# Analyse des données manquantes
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

# Création d'un tableau avec les characteristiques principales des individus
data_baseline = pd.DataFrame(np.array(['n = ', len(redcap_csv['record_id']), len(hc), len(ocd), len(other)]).T)
data_baseline[1] = ['Gender', "", "", "", ""]
data_baseline[2] = ['Men', repart_sex(redcap_csv)[1], repart_sex(hc)[1], repart_sex(ocd)[1],
                    repart_sex(other)[1]]
data_baseline[3] = ['Women', repart_sex(redcap_csv)[0], repart_sex(hc)[0], repart_sex(ocd)[0],
                    repart_sex(other)[0]]
data_baseline[4] = ['Age moyen', np.mean(redcap_csv['ddn'].apply(age)), np.mean(hc.age), np.mean(ocd.age),
                    np.mean(other.age)]
data_baseline[5] = ['Educational level', "", "", "", ""]
nom_etudes = ['Primary School', 'Secondary School', 'Bac', 'BEP/CAP', 'BTS', 'Licence', 'Master', 'Doctorat']
for i in np.arange(0, 8):
    data_baseline[i + 6] = [f'{nom_etudes[i]}', len(redcap_csv[redcap_csv.etudes == i]),
                            len(hc[hc.etudes == i]), len(ocd[ocd.etudes == i]), len(other[other.etudes == i])]
data_baseline[13] = ['Marital Status', "", "", "", ""]
matrimoniale = ['Single', 'En couple', 'Maried', 'Divorced', 'Widowed']
for i in np.arange(0, 5):
    data_baseline[i + 14] = [f'{matrimoniale[i]}', len(redcap_csv[redcap_csv.matrimoniale == i]),
                             len(hc[hc.matrimoniale == i]), len(ocd[ocd.matrimoniale == i]),
                             len(other[other.matrimoniale == i])]
# data_baseline[19] = ['Current Smoker', len(redcap_csv[redcap_csv['tabac'] == 1]),]

data_baseline = pd.DataFrame(np.array(data_baseline).T)
data_baseline.columns = ['Characteristic', 'Total', 'Control group', 'TOC group', 'Other disorder']
data_baseline.to_csv('Data_baseline.csv')

print(ocd.ybocs_score_tot.describe())
# print(control.age.describe())
