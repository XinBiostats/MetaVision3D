# MetaAtlas3D module
import nibabel as nib
import numpy as np

def create_nii(matrix,resolution,thickness,gap,insert=0):
    # resolution: MALDI resolution (x-y axis); section thickness; gap between adjacent sections; number of inserted sections
    # reshape matrix from (z,y,x) to (x,y,z)
    output_matrix = transpose(matrix,(2,1,0))
    Ir = squeeze(output_matrix)
    img = nib.Nifti1Image(Ir, affine=np.eye(4))
    # adjust thickness
    header = img.header.copy()
    header['pixdim'][3] = (thickness+gap)/((1+insert)*resolution)

    nii_img = nib.Nifti1Image(Ir, affine=np.eye(4), header=header)
    return nii_img

class MetaAtlas3D:
    def __init__(self,matrix,resolution,thickness,gap,insert=0):
        self.matrix=matrix
        self.resolution=resolution
        self.thickness=thickness
        self.gap=gap
        self.insert = insert
        
    def create_nii(self):
        # reshape matrix from (z,y,x) to (x,y,z)
        output_matrix = np.transpose(self.matrix,(2,1,0))
        Ir = np.squeeze(output_matrix)
        img = nib.Nifti1Image(Ir, affine=np.eye(4))
        # adjust thickness
        header = img.header.copy()
        header['pixdim'][3] = (self.thickness+self.gap)/((1+self.insert)*self.resolution)
    
        nii_img = nib.Nifti1Image(Ir, affine=np.eye(4), header=header)
        return nii_img

