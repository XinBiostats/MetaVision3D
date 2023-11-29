# MetaAtlas3D module
import nibabel as nib
import numpy as np

def create_nii(matrix,path,scale=0):
    # reshape matrix from (z,y,x) to (x,y,z)
    output_matrix = transpose(matrix,(2,1,0))
    Ir = squeeze(output_matrix)
    img = nib.Nifti1Image(Ir, affine=np.eye(4))
    # adjust thickness
    header = img.header.copy()
    header['pixdim'][3] = 1/(scale+1)

    ni_img = nib.Nifti1Image(Ir, affine=np.eye(4), header=header)
    return ni_img

class MetaAtlas3D:
    def __init__(self,matrix,scale=0):
        self.matrix=matrix
        self.scale = scale
        
    def create_nii(self):
        # reshape matrix from (z,y,x) to (x,y,z)
        output_matrix = np.transpose(self.matrix,(2,1,0))
        Ir = np.squeeze(output_matrix)
        img = nib.Nifti1Image(Ir, affine=np.eye(4))
        # adjust thickness
        header = img.header.copy()
        header['pixdim'][3] = 1/(self.scale+1)
    
        ni_img = nib.Nifti1Image(Ir, affine=np.eye(4), header=header)
        return ni_img

