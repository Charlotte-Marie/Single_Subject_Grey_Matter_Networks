# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:10:09 2024

@author: meinkcha
"""

import h5py
import numpy as np
import nibabel as nib
from nipype.interfaces import ants

h5_file_path = "F:\\wd_hcp_day1\\derivatives\\fmriprep\\sub-100307\\anat\\sub-100307_from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5"


ants.ApplyTransforms()

# Step 1: Load the HDF5 file
with h5py.File(h5_file_path, "r") as h5_file:
    print("Top-level keys:", list(h5_file.keys()))
    print("Top-level keys:", h5_file["TransformGroup"])
    transform_matrix = h5_file["TransformGroup"]["1"]["TransformParameters"]

# Step 2: Convert the transformation matrix to a NIfTI image or text file
# Here, we'll convert it to a NIfTI image
transform_image_data = np.eye(4)  # Identity affine matrix for transformation
transform_image_data[:3, :3] = transform_matrix.reshape((3, 3))  # Insert transform matrix
transform_image = nib.Nifti1Image(transform_image_data, np.eye(4))  # Create NIfTI image

# Save the transformation to a NIfTI file
transform_image_path = "transform.nii.gz"
nib.save(transform_image, transform_image_path)

# Step 3: Apply the transformation to your image using ANTsPy
# Load your input image
input_image_path = "your_input_image.nii.gz"
input_image = ants.image_read(input_image_path)

# Apply the transformation
output_image = ants.apply_transforms(input_image, transform_image_path)

# Save the transformed image
output_image_path = "transformed_image.nii.gz"
ants.image_write(output_image, output_image_path)