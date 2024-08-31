# MetaImputeModule
import numpy as np
import cv2

def find_neighbors(imgs,target_img,radius=2):
    
    target = imgs[target_img].copy()
    start_index = max(0, target_img-radius)
    end_index = min(len(imgs), target_img + radius +1)
    
    if start_index == 0:
        before = imgs[:target_img, :, :].copy()
        after = imgs[target_img + 1:end_index, :, :].copy()
        neighbors = np.concatenate((before, after), axis=0)
    elif end_index == len(imgs):
        before = imgs[start_index:target_img,:,:].copy()
        after = imgs[target_img+1:,:,:].copy()
        neighbors = np.concatenate((before, after), axis=0)
    else:
        before = imgs[start_index:target_img, :, :].copy()
        after = imgs[target_img + 1:end_index, :, :].copy()
        neighbors = np.concatenate((before,after), axis=0)
    return target,neighbors, before, after

def find_impute_mask(target, neighbors, before, after):
    if len(after)>0:
        mask1 = ((np.sum(after>0,axis=0) >= 1 ) & (target==0)).astype(np.uint8)
    else:
        mask1 = ((np.sum(before>0, axis=0) >= 1) & (target==0)).astype(np.uint8)

    binary_img = (target>0).astype(np.uint8)
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask2 = np.zeros_like(binary_img)
    for contour in contours:
        cv2.drawContours(mask2,[contour],-1,255,thickness=3)
    mask2 = cv2.bitwise_and(binary_img,mask2)

    impute_mask = (mask1 | mask2).astype(bool)
    return impute_mask

def impute(neighbors):
    mask = neighbors != 0
    sum_without_zeros = np.sum(neighbors * mask, axis=0)
    count_non_zeros = np.sum(mask, axis=0)
    imputation = np.zeros_like(sum_without_zeros)
    non_zero_indices = count_non_zeros != 0 
    imputation[non_zero_indices] = np.divide(sum_without_zeros[non_zero_indices], count_non_zeros[non_zero_indices])
    return imputation

def seq_impute(imgs):
    matrix_corrected_imputation = imgs.copy()
    for target_img in range(len(imgs)):
        target, neighbors, before, after = find_neighbors(matrix_corrected_imputation,target_img,radius=2)
        impute_mask = find_impute_mask(target,neighbors,before,after)
        imputation = impute(neighbors)
        matrix_corrected_imputation[target_img][impute_mask] = imputation[impute_mask]
    
    return matrix_corrected_imputation
    
def fully_impute(imgs):   
    impute_list = []
    for i in range(imgs.shape[0]):
        _,neighbors,_,_ = find_neighbors(imgs,i)
        imp_img = impute(neighbors)
        impute_list.append(imp_img)
    fully_imputed_matrix = np.array(impute_list)
    return fully_imputed_matrix

class MetaImpute3D:
    def __init__(self,matrix,radius):
        self.matrix = matrix
        self.radius = radius
        
    def seq_impute(self):
        matrix_corrected_imputation = self.matrix.copy()
        for target_img in range(len(self.matrix)):
            target, neighbors, before, after = find_neighbors(matrix_corrected_imputation,target_img,radius=self.radius)
            impute_mask = find_impute_mask(target,neighbors,before,after)
            imputation = impute(neighbors)
            matrix_corrected_imputation[target_img][impute_mask] = imputation[impute_mask]
        
        return matrix_corrected_imputation