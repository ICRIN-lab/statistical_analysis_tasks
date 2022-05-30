import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

redcap_csv = pd.read_csv("D:\Telechargement\STOCADPinelfollowup_DATA_2022-05-30_2240.csv")


def age(born):
    born = datetime.strptime(born, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month,
                                      today.day) < (born.month,
                                                    born.day))


resume = pd.DataFrame({'age': redcap_csv['ddn'].apply(age), 'sexe':redcap_csv['sexe'], 'disorder':redcap_csv['diagnostic_principal']})
#plt.hist(resume.age)
#plt.show()
plt.pie([len(resume.sexe[resume.sexe==0])/len(resume.sexe)*100,len(resume.sexe[resume.sexe==1])/len(resume.sexe)*100],labels=['Femme','Homme'])
plt.show()
print(resume)
