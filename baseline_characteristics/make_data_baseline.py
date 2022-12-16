import numpy as np
import pandas as pd
import scipy.stats as sps
from datetime import datetime, date

from scipy import stats

""" The redcap export in csv, change the path every time with the correct one"""
redcap_csv = pd.read_csv("../STOCADPinelfollowup_DATA_2022-12-05_1143.csv")
# Subselect patients who performed the tasks
redcap_csv = redcap_csv[(redcap_csv.record_id < 71) & (redcap_csv.redcap_event_name == "baseline_arm_1")]

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

# add variable age in df

hc = hc.assign(age=hc['ddn'].apply(age))
ocd = ocd.assign(age=ocd['ddn'].apply(age))
other = other.assign(age=other['ddn'].apply(age))


def fill_column(final_name, name_in_csv, i, nb_disorders, variable=False):
    if nb_disorders == 3:
        if not variable:
            return ["", final_name, len(redcap_csv[redcap_csv[name_in_csv] == i]), len(hc[hc[name_in_csv] == i]),
                    len(ocd[ocd[name_in_csv] == i]),
                    len(other[other[name_in_csv] == i])]
        else:
            return [final_name, "", len(redcap_csv[redcap_csv[name_in_csv] == i]), len(hc[hc[name_in_csv] == i]),
                    len(ocd[ocd[name_in_csv] == i]),
                    len(other[other[name_in_csv] == i])]
    elif nb_disorders == 2:
        if not variable:
            return ["", final_name, len(hc[hc[name_in_csv] == i]) + len(ocd[ocd[name_in_csv] == i]),
                    len(hc[hc[name_in_csv] == i]),
                    len(ocd[ocd[name_in_csv] == i])]
        else:
            return [final_name, "", len(hc[hc[name_in_csv] == i]) + len(ocd[ocd[name_in_csv] == i]),
                    len(hc[hc[name_in_csv] == i]),
                    len(ocd[ocd[name_in_csv] == i])]


def get_value(characteristic_name, nb_disorders, variable=False):
    data_baseline = pd.read_csv('Data_baseline.csv')
    if not variable:
        characteristic_line = data_baseline[data_baseline['Characteristic'] == characteristic_name]
    else:
        characteristic_line = data_baseline[data_baseline['Variable'] == characteristic_name]

    list_values = []
    if nb_disorders == 3:
        for i in range(3, 6):
            list_values.append(characteristic_line[characteristic_line.columns[i]].astype(int).values[0])
    if nb_disorders == 2:
        for i in range(3, 5):
            list_values.append(characteristic_line[characteristic_line.columns[i]].astype(int).values[0])
    if characteristic_name == "amateur___0":
        print(list_values)
    return list_values


def get_value_opposite(characteristic_name, nb_disorders, variable=False):
    list = get_value(characteristic_name=characteristic_name, nb_disorders=nb_disorders, variable=variable)
    if nb_disorders == 3:
        opposite_list = [len(hc) - list[0], len(ocd) - list[1], len(other) - list[2]]
    else:
        opposite_list = [len(hc) - list[0], len(ocd) - list[1]]
    return opposite_list


