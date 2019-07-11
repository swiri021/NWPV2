from statistics.nwpv import nwpv
import pandas as pd
import numpy as np


#Input must be Pandas DataFrame
df = pd.read_csv('Your_data.csv')

#Test input
test = ['Sample1', 'Sample2', 'Sample3',....]

#Control input
control = ['SampleC1', 'SampleC2', 'SampleC3',....]

#Call the class
nwpv = nwpv(df, test, control,)

#Result
print nwpv.get_result()
