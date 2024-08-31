# utils
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from skimage import filters, morphology, img_as_float,exposure,measure

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

def make_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        
def flip_axis(df,flipud=False,fliplr=False):
    if flipud:
        df.x = -1*df.x
    if fliplr:
        df.y = -1*df.y
    return df
    
def delete_inferior_tissues(df,inferior_tissues_id,first_feature='LPA_16_0',reverse=False):
    features_to_reset = df.columns[np.where(df.columns==first_feature)[0][0]:]
    if reverse:
        n_tissues = len(df['tissue_id'].unique())
        inferior_tissues_id = [n_tissues-i+1 for i in inferior_tissues_id]
        
    mask = df['tissue_id'].isin(inferior_tissues_id)
    df.loc[mask, features_to_reset] = 0
    
    return df

def get_shell_mask(shell_matrix, gaussian_sigma=1, closing_disk_radius=5):
    nslice = shell_matrix.shape[0]
    mask = np.zeros_like(shell_matrix,dtype=np.uint8)
    for i in tqdm(range(nslice)):
        img = shell_matrix[i]
        
        #shell
        img_rescale = exposure.rescale_intensity(img)
        img_gauss = filters.gaussian(img_rescale, sigma=gaussian_sigma)
        img_binary = img_gauss > filters.threshold_otsu(img_gauss)
        img_close = morphology.binary_closing(img_binary, morphology.disk(closing_disk_radius))
        
        #background
        background = ~(img>0)
        cleaned_background = morphology.remove_small_objects(background, min_size=100)
        
        #tissue mask
        mask_temp = cleaned_background + img_close
        
        mask_temp = morphology.remove_small_objects((1-mask_temp).astype(bool), min_size=500)
        mask_temp = morphology.remove_small_holes(mask_temp, area_threshold=1000)
        mask[i] = ~mask_temp * (img>0)
    return mask


def create_shell_dataframe(shell_df, shell_mask, reverse = False):
    x_size, y_size = image_size(shell_df)
    tissue_id_list = shell_df.tissue_id.unique().tolist()
    nslice = len(tissue_id_list)
    
    slice_shell_df_list=[]
    for slice_number in tqdm(range(nslice)):
        if reverse:
            df_temp = shell_df[shell_df['tissue_id'] == tissue_id_list[nslice-slice_number-1]]
        else:
            df_temp = shell_df[shell_df['tissue_id'] == tissue_id_list[slice_number]]
        
        x_values = df_temp['x'].to_numpy()
        y_values = df_temp['y'].to_numpy()

        visited_x = np.unique(x_values)
        visited_y = np.unique(y_values)

        cnt_x = len(visited_x)
        cnt_y = len(visited_y)

        sort_x_inds = visited_x.argsort()
        sort_y_inds = visited_y.argsort()

        visited_x = visited_x[sort_x_inds]
        visited_y = visited_y[sort_y_inds]

        x_vals = np.ceil((x_size - cnt_x)/2).astype(int)
        y_vals = np.ceil((y_size - cnt_y)/2).astype(int)

        x_ind = np.nonzero(shell_mask[slice_number])[0]-x_vals
        y_ind = np.nonzero(shell_mask[slice_number])[1]-y_vals
        values = shell_mask[slice_number][np.nonzero(shell_mask[slice_number])]

        nearest_x = visited_x[x_ind]
        nearest_y = visited_y[y_ind]
    
        slice_shell_df = pd.DataFrame({'x':nearest_x,'y':nearest_y,'shell':values})
        slice_shell_df_list.append(slice_shell_df)
    
    all_shell_df = pd.concat(slice_shell_df_list,axis=0, ignore_index=True)
    new_shell_df = pd.merge(shell_df,all_shell_df,on=['x','y'],how='left')
    
    #make_directory('./shell/')
    #new_shell_df.to_csv('./shell/shell.csv')
    return new_shell_df

def image_size(data):
    x_size_list = []
    y_size_list = []
    tissue_id_list = data.tissue_id.unique().tolist()
    for i in range(len(tissue_id_list)):
        data_temp = data[data['tissue_id'] == tissue_id_list[i]]

        # loop for counting the unique
        x_values = data_temp['x'].to_numpy()
        y_values = data_temp['y'].to_numpy()

        visited_x = np.unique(x_values)
        visited_y = np.unique(y_values)

        cnt_x = len(visited_x)
        cnt_y = len(visited_y)

        x_size_temp = ((cnt_x*1.1 + 9) // 10) * 10
        y_size_temp = ((cnt_y*1.1 + 9) // 10) * 10
        
        x_size_list.append(x_size_temp)
        y_size_list.append(y_size_temp)
        
    x_size = np.ceil(max(x_size_list)).astype(int)
    y_size = np.ceil(max(y_size_list)).astype(int)
    return x_size,y_size

def remove_shell(data,shell):
    data = data.reset_index(drop=True)
    shell = shell.reset_index(drop=True)
    shell_index = shell[shell['shell']==1].index
    new_data = data.drop(shell_index)
    return new_data