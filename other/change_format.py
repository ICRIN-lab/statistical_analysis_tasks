import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def correct_format(path):  # changer correct en result et True/False en 1/0
    df = pd.read_csv(path, encoding='ISO-8859-1')
    if (df['correct'][1] == True) or (df['correct'][1] == False):
        df['correct'] = np.where(df['correct'] == True, 1, 0)
    df.rename(columns={'correct': 'result'}, inplace=True)
    df.to_csv(path, index=False)
    print('Le format a été changé')


def change_id_candidate(path_file, id_candidate):
    tab = pd.read_csv(path_file, encoding='ISO-8859-1')
    tab['id_candidate'] = id_candidate
    tab.to_csv(path_file, index=False)


list_image = ['img_7_0.png', 'img_14_3.png', 'img_10_6.png', 'img_17_0.png', 'img_3_3.png', 'img_2_0.png',
              'img_13_1.png',
              'img_19_4.png', 'img_13_0.png', 'img_8_3.png', 'img_11_2.png', 'img_15_1.png', 'img_0_5.png',
              'img_5_3.png',
              'img_3_1.png', 'img_19_1.png', 'img_13_2.png', 'img_9_2.png', 'img_15_0.png', 'img_16_5.png',
              'img_2_2.png',
              'img_16_1.png', 'img_4_3.png', 'img_4_0.png', 'img_18_4.png', 'img_18_2.png', 'img_17_2.png',
              'img_3_4.png',
              'img_10_0.png', 'img_3_2.png', 'img_10_4.png', 'img_9_0.png', 'img_4_6.png', 'img_15_4.png',
              'img_2_5.png',
              'img_7_5.png', 'img_13_5.png', 'img_17_5.png', 'img_16_6.png', 'img_12_1.png', 'img_18_0.png',
              'img_3_0.png',
              'img_7_2.png', 'img_10_2.png', 'img_11_5.png', 'img_6_0.png', 'img_6_3.png', 'img_19_0.png',
              'img_11_0.png',
              'img_6_4.png', 'img_14_1.png', 'img_8_1.png', 'img_12_3.png', 'img_18_1.png', 'img_8_2.png',
              'img_1_6.png',
              'img_1_2.png', 'img_8_0.png', 'img_0_3.png', 'img_11_1.png', 'img_2_3.png', 'img_17_3.png', 'img_9_3.png',
              'img_17_1.png', 'img_1_0.png', 'img_12_4.png', 'img_1_3.png', 'img_16_2.png', 'img_19_5.png',
              'img_6_2.png',
              'img_5_5.png', 'img_7_6.png', 'img_5_2.png', 'img_14_0.png', 'img_4_1.png', 'img_0_2.png', 'img_4_2.png',
              'img_1_1.png', 'img_0_4.png', 'img_14_2.png', 'img_15_2.png', 'img_5_0.png', 'img_13_4.png',
              'img_14_4.png',
              'img_19_2.png', 'img_5_4.png', 'img_11_3.png', 'img_6_1.png', 'img_0_0.png', 'img_12_0.png',
              'img_16_0.png',
              'img_2_1.png', 'img_18_5.png', 'img_9_4.png', 'img_12_6.png', 'img_15_3.png', 'img_8_5.png',
              'img_7_4.png',
              'img_10_1.png', 'img_9_1.png']

tab = []
for i in range(0, len(list_image)):
    num = str(list_image[i])[4:6]
    if num.find('_') > 0:
        tab.append([i, 'shocking'])
    else:
        tab.append([i, 'non-shocking'])
tab = pd.DataFrame(tab)
tab.columns = ['no_trial', 'type']

tab.to_csv('csv_block_shocking.csv',index=False,header=True)