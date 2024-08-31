# MetaNorm3D module
import numpy as np
import pandas as pd

# def totalsum_norm(df, first_feature):
#     first_feature_index = np.where(df.columns==first_feature)[0][0]
#     row_sum = df.iloc[:, first_feature_index:].sum(axis=1)
#     non_zero_row_indices = np.where(row_sum != 0)[0]
#     df.iloc[non_zero_row_indices, first_feature_index:] = df.iloc[non_zero_row_indices,first_feature_index:].divide(row_sum.iloc[non_zero_row_indices],axis=0).fillna(0)
#     return df

# def section_norm(df, first_feature):
#     compounds = df.columns.tolist()[np.where(df.columns==first_feature)[0][0]:]
#     denominator = df.groupby('tissue_id')[compounds].median()
#     numerator = denominator.median()
#     scale_factor = numerator.div(denominator).replace([np.nan,np.inf],1)
#     df_merged = df.merge(scale_factor, on='tissue_id', suffixes=('', '_adj'))
#     for compound in compounds:
#         df_merged[compound] *= df_merged[f'{compound}_adj']
#     df_merged.drop(columns=[f'{compound}_adj' for compound in compounds], inplace=True)
#     return df_merged
    

class MetaNorm3D:
    def __init__(self, df, first_feature='LPA_16_0_'):
        self.df = df
        self.data = None
        self.first_feature = first_feature

    def totalsum_norm(self):
        first_feature_index = np.where(self.df.columns==self.first_feature)[0][0]
        row_sum = self.df.iloc[:, first_feature_index:].sum(axis=1)
        non_zero_row_indices = np.where(row_sum != 0)[0]
        self.df.iloc[non_zero_row_indices, first_feature_index:] = self.df.iloc[non_zero_row_indices,first_feature_index:].divide(row_sum.iloc[non_zero_row_indices],axis=0).fillna(0)
        return self.df

    def section_norm(self):
        compounds = self.df.columns.tolist()[np.where(self.df.columns==self.first_feature)[0][0]:]
        denominator = self.df.groupby('tissue_id')[compounds].median()
        numerator = denominator.median()
        scale_factor = numerator.div(denominator).replace([np.nan,np.inf],1)
        self.df = self.df.merge(scale_factor, on='tissue_id', suffixes=('', '_adj'))
        for compound in compounds:
            self.df[compound] *= self.df[f'{compound}_adj']
        self.df.drop(columns=[f'{compound}_adj' for compound in compounds], inplace=True)
        return self.df

    