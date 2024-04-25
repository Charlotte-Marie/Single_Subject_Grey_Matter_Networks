# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:37:00 2024

@author: meinkcha
"""

# %% Add path
import os 
import sys 
import nibabel as nib
import numpy as np
#sys.path.append("C:\\Users\\meinkcha.PSYCHOLOGIE\\Documents\\GitHub\\Functional-similarity-gradient\\1_Create_gradient")

# %% Import other packages

#from conmap_CM_create_brain_mask_2 import  create_gm_mask_from_dseg

def create_gm_mask_from_dseg(gm_path, individual_masks_path):
    """ This function creates an individual grey matter mask based on the freesurfer output
    "dseg" in Halfpipe, that has been resampled on the space of the bold image:
    "_space-MNI152NLin2009cAsym_res-2_dseg.nii.gz"
    https://fmriprep.org/en/1.3.0/outputs.html
    In dseg, white matter, grey matter, and CSF are seperated from each other
    """
    gm_img = nib.load(gm_path)  # Load image
    gm_np = gm_img.get_fdata() # Turn image to np-array

    np.place(gm_np, gm_np == 1,1) # Grey matter = 1 in segmentation image
    np.place(gm_np, gm_np != 1, 0)
    
    gm_bin_img = nib.Nifti1Image(gm_np,gm_img.affine)
        
    # Save grey matter mask
    # Generate gm_mask_name by replacing "dseg" with "gm"
    gm_mask_name = os.path.basename(gm_path).replace("dseg", "gm")
    nib.save(gm_bin_img,os.path.join(individual_masks_path,gm_mask_name))
    
    return gm_bin_img 

# %% Define functions

gm_path = "Y:\\PsyThera\\Projekte_Meinke\\Structural_covariance\\test_script\\input_data\\sub-3C09WU001A_space-MNI152NLin2009cAsym_res-2_dseg.nii.gz"
create_gm_mask_from_dseg(gm_path, individual_masks_path = "Y:\\PsyThera\\Projekte_Meinke\\Structural_covariance\\test_script\\input_data\\grey_matter_masks")