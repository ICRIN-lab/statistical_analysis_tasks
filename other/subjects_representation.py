import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

redcap_csv = pd.read_csv('/Users/melissamarius/Downloads/STOCADPinelfollowup_DATA_2022-05-30_1600.csv')
resume = redcap_csv[['ddn', 'sexe']]


def age(born):
    born = datetime.strptime(born, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month,
                                      today.day) < (born.month,
                                                    born.day))


print(resume['ddn'].apply(age), resume)