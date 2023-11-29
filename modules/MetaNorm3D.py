# MetaNorm3D module
import numpy as np
import pandas as pd

def totalsum_norm(df, first_feature_index):
    row_sum = df.iloc[:, first_feature_index:].sum(axis=1)
    df.iloc[:, first_feature_index:] = df.iloc[:, first_feature_index:].divide(row_sum, axis=0).fillna(0)
    return df

def section_norm(df, compound, first_feature_index):
    data = df[df.columns[:first_feature_index].tolist() + [compound]]
    norm_factor = data.groupby('tissue_id')[compound].median().median() / data.groupby('tissue_id')[compound].median()
    norm_factor.name = 'norm_factor'
    data = data.merge(norm_factor, on='tissue_id')
    data['result'] = np.array(data[compound]) * np.array(data['norm_factor'])
    return data

class MetaNorm3D:
    def __init__(self, df, compound, first_feature='LPA_16_0_'):
        self.df = df
        self.compound = compound
        self.first_feature = first_feature
        self.first_feature_index = np.where(df.columns==first_feature)[0][0]

    def totalsum_norm(self):
        row_sum = self.df.iloc[:, self.first_feature_index:].sum(axis=1)
        self.df.iloc[:, self.first_feature_index:] = self.df.iloc[:, self.first_feature_index:].divide(row_sum, axis=0).fillna(0)
        return self.df

    def section_norm(self):
        data = self.df[self.df.columns[:self.first_feature_index].tolist() + [self.compound]]
        norm_factor = data.groupby('tissue_id')[self.compound].median().median() / data.groupby('tissue_id')[self.compound].median()
        norm_factor.name = 'norm_factor'
        data = data.merge(norm_factor, on='tissue_id')
        data['result'] = np.array(data[self.compound]) * np.array(data['norm_factor'])
        return data


        
    