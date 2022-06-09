import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sps
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


def repartition_age():
    # Age moyen selon les groupes
    plt.title("Age moyen pour selon les groupes")
    plt.boxplot([hc.age, ocd.age, other.age])
    plt.xticks(np.array([1, 2, 3]), ["Healthy Control", "OCD", "Other disorder"])
    plt.show()


def repartition_sexe():
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
    if not variable:
        return ["", final_name, len(redcap_csv[redcap_csv[name_in_csv] == i]), len(hc[hc[name_in_csv] == i]),
                len(ocd[ocd[name_in_csv] == i]),
                len(other[other[name_in_csv] == i])]
    else:
        return [final_name, "", len(redcap_csv[redcap_csv[name_in_csv] == i]), len(hc[hc[name_in_csv] == i]),
                len(ocd[ocd[name_in_csv] == i]),
                len(other[other[name_in_csv] == i])]


def get_value(characteristic_name, variable=False):
    data_baseline = pd.read_csv('Data_baseline.csv')
    if not variable:
        characteristic_line = data_baseline[data_baseline['Characteristic'] == characteristic_name]
    else:
        characteristic_line = data_baseline[data_baseline['Variable'] == characteristic_name]
    list_values = []
    for i in range(3, 6):
        list_values.append(characteristic_line[characteristic_line.columns[i]].astype(int).values[0])
    return list_values


def get_value_opposite(characteristic_name, variable):
    list = get_value(characteristic_name=characteristic_name, variable=variable)
    opposite_list = [len(hc) - list[0], len(ocd) - list[1], len(other) - list[2]]
    return opposite_list


def p_value_column():
    tab_study = [get_value('Primary education'), get_value('Secondary education'),
                 get_value('High school diploma'), get_value('Vocational training'),
                 get_value('BTEC Higher National Diploma'), get_value('Bachelor'),
                 get_value('Master'), get_value('PhD')]

    [tab_study.remove(t) for t in tab_study if t == [0, 0, 0]]

    tab = [" ", round(sps.f_oneway(hc.age, ocd.age, other.age)[1], 3),
           round(sps.ttest_ind(get_value('Men'), get_value('Women'))[1], 3), "",
           "", round(sps.chi2_contingency(tab_study)[1], 3), "", "", "", "", "", "", "", "",
           round(sps.chi2_contingency(
               [get_value('Single'), get_value('In relationship'), get_value('Maried'), get_value('Divorced'),
                get_value('Widowed')])[1], 3), "", "", "", "", ""]

    names_list = ['Current Smoker', 'Current Alcohol Drinker', 'Consumption of cafeine', 'Bad visual acuity',
                  'Epilepsy antecedent', 'Brain stimulation']
    for name in names_list:
        tab.append(round(sps.f_oneway(get_value(name, variable=True), get_value_opposite(name, variable=True))[1], 3))
    tab.extend([""] * 5)

    names_list2 = ['maudsley_score', 'eq5d5l_score_tot', 'eq5d5l_sore_valid_sante']
    for name2 in names_list2:
        ocd_name = np.array(ocd[name2])
        ocd_tab = ocd_name[~np.isnan(ocd_name)]
        other_name =np.array(other[name2])
        other_tab = other_name[~np.isnan(other_name)]
        tab.append(sps.ttest_ind(ocd_tab, other_tab)[1])
    tab.extend([""] * 8)
    return tab


