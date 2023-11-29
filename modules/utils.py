# utils
import pandas as pd
import numpy as np

def get_ref_compound(df,first_feature='LPA_16_0_'):
    first_feature_index = np.where(df.columns==first_feature)[0][0]
    prevalence = df.iloc[:,first_feature_index:].astype(bool).mean()
    return prevalence.idxmax()