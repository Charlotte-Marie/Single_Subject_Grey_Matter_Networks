# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:30:51 2024

@author: meinkcha
"""

# %% import 
import os 
import sys 
import nibabel as nib
import numpy as np
import nitransforms as nt
import ants

# %% 
# Load atlas_file
#glasser_atlas_path = "Y:\PsyThera\Projekte_Meinke\Gradient\Atlases\HCPex_v1.0_modified_resampled_Halfpipe_space\HCPex_2mm_modified_resampled_to_MNI152Nlin2009c.nii.gz"
glasser_atlas_path = "F:\\wd_hcp_day1\\derivatives\\fmriprep\\sub-100307\\anat\\sub-100307_space-MNI152NLin2009cAsym_res-2_desc-preproc_T1w.nii.gz"
path_transformation = "F:\\wd_hcp_day1\\derivatives\\fmriprep\\sub-100307\\anat\\sub-100307_from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5"
path_gm_mask = "F:\\wd_hcp_day1\\derivatives\\fmriprep\\sub-100307\\anat\\sub-100307_label-GM_probseg.nii.gz"
results_path = "Y:\\PsyThera\\Projekte_Meinke\\Structural_covariance\\test_individual_atlas"

atlas_nii = ants.image_read(glasser_atlas_path)
gm = ants.image_read(path_gm_mask)

# Apply transformation on atlas
xfm = nt.manip.load(path_transformation, reference = atlas_nii, fmt = "X5")
#atlas_individual = xfm.apply(atlas_nii, reference = atlas_nii)

atlas_individual = ants.apply_transforms(fixed = gm, moving = atlas_nii, transformlist = 
                                         interpolator = "lanczosWindowedSinc")

#display(atlas_individual)
nib.save(atlas_individual, os.path.join(results_path, "atlas_sub_100307.nii.gz"))
