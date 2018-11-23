import sys, os
import pandas as pd
import numpy as np

from bclibs.split import print_split

# Task 1: Using to_csv of pd
print_split("Task 1: Test to_csv")
df = pd.DataFrame(np.random.randn(6,3))
print(df.head())
df.to_csv('pd.cvs')


