import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

redcap_csv = pd.read_csv('/Users/melissamarius/Downloads/STOCADPinelfollowup_DATA_2022-05-30_1600.csv')


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
    plt.show()
    print("L'age moyen est :", np.mean(resume.age), "ans , le maximum est de ", max(resume.age), "ans et le minimum est de ",
          min(resume.age), "ans")

    # Age moyen selon les groupes
    plt.title("Age moyen pour selon les groupes")
    plt.boxplot([resume_no_disorder.age, resume_disorder.age])
    plt.xticks(np.array([1, 2]), ['No-disorder', "Disorder"])
    plt.show()


def Repartition_sexe():
    # Répartion du sexe dans l'échantillion entier
    plt.title("Répartition du sexe pour l'échantillon en entier")
    plt.pie([len(resume.sexe[resume.sexe == 0]) / len(resume.sexe) * 100,
             len(resume.sexe[resume.sexe == 1]) / len(resume.sexe) * 100], labels=['Femme', 'Homme'], autopct='%1.1f%%')
    plt.show()

    # Répartion selon les groupes
    group = [resume_no_disorder, resume_disorder, resume_toc]
    men_means = [repart_sexe(df)[1] for df in group]
    women_means = [repart_sexe(df)[0] for df in group]
    labels = ['No_disorder', 'All disorder', "Toc"]
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, men_means, width, label='Men')
    rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
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
    plt.show()


plt.title('Répartition des sujets')
plt.pie([len(resume_no_disorder), len(resume_disorder), len(resume_toc)], labels=['No_disorder', 'All disorder', 'Toc'],
        autopct='%1.1f%%')
plt.show()
Repartition_sexe()
Repartition_age()
