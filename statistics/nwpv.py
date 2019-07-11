from .statistics import STAT
from scipy import stats
import numpy as np

class nwpv:

	def _preprocessing(self, min_adj=1e-16, max_adj=0.9999999999999999):
		#####Minvalue adjustment
		self.st_df['mtest_pvalue'] = self.st_df['mtest_pvalue'].apply(lambda x: min_adj if x<min_adj else x)
		self.st_df['ttest_pvalue'] = self.st_df['ttest_pvalue'].apply(lambda x: min_adj if x<min_adj else x)
		self.st_df['ranksums_pvalue'] = self.st_df['ranksums_pvalue'].apply(lambda x: min_adj if x<min_adj else x)

		#####Maxvalue adjustment
		self.st_df['mtest_pvalue'] = self.st_df['mtest_pvalue'].apply(lambda x: max_adj if x==1 else x)
		self.st_df['ttest_pvalue'] = self.st_df['ttest_pvalue'].apply(lambda x: max_adj if x==1 else x)
		self.st_df['ranksums_pvalue'] = self.st_df['ranksums_pvalue'].apply(lambda x: max_adj if x==1 else x)

		#####Z transform
		self.st_df['mtest_pvalue_z'] = self.st_df['mtest_pvalue'].apply(lambda x : stats.norm.ppf(1-x))
		self.st_df['ttest_pvalue_z'] = self.st_df['ttest_pvalue'].apply(lambda x : stats.norm.ppf(1-x))
		self.st_df['ranksums_pvalue_z'] = self.st_df['ranksums_pvalue'].apply(lambda x : stats.norm.ppf(1-x))

	def _combined(self, st):
		#####Scaling (StandardScaler)
		self.st_df['mtest_pvalue_scaled'] = (self.st_df['mtest_pvalue_z'] - self.st_df['mtest_pvalue_z'].mean()) / self.st_df['mtest_pvalue_z'].std()
		self.st_df['ttest_pvalue_scaled'] = (self.st_df['ttest_pvalue_z'] - self.st_df['ttest_pvalue_z'].mean()) / self.st_df['ttest_pvalue_z'].std()
		self.st_df['ranksums_pvalue_scaled'] = (self.st_df['ranksums_pvalue_z'] - self.st_df['ranksums_pvalue_z'].mean()) / self.st_df['ranksums_pvalue_z'].std()

		#####Combined zvalue by mean
		self.st_df['combined_pvalue'] = self.st_df['mtest_pvalue_scaled']+self.st_df['ttest_pvalue_scaled']+self.st_df['ranksums_pvalue_scaled']
		self.st_df['combined_pvalue'] = self.st_df['combined_pvalue'].apply(lambda x : float(x)/float(np.sqrt(3.0)))

		#####Transform to P-value
		self.st_df['combined_pvalue'] = self.st_df['combined_pvalue'].apply(lambda x : stats.norm.sf(x)*2)
		self.st_df['combined_pvalue'] = self.st_df['combined_pvalue'].apply(lambda x : float("{:.5f}".format(x)))
		self.st_df = st.storey_fdr(self.st_df, p_name='combined_pvalue')

	def get_result(self):
		return self.st_df[['FC','mtest_pvalue', 'ttest_pvalue', 'ranksums_pvalue', 'combined_pvalue', 'combined_pvalue_adj']]

	def __init__(self, df, test1, control):
		st = STAT(df, test1, control)
		assert np.prod([x in df.columns.tolist() for x in test1]) and np.prod([x in df.columns.tolist() for x in control]), "Some samples do not exist in DataFrame"
		assert len(test1)>=3 and len(control)>=3, "Too small size of samples(Control or Test)"

		self.st_df = st.statistics_result()
		self._preprocessing()
		self._combined(st)