def p_value_column(nb_disorders):
    if nb_disorders == 3:
        tab_study = [get_value('Primary education', 3), get_value('Secondary education', 3),
                     get_value('High school diploma', 3), get_value('Vocational training', 3),
                     get_value('BTEC Higher National Diploma', 3), get_value('Bachelor', 3),
                     get_value('Master', 3), get_value('PhD', 3)]

        [tab_study.remove(t) for t in tab_study if t == [0, 0, 0]]
        tab = [" ", round(sps.f_oneway(hc.age, ocd.age, other.age)[1], 3),
               round(sps.chi2_contingency([get_value('Men', 3), get_value('Women', 3)])[1], 3), "",
               "", round(sps.chi2_contingency(tab_study)[1], 3), "", "", "", "", "", "", "", "",
               round(sps.chi2_contingency(
                   [get_value('Single', 3), get_value('In relationship', 3), get_value('Maried', 3),
                    get_value('Divorced', 3),
                    get_value('Widowed', 3)])[1], 3), "", "", "", "", "", ""]
        tab2 = [" ", round(sps.f_oneway(hc.age, ocd.age, other.age)[0], 2),
                round(sps.chi2_contingency([get_value('Men', 3), get_value('Women', 3)])[0], 2), "",
                "", round(sps.chi2_contingency(tab_study)[0], 2), "", "", "", "", "", "", "", "",
                round(sps.chi2_contingency(
                    [get_value('Single', 3), get_value('In relationship', 3), get_value('Maried', 3),
                     get_value('Divorced', 3),
                     get_value('Widowed', 3)])[0], 2), "", "", "", "", "", ""]

        names_list = ['Tobacco', 'Alcohol', 'Caffeine']
        '''drugs = {'Tobacco': 'tabac', 'Alcohol': 'alcool', 'Caffeine': 'cafeine'}
        for key, val in drugs.items():'''
        for name in names_list:
            tab.append(round(sps.chi2_contingency([get_value(name, 3), get_value_opposite(name, 3)])[1], 3))
            tab2.append(round(sps.chi2_contingency([get_value(name, 3), get_value_opposite(name, 3)])[0],
                      2))
        tab.append(round(stats.ttest_ind(get_value('Laterality', 2, True), get_value_opposite('Laterality', 2, True))[1], 3))
        tab2.append(round(stats.ttest_ind(get_value('Laterality', 2, True), get_value_opposite('Laterality', 2, True))[0], 2))
        tab.append(round(stats.ttest_ind(get_value('BMI', 3, True), get_value_opposite('BMI', 3, True))[1], 3))
        tab2.append(round(stats.ttest_ind(get_value('BMI', 3, True), get_value_opposite('BMI', 3, True))[0], 2))
        tab.append(round(stats.ttest_ind(get_value('Poor visual acuity', 3, True), get_value_opposite('Poor visual acuity', 3, True))[0]))
        tab2.append(round(stats.ttest_ind(get_value('Poor visual acuity', 3, True),
                                          get_value_opposite('Poor visual acuity', 3, True))[1]))

        tab.append(round(sps.chi2_contingency([get_value('Satisfied with optical correction (yes)', 3),
                                               get_value_opposite('Satisfied with optical correction (yes)', 3)])[1],
                         3))
        tab2.append(round(sps.chi2_contingency([get_value('Satisfied with optical correction (yes)', 3),
                                                get_value_opposite('Satisfied with optical correction (yes)', 3)])[0],
                          2))
        # ICI
        tab.append(round(sps.chi2_contingency([get_value('jeu d\'échecs', 3),
                                               get_value_opposite('jeu d\'échecs', 3)])[1],
                         3))
        tab2.append(round(sps.chi2_contingency([get_value('jeu d\'échecs', 3),
                                                get_value_opposite('jeu d\'échecs', 3)])[0],
                          2))
        tab.extend([""]*4)
        tab2.extend([""]*4)
        # FIN ICI
        tab.append(
            round(sps.chi2_contingency([get_value('History of epilepsy', 3, variable=True),
                                        get_value_opposite('History of epilepsy', 3, variable=True)])[1], 3))
        tab2.append(
            round(sps.chi2_contingency([get_value('History of epilepsy', 3, variable=True),
                                        get_value_opposite('History of epilepsy', 3, variable=True)])[0], 2))
        tab.append(round(sps.chi2_contingency([[len(ocd[ocd['stimulation'] == 0]), len(ocd[ocd['stimulation'] == 1])], [
            len(other[other['stimulation'] == 0]), len(other[other['stimulation'] == 0])]])[1], 3))
        tab2.append(
            round(sps.chi2_contingency([[len(ocd[ocd['stimulation'] == 0]), len(ocd[ocd['stimulation'] == 1])], [
                len(other[other['stimulation'] == 0]), len(other[other['stimulation'] == 0])]])[0], 2))

        tab.extend([""] * 5)
        tab2.extend([""] * 5)

        for name2 in ['maudsley_score', 'eq5d5l_sore_valid_sante']:
            ocd_name = np.array(ocd[name2])
            ocd_tab = ocd_name[~np.isnan(ocd_name)]
            other_name = np.array(other[name2])
            other_tab = other_name[~np.isnan(other_name)]
            tab.append(round(sps.ttest_ind(ocd_tab, other_tab)[1], 3))
            tab2.append(round(sps.ttest_ind(ocd_tab, other_tab)[0], 2))
        tab.extend([""] * 8)
        tab2.extend([""] * 8)

    else:
        tab_study = [get_value('Primary education', 2), get_value('Secondary education', 2),
                     get_value('High school diploma', 2), get_value('Vocational training', 2),
                     get_value('BTEC Higher National Diploma', 2), get_value('Bachelor', 2),
                     get_value('Master', 2), get_value('PhD', 2)]

        [tab_study.remove(t) for t in tab_study if t == [0, 0]]
        tab = [" ", round(stats.ttest_ind(hc.age, ocd.age)[1], 3),
               round(stats.ttest_ind(get_value('Men', 2), get_value('Women', 2))[1], 3), "",
               "", round(sps.chi2_contingency(tab_study)[1], 3), "", "", "", "", "", "", "", "",
               round(sps.chi2_contingency(
                   [get_value('Single', 2), get_value('In relationship', 2), get_value('Maried', 2),
                    get_value('Divorced', 2),
                    get_value('Widowed', 2)])[1], 3), "", "", "", "", "", ""]
        tab2 = [" ", round(stats.ttest_ind(hc.age, ocd.age)[0], 2),
                round(sps.ttest_ind(get_value('Men', 2), get_value('Women', 2))[0], 2), "",
                "", round(sps.chi2_contingency(tab_study)[0], 2), "", "", "", "", "", "", "", "",
                round(sps.chi2_contingency(
                    [get_value('Single', 2), get_value('In relationship', 2), get_value('Maried', 2),
                     get_value('Divorced', 2),
                     get_value('Widowed', 2)])[0], 2), "", "", "", "", "", ""]

        drugs = {'Tobacco': 'tabac', 'Alcohol': 'alcool', 'Caffeine': 'cafeine'}
        for key, val in drugs.items():
            tab_values = get_value(key, 2)
            l1 = [0] * (len(hc) - tab_values[0]) + [1] * tab_values[0]
            l2 = [0] * (len(ocd) - tab_values[1]) + [1] * tab_values[1]
            tab.append(round(stats.ttest_ind(l1, l2)[1], 3))
            tab2.append(round(stats.ttest_ind(l1, l2)[0], 2))
        tab.append(round(stats.ttest_ind(get_value('Laterality', 2, True), get_value_opposite('Laterality', 2, True))[1], 3))
        tab2.append(round(stats.ttest_ind(get_value('Laterality', 2, True), get_value_opposite('Laterality', 2, True))[0], 2))

        tab.append(round(stats.ttest_ind(get_value('BMI', 2, True), get_value_opposite('BMI', 2, True))[1], 3))
        tab2.append(round(stats.ttest_ind(get_value('BMI', 2, True), get_value_opposite('BMI', 2, True))[0], 2))


        tab.append(round(stats.ttest_ind(get_value('Poor visual acuity', 2, True), get_value_opposite('Poor visual acuity', 2, True))[1],
                         2))
        tab2.append(
            round(stats.ttest_ind(get_value('Poor visual acuity', 2, True), get_value_opposite('Poor visual acuity', 2, True))[0],
                  2))

        tab.append(round(stats.ttest_ind(get_value('Satisfied with optical correction (yes)', 2),
                                       get_value_opposite('Satisfied with optical correction (yes)', 2))[1],
                         3))
        tab2.append(round(stats.ttest_ind(get_value('Satisfied with optical correction (yes)', 2),
                                        get_value_opposite('Satisfied with optical correction (yes)', 2))[0],
                          2))
        tab.append(round(sps.chi2_contingency([get_value('jeu d\'échecs', 2),
                                               get_value_opposite('jeu d\'échecs', 2)])[1],
                         3))
        tab2.append(round(sps.chi2_contingency([get_value('jeu d\'échecs', 2),
                                                get_value_opposite('jeu d\'échecs', 2)])[0],
                          2))
        tab.extend([""]*4)
        tab2.extend([""]*4)
        tab.append(
            round(sps.ttest_ind(get_value('History of epilepsy', 2, variable=True),
                                get_value_opposite('History of epilepsy', 2, variable=True))[1], 3))
        tab2.append(
            round(sps.ttest_ind(get_value('History of epilepsy', 2, variable=True),
                                get_value_opposite('History of epilepsy', 2, variable=True))[0], 2))
        tab.extend([""] * 14)
        tab2.extend([""] * 14)

    return tab2, tab


