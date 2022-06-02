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


def repart_sexe(df):
    return [len(df.sexe[df.sexe == 0]) / len(df.sexe) * 100,
            len(df.sexe[df.sexe == 1]) / len(df.sexe) * 100]


resume = pd.DataFrame(
    {'age': redcap_csv['ddn'].apply(age), 'sexe': redcap_csv['sexe'], 'disorder': redcap_csv['diagnostic_principal']})
resume_no_disorder = resume[resume.disorder == 0]
resume_disorder = resume[resume.disorder != 0]
resume_toc = resume[resume.disorder == 1]


def Repartition_age():
    # Répartion de l'age
    plt.title("Répartition de l'âge pour l'échantillon en entier")
    plt.boxplot(resume.age)
    #plt.show()
    print("L'age moyen est :", round(np.mean(resume.age)), "ans , le maximum est de ", max(resume.age),
          "ans et le minimum est de ",
          min(resume.age), "ans")

    # Age moyen selon les groupes
    plt.title("Age moyen pour selon les groupes")
    plt.boxplot([resume_no_disorder.age, resume_disorder.age])
    plt.xticks(np.array([1, 2]), ['No-disorder', "Disorder"])
    #plt.show()


def Repartition_sexe():
    # Répartion du sexe dans l'échantillion entier
    plt.title("Répartition du sexe pour l'échantillon en entier")
    plt.pie([len(resume.sexe[resume.sexe == 0]) / len(resume.sexe) * 100,
             len(resume.sexe[resume.sexe == 1]) / len(resume.sexe) * 100], labels=['Femme', 'Homme'], autopct='%1.1f%%')
    #plt.show()

    # Répartition selon les groupes
    group = [resume_no_disorder, resume_disorder, resume_toc]
    men_means = [repart_sexe(df)[1] for df in group]
    women_means = [repart_sexe(df)[0] for df in group]
    labels = ['No_disorder', 'All disorder', "Toc"]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, men_means, width, label='Men')
    rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    ax.set_ylabel('Pourcentage (%)')
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
    #plt.show()


plt.title('Répartition des sujets')
plt.pie([len(resume_no_disorder), len(resume) - len(resume_no_disorder) - len(resume_toc), len(resume_toc)],
        labels=['No_disorder', 'Other disorder', 'Toc'],
        autopct='%1.1f%%')
#plt.show()
Repartition_sexe()
Repartition_age()
print('\n')

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


def prop_etudes(tab):
    proportion = []
    for i in np.arange(0, 8):
        proportion.append(tab.etudes==i)
    return proportion


control = redcap_csv[redcap_csv.diagnostic_principal == 0]
toc = redcap_csv[redcap_csv.diagnostic_principal == 1]
other = redcap_csv[redcap_csv.diagnostic_principal !=1]
data_baseline = pd.DataFrame(np.array(['n = ', len(redcap_csv['record_id']), len(control), len(toc), len(other)]).T)
data_baseline[1] = ['Homme',repart_sexe(redcap_csv)[1], repart_sexe(control)[1], repart_sexe(toc)[1], repart_sexe(other)[1]]
data_baseline[2] = ['Femme', repart_sexe(redcap_csv)[0], repart_sexe(control)[0], repart_sexe(toc)[0], repart_sexe(other)[0]]

nom_etudes = ['Primaire', 'Secondaire','Bac', 'BEP/CAP', 'BTS', 'Licence', 'Master', 'Doctorat']
for i in np.arange(0, 8):
    data_baseline[i+3] = [f'{nom_etudes[i]}', len(redcap_csv[redcap_csv.etudes==i]), len(control[control.etudes==i]), len(toc[toc.etudes==i]), len(other[other.etudes==i])]
matrimoniale = ['Célibataire','En couple', 'Marié(e)','Divorcé(e)', 'Veuf(ve)']
for i in np.arange(0,5):
    data_baseline[i+11] = [f'{matrimoniale[i]}', len(redcap_csv[redcap_csv.matrimoniale==i]), len(control[control.matrimoniale==i]), len(toc[toc.matrimoniale==i]), len(other[other.matrimoniale==i])]

print(data_baseline)
#data_baseline.columns = ['Characteristic', 'Total', 'Control group', 'TOC group', 'Other disorder group']
data_baseline.to_csv('Data_baseline.csv')
#print(redcap_csv['diagnostic_principal'].unique())
