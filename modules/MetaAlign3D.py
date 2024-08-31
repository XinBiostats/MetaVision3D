# MetaAlign3D module
import numpy as np
import pandas as pd
import cv2
import os
from tqdm import tqdm
from .utils import get_ref_compound,make_directory

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
    
    
def create_slice(df_all,slice_number, compound, reverse = False):
    tissue_id_list = df_all.tissue_id.unique().tolist()
    nslice = len(tissue_id_list)
    if reverse:
        df_temp = df_all[df_all['tissue_id'] == tissue_id_list[nslice-slice_number-1]]
    else:
        df_temp = df_all[df_all['tissue_id'] == tissue_id_list[slice_number]]


    # loop for counting the unique
    # x_values = np.around(df_temp['x'].to_numpy(), 0)
    # y_values = np.around(df_temp['y'].to_numpy(), 0)
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

    reshaped_matrix = np.zeros((cnt_x, cnt_y))
    for ii, vi in enumerate(getattr(df_temp,compound)):
        if not np.isnan(vi):
            x_ind = find_nearest(visited_x, x_values[ii])
            y_ind = find_nearest(visited_y, y_values[ii])
            reshaped_matrix[x_ind, y_ind] = vi
            
        else:
            continue
    
    return reshaped_matrix

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def create_compound_matrix(data,compound,reverse=False):
    x_size, y_size = image_size(data)
    nslice = len(data.tissue_id.unique())
    matrix = np.zeros((nslice, x_size, y_size))

    for ii in tqdm(range(matrix.shape[0])):
        data_temp = create_slice(data, ii,compound=compound, reverse=reverse)
        x_vals = np.ceil((x_size - data_temp.shape[0])/2).astype(int) 
        y_vals = np.ceil((y_size - data_temp.shape[1])/2).astype(int) #find the (x,y) of the start vertex, '/2' means put the slice in the center
        matrix[ii, x_vals:x_vals+data_temp.shape[0], y_vals:y_vals+data_temp.shape[1]] = data_temp
    return matrix



def motionCorr_apply_maldi(ref_image, moving_image):
    cv_img_1 = cv2.convertScaleAbs(ref_image, alpha=255/ref_image.max())
    cv_img_2 = cv2.convertScaleAbs(moving_image, alpha=255/moving_image.max())
    # Find size of image1
    sz = cv_img_2.shape

    # Define the motion model
    warp_mode = cv2.MOTION_EUCLIDEAN
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    
    # Specify the number of iterations.
    number_of_iterations = 5000;
    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-10;
    
    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)

    # Run the ECC algorithm. The results are stored in warp_matrix.
    try:
        (cc, warp_matrix) = cv2.findTransformECC (cv_img_1,cv_img_2,warp_matrix, warp_mode, criteria)
    except cv2.error:
        return cv_img_2,warp_matrix

    # Use warpAffine for Translation, Euclidean and Affine
    im2_aligned = cv2.warpAffine(moving_image, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
    return im2_aligned,warp_matrix

def alignment_warp_matrix(moving_image, warp_matrix):
    cv_img_2 = cv2.convertScaleAbs(moving_image, alpha=255/moving_image.max())
    sz = cv_img_2.shape
    im_aligned = cv2.warpAffine(moving_image, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    
    return im_aligned

def calculate_warp_matrix(ref_matrix):
    matrix_corrected = np.zeros((ref_matrix.shape))
    matrix_corrected[0] = ref_matrix[0]
    warp_matrix_all = np.zeros((matrix_corrected.shape[0] - 1, 2, 3))
    for ii in tqdm(range(matrix_corrected.shape[0] - 1)):
        if np.all(ref_matrix[ii + 1] == 0):
            next_nonzero_index = ii + 2
            while next_nonzero_index < ref_matrix.shape[0] and np.all(ref_matrix[next_nonzero_index] == 0):
                next_nonzero_index += 1
            if next_nonzero_index < ref_matrix.shape[0]:
                matrix_corrected[ii + 1], warp_matrix_all[ii] = motionCorr_apply_maldi(
                    matrix_corrected[ii], ref_matrix[next_nonzero_index])
            else:
                matrix_corrected[ii + 1] = matrix_corrected[ii]
                warp_matrix_all[ii] = np.eye(2, 3)
        else:
            matrix_corrected[ii + 1], warp_matrix_all[ii] = motionCorr_apply_maldi(
                matrix_corrected[ii], ref_matrix[ii + 1])
            
    return warp_matrix_all
        

def seq_align(matrix, warp_matrix_all):
    matrix_corrected = np.zeros((matrix.shape))
    matrix_corrected[0] = matrix[0]
    for ii in tqdm(range(matrix_corrected.shape[0]-1)):
        if np.all(matrix[ii + 1] == 0):
            matrix_corrected[ii+1] = matrix[ii+1]
        else:
            matrix_corrected[ii+1] = alignment_warp_matrix(matrix[ii+1],warp_matrix_all[ii]) 
    return matrix_corrected


class MetaAlign3D:
    def __init__(self, group, data, compound, first_feature='Pyruvate', reverse=False):
        self.group = group
        self.data = data
        self.compound = compound
        self.first_feature = first_feature
        self.reverse = reverse
        self.matrix=None
        self.corrected_matrix=None
        self.warp_matrix_all=None
        
        if os.path.exists(f'./warpmatrix/warp_matrix_{self.group}.npy'):
            print('Warp matrix exists. Using existing warp matrix to do alignment.')
            self.warp_matrix_all = np.load(f'./warpmatrix/warp_matrix_{self.group}.npy')
            
        else:
            print('Warp matrix does not exist. Using the most prevalent compound to calculate warp matrix.')
            # find most prevalent compound as reference compound
            ref_compound = get_ref_compound(self.data,first_feature=self.first_feature)
            # calculate warp matrix
            ref_compound_matrix = create_compound_matrix(self.data, ref_compound, reverse=self.reverse)
            self.warp_matrix_all = calculate_warp_matrix(ref_compound_matrix)
            make_directory('./warpmatrix/')
            np.save(f'./warpmatrix/warp_matrix_{self.group}', self.warp_matrix_all)
            print(f'Warp matrix is created based on {ref_compound}.')
            
    def create_compound_matrix(self):
        x_size, y_size = image_size(self.data)
        nslice = len(self.data.tissue_id.unique())
        self.matrix = np.zeros((nslice, x_size, y_size))
        for ii in tqdm(range(self.matrix.shape[0])):
            data_temp = create_slice(self.data, ii, compound=self.compound, reverse=self.reverse)
            x_vals = int((x_size - data_temp.shape[0])/2) 
            y_vals = int((y_size - data_temp.shape[1])/2) #find the (x,y) of the start vertex, '/2' means put the slice in the center
            self.matrix[ii, x_vals:x_vals+data_temp.shape[0], y_vals:y_vals+data_temp.shape[1]] = data_temp
        return self.matrix
    
    def seq_align(self):
        self.matrix_corrected = np.zeros((self.matrix.shape))
        self.matrix_corrected[0] = self.matrix[0]
        for ii in tqdm(range(self.matrix_corrected.shape[0]-1)):
            if np.all(self.matrix[ii + 1] == 0):
                self.matrix_corrected[ii+1] = self.matrix[ii+1]
            else:
                self.matrix_corrected[ii+1] = alignment_warp_matrix(self.matrix[ii+1],self.warp_matrix_all[ii]) 
        return self.matrix_corrected
    
    

    
            
        
                    



