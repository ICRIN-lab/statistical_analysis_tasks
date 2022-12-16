import pandas as pd
import numpy as np
from random import randint

df = pd.DataFrame({'A': [randint(1, 9) for x in range(10)],
                   'B': [randint(1, 9)*10 for x in range(10)],
                   'C': [randint(1, 9)*100 for x in range(10)]})

print(df[(df["A"] < 5) & (df["B"] < 50)])

L = [[4, 6, 8], [5, 2, 0], [3, 2, 0]]
print(np.nanmean(L, axis=0))

L = [4, 6, 2]

### SUCCESS RATE

# SYMMETRY DONE
# WIT DONE
# LUCIFER DONE
# SEVEN_DIFF DONE

# PER BLOCK  ?
# EASY, YLIM

