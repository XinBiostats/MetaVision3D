# Evaluate
import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
import matplotlib.pyplot as plt
import cv2
from modules.MetaImpute3D import *

def norm_boxplot(matrix):
    matrix_reshape = matrix.reshape(matrix.shape[0],-1)

    non_zero_list = []
    for row in matrix_reshape:
        non_zero_row = row[np.nonzero(row)]
        non_zero_list.append(non_zero_row)

    fig, ax = plt.subplots(figsize=(6,15))
    ax.boxplot(non_zero_list,vert=False,showfliers=False)
    ax.invert_yaxis()
    ax.set_xlabel('Intensity',fontweight='bold',fontsize=15)
    ax.set_ylabel('Slice',fontweight='bold',fontsize=15)
    ax.tick_params(axis='both', which='both', labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    labels = [label.set_fontweight('bold') for label in labels]
    plt.show()

def align_ECC(matrix):
    ecc_list = []
    for i in range(matrix.shape[0]-1):
        ecc = cv2.computeECC(matrix[i],matrix[i+1])
        ecc_list.append(ecc)
    return ecc_list

def align_SSIM(matrix):
    ssim_list = []
    for i in range(matrix.shape[0]-1):
        img1 = minmax_scaler(matrix[i])
        img2 = minmax_scaler(matrix[i+1])
        ssim_val = ssim(img1,img2,data_range=255)
        ssim_list.append(ssim_val)
    return ssim_list

def minmax_scaler(img):
    min_value = np.min(img)
    max_value = np.max(img)
    img_scaled = ((img - min_value) / (max_value - min_value) * 255).astype(np.uint8)
    return img_scaled

def align_MSE(matrix):
    mse_list = []
    for i in range(matrix.shape[0]-1):
        mse_val = mse(matrix[i],matrix[i+1])
        mse_list.append(mse_val)
    return mse_list

def impute_ECC(matrix1,matrix2):
    ecc_list = []
    for i in range(matrix1.shape[0]):
        ecc = cv2.computeECC(matrix1[i],matrix2[i])
        ecc_list.append(ecc)
    return ecc_list

def impute_SSIM(matrix1,matrix2):
    ssim_list = []
    for i in range(matrix1.shape[0]):
        img1 = minmax_scaler(matrix1[i])
        img2 = minmax_scaler(matrix2[i])
        ssim_val = ssim(img1,img2,data_range=255)
        ssim_list.append(ssim_val)
    return ssim_list

def impute_MSE(matrix1,matrix2):
    mse_list = []
    for i in range(matrix1.shape[0]):
        mse_val = mse(matrix1[i],matrix2[i])
        mse_list.append(mse_val)
    return mse_list

def calculate_metric(data, operation, metric,data2=None):
    if operation == 'alignment':
        if metric == 'ECC':
            result = align_ECC(data)
        elif metric == 'SSIM':
            result = align_SSIM(data)
        elif metric == 'MSE':
            result = align_MSE(data)
        else:
            raise ValueError("Invalid metric name, please use 'ECC', 'SSIM' or 'MSE'")      
        
    elif operation=='imputation':
        if data2 is None:
            raise ValueError("Please provide two input datasets: the original one and the imputed one")      
        if metric == 'ECC':
            result = impute_ECC(data,data2)
        elif metric == 'SSIM':
            result = impute_SSIM(data,data2)
        elif metric == 'MSE':
            result = impute_MSE(data,data2)
        else:
            raise ValueError("Invalid metric name, please use 'ECC', 'SSIM' or 'MSE'")      

    else:
        raise ValueError("Invalid operation name, please use 'alignment' or 'imputation'")
    return result
        

        