def check_score(tab):
    return list(filter(lambda x: x != 999, tab['eq5d5l_sore_valid_sante']))


def make_data_baseline(nb_disorders):
    if nb_disorders == 3:
        data_baseline = [['', "", f"(n = {len(redcap_csv['record_id'])})", f"(n = {len(hc)})", f"(n = {len(ocd)})",
                          f"(n = {len(other)})"],
                         ['Age', "",
                          f"{round(int(np.mean(redcap_csv['ddn'].apply(age))), 2)} ({round(int(np.std(redcap_csv['ddn'].apply(age))), 2)})",
                          f"{round(int(np.mean(hc.age)), 2)} ({round(int(np.std(hc.age)), 2)})",
                          f"{round(int(np.mean(ocd.age)), 2)} ({round(int(np.std(ocd.age)), 2)})",
                          f"{round(int(np.mean(other.age)), 2)} ({round(int(np.std(other.age)), 2)})"],
                         ['Gender', "", "", "", ""],
                         ["", 'Men', repart_sex(redcap_csv)[1], repart_sex(hc)[1], repart_sex(ocd)[1],
                          repart_sex(other)[1]],
                         ["", 'Women', repart_sex(redcap_csv)[0], repart_sex(hc)[0], repart_sex(ocd)[0],
                          repart_sex(other)[0]], ['Educational level', "", "", "", "", ""]]
        study_name = ['Primary education', 'Secondary education', 'High school diploma', 'Vocational training',
                      'BTEC Higher National Diploma', 'Bachelor', 'Master', 'PhD']
        for i in np.arange(0, 8):
            data_baseline.append(fill_column(f'{study_name[i]}', 'etudes', i, nb_disorders))
        data_baseline.append(['Marital Status', "", "", "", ""])
        marital = ['Single', 'In relationship', 'Maried', 'Divorced', 'Widowed']
        for i in np.arange(0, 5):
            data_baseline.append(fill_column(f'{marital[i]}', 'matrimoniale', i, nb_disorders))
        data_baseline.append(['Psycho active drugs', "", "", "", ""])
        drugs = {'Tobacco': 'tabac', 'Alcohol': 'alcool', 'Caffeine': 'cafeine'}
        for key, val in drugs.items():
            data_baseline.append(fill_column(key, val, 1, nb_disorders))
        data_baseline.append(fill_column('Laterality', 'lateralite', 1, nb_disorders, variable=True))
        data_baseline.append(['BMI', "", round(int(np.mean(pd.concat([hc['imc'], ocd['imc'], other['imc']]))), 2), int(np.mean(hc['imc'])), int(np.mean(ocd['imc'])), round(int(np.mean(other['imc'])), 2)])
        data_baseline.append(fill_column('Poor visual acuity', 'acuite', 1, 3, variable=True))
        data_baseline.append(fill_column('Satisfied with optical correction (yes)', 'correction', 1, nb_disorders=3))
        data_baseline.append(['Amateur', '', '', '', ''])
        amateur = ['jeu d\'échecs', 'art', 'cinéma', 'histoire']
        for i in np.arange(0, 4):
            data_baseline.append(fill_column(f'{amateur[i]}', f'amateur___{i}', 1, nb_disorders))
        data_baseline.append(fill_column('History of epilepsy', 'epilepsie', 1, 3, variable=True))
        data_baseline.append(['Brain stimulation', "", len(redcap_csv[redcap_csv['stimulation'] == 1]), "",
                              len(ocd[ocd['stimulation'] == 1]),
                              len(other[other['stimulation'] == 1])])
        data_baseline.append(['Brain stimulation techniques', "", "", "", "", ""])
        technique_name = ['rTMS', 'tDCS', 'deep TMS', 'TCES']
        for i in np.arange(0, 4):
            data_baseline.append(
                ["", technique_name[i], len(redcap_csv[redcap_csv['technique_stimulation_ni'] == i]), "",
                 len(ocd[ocd['technique_stimulation_ni'] == i]),
                 len(other[other['technique_stimulation_ni'] == i])])
        data_baseline.append(
            ['Maudsley score', "", "", "",
             f"{round(int(np.mean(ocd.maudsley_score)), 2)} ({round(int(np.std(ocd.maudsley_score)), 2)})",
             f"{round(int(np.mean(other.maudsley_score)), 2)} ({round(int(np.std(other.maudsley_score)), 2)})"])
        # data_baseline.append(
        #   ['Health state score', "", "", "",
        #   f"{round(np.mean(ocd.eq5d5l_score_tot), 2)} ({round(np.std(ocd.eq5d5l_score_tot), 2)})",
        #   f"{round(np.mean(other.eq5d5l_score_tot), 2)} ({round(np.std(other.eq5d5l_score_tot), 2)})"])

        data_baseline.append(
            ['VAS score', "", "", "",
             f"{round(int(np.nanmean(check_score(ocd))), 2)} ({round(int(np.nanstd(check_score(ocd))), 2)})",
             f"{round(int(np.nanmean(check_score(other))), 2)} ({round(int(np.nanstd(check_score(other))), 2)})"])
        data_baseline.append(['HAD anxiety score', "", "", "", "",
                              f"{round(int(np.nanmean(other.score_had_anx)), 2)} ({round(int(np.nanstd(other.score_had_anx)), 2)})"])
        data_baseline.append(['HAD depression score', "", "", "", "",
                              f"{round(int(np.nanmean(other.score_had_dep)), 2)} ({round(int(np.nanstd(other.score_had_dep)), 2)})"])
        data_baseline.append(['Y-BOCS score', "", "", "", "", ""])
        data_baseline.append(["", "< 7", "", "", len(ocd[ocd.ybocs_score_tot < 7]), ""])
        data_baseline.append(
            ["", "8 - 15", "", "", len(ocd[(ocd.ybocs_score_tot >= 8) & (ocd.ybocs_score_tot <= 15)]), ""])
        data_baseline.append(
            ["", "16 - 23", "", "", len(ocd[(ocd.ybocs_score_tot >= 16) & (ocd.ybocs_score_tot <= 23)]), ""])
        data_baseline.append(
            ["", "24 - 31", "", "", len(ocd[(ocd.ybocs_score_tot >= 24) & (ocd.ybocs_score_tot <= 31)]), ""])
        data_baseline.append(
            ["", "32 - 40", "", "", len(ocd[(ocd.ybocs_score_tot >= 32) & (ocd.ybocs_score_tot <= 40)]), ""])
        data_baseline = pd.DataFrame(data_baseline)
        data_baseline.columns = ['Variable', 'Characteristic', 'All subjects', 'Healthy control', 'OCD patients',
                                 'Other disorder']
        data_baseline.to_csv('Data_baseline.csv', index=False)
        data_baseline['t'], data_baseline['p'] = p_value_column(3)

        data_baseline.to_csv('Data_baseline.csv', index=False)

    elif nb_disorders == 2:
        data_baseline = [["", "", f"(n = {len(hc) + len(ocd)})", f"(n = {len(hc)})", f"(n = {len(ocd)})"],
                         ['Age', "",
                          f"{round(int(np.mean(redcap_csv['ddn'].apply(age))), 2)} ({round(int(np.std(redcap_csv['ddn'].apply(age))), 2)})",
                          f"{round(int(np.mean(hc.age)), 2)} ({round(int(np.std(hc.age)), 2)})",
                          f"{round(int(np.mean(ocd.age)), 2)} ({round(int(np.std(ocd.age)), 2)})"],
                         ['Gender', "", "", "", ""],
                         ["", 'Men', repart_sex(hc)[1] + repart_sex(ocd)[1], repart_sex(hc)[1], repart_sex(ocd)[1]],
                         ["", 'Women', repart_sex(hc)[0] + repart_sex(ocd)[0], repart_sex(hc)[0], repart_sex(ocd)[0]],
                         ['Educational level', "", "", "", ""]]
        study_name = ['Primary education', 'Secondary education', 'High school diploma', 'Vocational training',
                      'BTEC Higher National Diploma', 'Bachelor', 'Master', 'PhD']
        for i in np.arange(0, 8):
            data_baseline.append(fill_column(f'{study_name[i]}', 'etudes', i, nb_disorders))
        data_baseline.append(['Marital Status', "", "", "", ""])
        marital = ['Single', 'In relationship', 'Maried', 'Divorced', 'Widowed']
        for i in np.arange(0, 5):
            data_baseline.append(fill_column(f'{marital[i]}', 'matrimoniale', i, nb_disorders))
        data_baseline.append(['Psycho active drugs', "", "", "", ""])
        drugs = {'Tobacco': 'tabac', 'Alcohol': 'alcool', 'Caffeine': 'cafeine'}
        for key, val in drugs.items():
            data_baseline.append(fill_column(key, val, 1, nb_disorders))
        data_baseline.append(fill_column('Laterality', 'lateralite', 1, nb_disorders, variable=True))
        data_baseline.append(['BMI', "", round(float(np.mean(pd.concat([hc['imc'], ocd['imc']]))), 2), np.mean(hc['imc']), np.mean(ocd['imc'])])
        data_baseline.append(fill_column('Poor visual acuity', 'acuite', 1, nb_disorders, variable=True))
        data_baseline.append(fill_column('Satisfied with optical correction (yes)', 'correction', 1, nb_disorders))
        data_baseline.append(["Amateur", "", "", "", ""])
        amateur = ['jeu d\'échecs', 'art', 'cinéma', 'histoire']
        for i in np.arange(0, 4):
            data_baseline.append(fill_column(f'{amateur[i]}', f'amateur___{i}', 1, nb_disorders))
        data_baseline.append(fill_column('History of epilepsy', 'epilepsie', 1, nb_disorders, variable=True))
        data_baseline.append(['Brain stimulation', "", len(hc[hc['stimulation'] == 1]) + len(ocd[ocd['stimulation'] == 1]), "",
                              len(ocd[ocd['stimulation'] == 1])])
        data_baseline.append(['Brain stimulation techniques', "", "", "", ""])
        technique_name = ['rTMS', 'tDCS', 'deep TMS', 'TCES']
        for i in np.arange(0, 4):
            data_baseline.append(
                ["", technique_name[i], len(redcap_csv[redcap_csv['technique_stimulation_ni'] == i]), "",
                 len(ocd[ocd['technique_stimulation_ni'] == i])])
        data_baseline.append(
            ['Maudsley score', "", "", "",
             f"{round(int(np.mean(ocd.maudsley_score)), 2)} ({round(int(np.std(ocd.maudsley_score)), 2)})"])
        # data_baseline.append(
        #   ['Health state score', "", "", "",
        #   f"{round(np.mean(ocd.eq5d5l_score_tot), 2)} ({round(np.std(ocd.eq5d5l_score_tot), 2)})",
        #   f"{round(np.mean(other.eq5d5l_score_tot), 2)} ({round(np.std(other.eq5d5l_score_tot), 2)})"])

        data_baseline.append(
            ['VAS score', "", "", "",
             f"{round(int(np.nanmean(check_score(ocd))), 2)} ({round(int(np.nanstd(check_score(ocd))), 2)})"])
        data_baseline.append(['Y-BOCS score', "", "", "", ""])
        data_baseline.append(["", "< 7", "", "", len(ocd[ocd.ybocs_score_tot < 7])])
        data_baseline.append(
            ["", "8 - 15", "", "", len(ocd[(ocd.ybocs_score_tot >= 8) & (ocd.ybocs_score_tot <= 15)])])
        data_baseline.append(
            ["", "16 - 23", "", "", len(ocd[(ocd.ybocs_score_tot >= 16) & (ocd.ybocs_score_tot <= 23)])])
        data_baseline.append(
            ["", "24 - 31", "", "", len(ocd[(ocd.ybocs_score_tot >= 24) & (ocd.ybocs_score_tot <= 31)])])
        data_baseline.append(
            ["", "32 - 40", "", "", len(ocd[(ocd.ybocs_score_tot >= 32) & (ocd.ybocs_score_tot <= 40)])])

        data_baseline = pd.DataFrame(data_baseline)
        data_baseline.columns = ['Variable', 'Characteristic', 'All subjects', 'Healthy control', 'OCD patients']
        data_baseline.to_csv('Socio_Demo_HC_OCD.csv', index=False)
        data_baseline['t'], data_baseline['p'] = p_value_column(2)
        data_baseline.to_csv('Socio_Demo_HC_OCD.csv', index=False)


make_data_baseline(3)
print(check_score(ocd))
