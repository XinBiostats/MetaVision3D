from tqdm import tqdm
from modules.setup import *
from modules.utils import *
from modules.MetaNorm3D import *
from modules.MetaAlign3D import *
from modules.MetaImpute3D import *
from modules.MetaInterp3D import *
from modules.MetaAtlas3D import *
from modules.visualize import *
from modules.evaluate import *

#################################
####### setup #########
group = 'wt'
omic = 'lipid'

data_file_path = f'./data/{group}/3d_brain_{group}_pbp_{omic}_preprocessed.csv'
shell_file_path = f'./data/{group}/shell.csv'

#output path
raw_path = f'./output/{group}/{omic}/raw'
norm_path = f'./output/{group}/{omic}/norm'
align_path = f'./output/{group}/{omic}/align'
impute_path = f'./output/{group}/{omic}/impute'
interpolate_path = f'./output/{group}/{omic}/interpolate'
nii_path = f'./output/{group}/{omic}/3D'

inferior_tissues_id = [62,67,116]
first_feature = 'LPA.18.1.'

#################################
####### load raw dataset ########
#################################
shell = pd.read_csv(shell_file_path,index_col=0)
df = pd.read_csv(data_file_path,index_col=0)
df = remove_shell(df,shell)
df, deleted_compound = delete_low_prevalence_compound(df, 0.1, first_feature=first_feature)

compounds = df.columns.tolist()[np.where(df.columns==first_feature)[0][0]:]

#################################
####### preprocessing ###########
#################################
# flip in the left/right direction
df = flip_axis(df,flipud=True)

df = delete_inferior_tissues(df,inferior_tissues_id,first_feature=first_feature,reverse=True)

# for compound in tqdm(compounds):
#     raw_matrix = create_compound_matrix(df, compound=compound,reverse=True)
    
#     display_montage(raw_matrix,grayscale=False,cmap=new_cmap1)
#     make_directory(f'{raw_path}/montage')
#     plt.savefig(f'{raw_path}/montage/{compound}.png',dpi=2000)
#     plt.close('all')

###################################
###### MetaNorm3D #################
###################################
# normalization
meta_norm = MetaNorm3D(df, first_feature=first_feature)
# totalsum normalization
data = meta_norm.totalsum_norm()
# section normalization
# data = meta_norm.section_norm()

# for compound in tqdm(compounds):
#     norm_matrix = create_compound_matrix(data, compound=compound,reverse=True)
    
#     display_montage(norm_matrix,grayscale=False,cmap=new_cmap1)
#     make_directory(f'{norm_path}/montage')
#     plt.savefig(f'{norm_path}/montage/{compound}.png',dpi=2000)
#     plt.close('all')

###################################
###### MetaAlign3D+MetaImpute3D ###
###### MetaInterp3D+MetaAtlas3D ###
###################################
for compound in tqdm(compounds):
    # MetaAlign3D
    meta_align = MetaAlign3D(group,data,compound,first_feature=first_feature, reverse=True)
    compound_matrix = meta_align.create_compound_matrix()
    aligned_matrix = meta_align.seq_align()
    
    display_montage(aligned_matrix,grayscale=False,cmap=new_cmap1)
    make_directory(f'{align_path}/montage')
    plt.savefig(f'{align_path}/montage/{compound}.png',dpi=2000)
    plt.close('all')
    
    make_directory(f'{align_path}/animation')
    animation = display_animation(aligned_matrix,grayscale=False,cmap=cmap1)
    animation.save(f'{align_path}/animation/{compound}.gif', writer='pillow')

    # MetaImpute3D
    meta_impute = MetaImpute3D(aligned_matrix,radius=1)
    imputed_matrix = meta_impute.seq_impute()
    
    display_montage(imputed_matrix,grayscale=False,cmap=new_cmap1)
    make_directory(f'{impute_path}/montage')
    plt.savefig(f'{impute_path}/montage/{compound}.png',dpi=2000)
    plt.close('all')
    
    make_directory(f'{impute_path}/animation')
    animation = display_animation(imputed_matrix,grayscale=False,cmap=cmap1)
    animation.save(f'{impute_path}/animation/{compound}.gif', writer='pillow')
    
    # MetaInterp3D
    meta_interp = MetaInterp3D(imputed_matrixs,2)
    interpolated_matrix = meta_interp.interp()
    
    display_interp_montage(interpolated_matrix,new_cmap1,new_cmap2,insert=2)
    make_directory(f'{interpolate_path}/montage')
    plt.savefig(f'{interpolate_path}/montage/{compound}.png',dpi=2000)
    plt.close('all')

    # MetaAtlas3D
    meta_atlas = MetaAtlas3D(interpolated_matrix,resolution=50,thickness=10,gap=50,insert=2)
    nii_img = meta_atlas.create_nii()
    
    make_directory(nii_path)
    nib.save(nii_img,f'{nii_path}/{compound}.nii.gz')
    
    