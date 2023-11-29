# visualization
import pandas as pd
import numpy as np
from pylab import *
import math
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation

def mmontage(d, originSelect='lower'):

    slices, rows, cols = d.shape

    N = round(math.sqrt(slices))

    im_cols = N
    im_rows = N

    if im_rows*im_cols < slices:
        im_rows = im_rows + 1

    extra = im_cols * im_rows - slices

    ii = 0
    d2 = np.zeros((int(im_rows*rows), int(im_cols*cols)), dtype=d.dtype)

    for ri in np.arange(0, im_rows):
        for ci in np.arange(0, im_cols):
            if ii == slices:
                break
            d2[int(ri*rows):int((ri+1)*rows), int(ci*cols):int((ci+1)*cols)] = d[ii, :, :]
            ii = ii + 1

    imshow(d2, origin = originSelect)
    axis('off')

def display_montage(matrix,grayscale=True,cmap=None):
    fig, ax = plt.subplots()
    im = mmontage(matrix, 'upper')
    if grayscale:
        gray()
    else:
        set_cmap(cmap)
        cbar = fig.colorbar(im,ax=ax,ticks=[0,np.percentile(matrix[matrix != 0], 99)],shrink=0.5)
        cbar.mappable.set_clim(vmin=0,vmax=np.percentile(matrix[matrix != 0], 99))
        cbar.ax.set_yticklabels(['low', 'high'])
    axis('off')
    clim(0, np.percentile(matrix[matrix != 0], 99))

def display_animation(matrix,grayscale=False,cmap=None):
    plt.rcParams["animation.html"] = "jshtml"
    frames = matrix.shape[0]
    fig, ax = plt.subplots(figsize=(4, 4))
    vmax = np.percentile(matrix[matrix != 0], 99)
    
    def animate(i):
        im = ax.imshow(matrix[i], origin='upper',vmax=vmax)
        if grayscale:
            gray()
        else:
            set_cmap(cmap)
        ax.set_axis_off()
    
    ani = matplotlib.animation.FuncAnimation(fig, animate, frames=frames)
    plt.close(fig)
    return ani

def display_interp_montage(imgs,cmap1,cmap2,scale):
    d = imgs
    slices, rows, cols = d.shape

    N = round(math.sqrt(slices))

    im_cols = N
    im_rows = N

    if im_rows*im_cols < slices:
        im_rows = im_rows + 1

    fig, axes = plt.subplots(im_rows,im_cols,figsize=(7,4))
    
    plt.subplots_adjust(left=0.1,right=0.875,wspace=0, hspace=0)

    real_img_idx = np.arange(d.shape[0])[::(scale+1)]

    for i, img in enumerate(d):
        row_idx = i//im_cols
        col_idx = i%im_cols

        if i in real_img_idx:
            im1 = axes[row_idx,col_idx].imshow(img,cmap=cmap1,vmax=np.percentile(d[d != 0], 99))

            axes[row_idx,col_idx].axis('tight')    
            axes[row_idx,col_idx].axis('off')
        else:
            im2 = axes[row_idx,col_idx].imshow(img,cmap=cmap2,vmax=np.percentile(d[d != 0], 99))

            axes[row_idx,col_idx].axis('tight')    
            axes[row_idx,col_idx].axis('off')

    empty_image = np.zeros_like(d[0])
    for i in range(len(d), im_cols * im_rows):
        row_idx = i // im_cols
        col_idx = i % im_cols
        axes[row_idx, col_idx].imshow(empty_image, cmap=cmap1)
        axes[row_idx, col_idx].axis('tight')   
        axes[row_idx, col_idx].axis('off')
    
    cbar_ax1 = fig.add_axes([0.89, 0.25, 0.02, 0.5])
    cbar1 = fig.colorbar(im1, cax=cbar_ax1, ticks=[])
    cbar1.mappable.set_clim(vmin=0,vmax=np.percentile(d[d != 0], 99))
    
    cbar_ax2 = fig.add_axes([0.92, 0.25, 0.02, 0.5])
    cbar2 = fig.colorbar(im2, cax=cbar_ax2, ticks=[0,np.percentile(d[d != 0], 99)])
    cbar2.mappable.set_clim(vmin=0,vmax=np.percentile(d[d != 0], 99))
    cbar2.ax.set_yticklabels(['low', 'high'])

def overlap(matrix,cmap):
    imgs = matrix[[0,len(matrix)//2,-1],:]
    canvas = np.zeros_like(imgs[0], dtype='float64')
    alpha = 0.1
    for i in range(len(imgs)):
        cv2.addWeighted(imgs[i], alpha, canvas, 1 - alpha, 0, canvas)
    plt.imshow(canvas,cmap=cmap)
    axis('off')
    