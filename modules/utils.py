# utils
import pandas as pd
import numpy as np

def get_ref_compound(df,first_feature='LPA_16_0_'):
    first_feature_index = np.where(df.columns==first_feature)[0][0]
    prevalence = df.iloc[:,first_feature_index:].astype(bool).mean()
    return prevalence.idxmax()

def delete_low_prevalence_compound(df, prevalence_threshold, first_feature='LPA_16_0_'):
    first_feature_index = np.where(df.columns==first_feature)[0][0]
    columns = df.iloc[:,:first_feature_index]
    prevalence = df.iloc[:,first_feature_index:].astype(bool).mean()
    compound_left = df.loc[:,prevalence.index[prevalence>prevalence_threshold]]
    df_filter = pd.concat([columns,compound_left],axis=1)
    deleted_compound = prevalence.index[prevalence<=prevalence_threshold].tolist()
    return df_filter, deleted_compound