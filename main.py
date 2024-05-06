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
####### load raw dataset ########
#################################
data_path = './data/3d_lipid.csv'
df_raw = pd.read_csv(data_path,index_col=False)
df, deleted_compound = delete_low_prevalence_compound(df_raw, 0.1, first_feature='LPA_16_0_')

compounds = df.columns.tolist()[5:]
ref_compound = get_ref_compound(df,first_feature='LPA_16_0_')

####################################################
####### run ref_compound to get warpmatrix #########
####################################################
get_warp_matrix(df,ref_compound,first_feature='LPA_16_0_',reverse=True)

##########################################
###### run all compounds #################
##########################################
for compound in compounds:
    # MetaNorm3D
    ## normalization
    meta_norm = MetaNorm3D(df, compound, first_feature='LPA_16_0_')
    
    ## totalsum normalization
    norm_df = meta_norm.totalsum_norm()
    
    ## section normalization
    data = meta_norm.section_norm()
    
    # MetaAlign3D
    meta_align = MetaAlign3D(data)
    
    ## manual slices fitting and create compound matrix
    compound_matrix = meta_align.create_compound_matrix(reverse=False)
    
    aligned_matrix = meta_align.seq_align()
    
    display_montage(aligned_matrix,grayscale=False,cmap=new_cmap1)
    
    if not os.path.exists('./output/align/'):
        os.makedirs('./output/align/')
    plt.savefig(f'./output/align/{compound}.png',dpi=2000)
    plt.close('all')
    
    # MetaImpute3D
    meta_impute = MetaImpute3D(aligned_matrix)
    
    imputed_matrix = meta_impute.seq_impute()
    
    display_montage(imputed_matrix,grayscale=False,cmap=new_cmap1)
    
    if not os.path.exists('./output/impute/'):
        os.makedirs('./output/impute/')
    plt.savefig(f'./output/impute/{compound}.png',dpi=2000)
    plt.close('all')
    
    # MetaInterp3D
    meta_interp = MetaInterp3D(imputed_matrix,2)
    
    interpolated_matrix = meta_interp.interp()
    
    display_interp_montage(interpolated_matrix,new_cmap1,new_cmap2,scale=2)
    
    if not os.path.exists('./output/interp/'):
        os.makedirs('./output/interp/')
    plt.savefig(f'./output/interp/{compound}.png',dpi=2000)
    plt.close('all')
    
    # MetaAtlas3D
    meta_atlas = MetaAtlas3D(interpolated_matrix)
    
    nii_img = meta_atlas.create_nii()
    
    if not os.path.exists('./output/3D/'):
        os.makedirs('./output/3D/')
    nib.save(nii_img,f'./output/3D/{compound}.nii.gz')