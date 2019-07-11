# NWPV2
Method of Combined P-value to identify Differential Expressed Gene in dataset

# Reference
[Optimally weighted Z-test is a powerful method for combining probabilities in meta-analysis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3135688/)

# Example :
```Python
from statistics.nwpv import nwpv
import pandas as pd
import numpy as np


#Input must be Pandas DataFrame
df = pd.read_csv('Your_data.csv')

#Test input (Size >= 3)
test = ['Sample1', 'Sample2', 'Sample3',....]

#Control input (Size >= 3)
control = ['SampleC1', 'SampleC2', 'SampleC3',....]

#Call the class
nwpv = nwpv(df, test, control)

#Result
print nwpv.get_result()
```
