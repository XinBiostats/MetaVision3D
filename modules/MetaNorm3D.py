# MetaNorm3D module
import numpy as np
import pandas as pd

def totalsum_norm(df, first_feature_index):
    delete_row = np.where(df.iloc[:,first_feature_index:].sum(axis=1)==0)[0]
    df = df.drop(delete_row)
    row_sum = df.iloc[:, first_feature_index:].sum(axis=1)
    df.iloc[:, first_feature_index:] = df.iloc[:, first_feature_index:].divide(row_sum, axis=0).fillna(0)
    return df

def section_norm(df, compound, first_feature_index):
    data = df[df.columns[:first_feature_index].tolist() + [compound]]
    denominator = data.groupby('tissue_id')[compound].median()
    numerator = denominator.median()
    denominator[denominator==0] = numerator
    
    if (denominator==0).any():
        print('Skipping section normalization due to dividing by 0')
        data['result'] = data[compound]
        return data
    else:
        norm_factor = numerator/denominator
        norm_factor.name = 'norm_factor'
        data = data.merge(norm_factor, on='tissue_id')
        data['result'] = np.array(data[compound]) * np.array(data['norm_factor'])
        return data
    
def no_norm(df, compound, first_feature_index):
    delete_row = np.where(df.iloc[:,first_feature_index:].sum(axis=1)==0)[0]
    df = df.drop(delete_row)
    data = df[df.columns[:first_feature_index].tolist() + [compound]].copy()
    data['result'] = data[compound]
    return data

class MetaNorm3D:
    def __init__(self, df, compound, first_feature='LPA_16_0_'):
        self.df = df
        self.data = None
        self.compound = compound
        self.first_feature = first_feature
        self.first_feature_index = np.where(df.columns==first_feature)[0][0]

    def totalsum_norm(self):
        delete_row = np.where(self.df.iloc[:,self.first_feature_index:].sum(axis=1)==0)[0]
        self.df = self.df.drop(delete_row)
        row_sum = self.df.iloc[:, self.first_feature_index:].sum(axis=1)
        self.df.iloc[:, self.first_feature_index:] = self.df.iloc[:, self.first_feature_index:].divide(row_sum, axis=0).fillna(0)
        return self.df

    def section_norm(self):
        self.data = self.df[self.df.columns[:self.first_feature_index].tolist() + [self.compound]].copy()
        denominator = self.data.groupby('tissue_id')[self.compound].median()
        numerator = denominator.median()
        denominator[denominator==0] = numerator
        norm_factor = numerator/denominator
        if (denominator==0).any():
            print('Skipping section normalization due to dividing by 0')
            self.data.loc[:,'result'] = self.data[self.compound]
            return self.data
        else:
            norm_factor.name = 'norm_factor'
            self.data = self.data.merge(norm_factor, on='tissue_id')
            self.data.loc[:,'result'] = np.array(self.data[self.compound]) * np.array(self.data['norm_factor'])
            return self.data


    def no_norm(self):
        delete_row = np.where(self.df.iloc[:,self.first_feature_index:].sum(axis=1)==0)[0]
        self.df = self.df.drop(delete_row)
        self.data = self.df[self.df.columns[:self.first_feature_index].tolist() + [self.compound]].copy()
        self.data['result'] = self.data[self.compound]
        return self.data
    