def make_data_baseline():
    data_baseline = [['', "", f"(n = {len(redcap_csv['record_id'])})", f"(n = {len(hc)})", f"(n = {len(ocd)})",
                      f"(n = {len(other)})"],
                     ['Age', "",
                      f"{round(np.mean(redcap_csv['ddn'].apply(age)), 2)} ({round(np.std(redcap_csv['ddn'].apply(age)), 2)})",
                      f"{round(np.mean(hc.age), 2)} ({round(np.std(hc.age), 2)})",
                      f"{round(np.mean(ocd.age), 2)} ({round(np.std(ocd.age), 2)})",
                      f"{round(np.mean(other.age), 2)} ({round(np.std(other.age), 2)})"],
                     ['Gender', "", "", "", ""],
                     ["", 'Men', repart_sex(redcap_csv)[1], repart_sex(hc)[1], repart_sex(ocd)[1],
                      repart_sex(other)[1]],
                     ["", 'Women', repart_sex(redcap_csv)[0], repart_sex(hc)[0], repart_sex(ocd)[0],
                      repart_sex(other)[0]]
        , ['Educational level', "", "", "", "", ""]]
    study_name = ['Primary education', 'Secondary education', 'High school diploma', 'Vocational training',
                  'BTEC Higher National Diploma', 'Bachelor', 'Master', 'PhD']
    for i in np.arange(0, 8):
        data_baseline.append(fill_column(f'{study_name[i]}', 'etudes', i))
    data_baseline.append(['Marital Status', "", "", "", ""])
    marital = ['Single', 'In relationship', 'Maried', 'Divorced', 'Widowed']
    for i in np.arange(0, 5):
        data_baseline.append(fill_column(f'{marital[i]}', 'matrimoniale', i))
    data_baseline.append(fill_column('Current Smoker', 'tabac', 1, variable=True))
    data_baseline.append(fill_column('Current Alcohol Drinker', 'alcool', 1, variable=True))
    data_baseline.append(fill_column('Consumption of cafeine', 'cafeine', 1, variable=True))
    data_baseline.append(fill_column('Bad visual acuity', 'acuite', 1, variable=True))
    data_baseline.append(fill_column('Epilepsy antecedent', 'epilepsie', 1, variable=True))
    data_baseline.append(fill_column('Brain stimulation', 'stimulation', 1, variable=True))
    data_baseline.append(['Brain stimulation techniques', "", "", "", "", ""])
    technique_name = ['rTMS', 'tDCS', 'deep TMS', 'TCES']
    for i in np.arange(0, 4):
        data_baseline.append(fill_column(f'{technique_name[i]}', 'technique_stimulation_ni', i))
    data_baseline.append(
        ['Resistance score (Maudsley)', "", "", "",
         f"{round(np.mean(ocd.maudsley_score), 2)} ({round(np.std(ocd.maudsley_score), 2)})",
         f"{round(np.mean(other.maudsley_score), 2)} ({round(np.std(other.maudsley_score), 2)})"])
    data_baseline.append(
        ['Health state score', "", "", "",
         f"{round(np.mean(ocd.eq5d5l_score_tot), 2)} ({round(np.std(ocd.eq5d5l_score_tot), 2)})",
         f"{round(np.mean(other.eq5d5l_score_tot), 2)} ({round(np.std(other.eq5d5l_score_tot), 2)})"])
    data_baseline.append(
        ['VAS score', "", "", "",
         f"{round(np.mean(ocd.eq5d5l_sore_valid_sante), 2)} ({round(np.std(ocd.eq5d5l_sore_valid_sante), 2)})",
         f"{round(np.mean(other.eq5d5l_sore_valid_sante), 2)} ({round(np.std(other.eq5d5l_sore_valid_sante), 2)})"])
    data_baseline.append(['HAD anxiety score', "", "", "", "",
                          f"{round(np.mean(other.score_had_anx), 2)} ({round(np.std(other.score_had_anx), 2)})"])
    data_baseline.append(['HAD depression score', "", "", "", "",
                          f"{round(np.mean(other.score_had_dep), 2)} ({round(np.std(other.score_had_dep), 2)})"])
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
    data_baseline.columns = ['Variable', 'Characteristic', 'All subjects', 'Healthy control', 'OCD patients',
                             'Other disorder']
    data_baseline['p-value'] = p_value_column()
    data_baseline.to_csv('Data_baseline.csv', index=False)


make_data_baseline()


