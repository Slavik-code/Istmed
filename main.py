import nibabel as nib

from skimage import exposure
from skimage.transform import resize
import numpy as np
import cv2 as cv

PICT = None

def new_frame(x):
    pict = data[:, :, x].T
    norm = (pict - np.min(pict) / np.max(pict) - np.min(pict))
    ecv = exposure.equalize_hist(norm)
    ecv = resize(ecv, (1000, 1000), anti_aliasing = 1)
    global PICT
    PICT = ecv

img3D = nib.load('IXI020-Guys-0700-T1.nii.gz')
data = img3D.get_fdata()
shapka = data.shape[2]
cv.namedWindow('image_MRT')
cv.createTrackbar('Slice_MRT', 'image_MRT', 0, shapka-1, new_frame)

while 1:
    if PICT is None:
        new_frame(0)
    cv.imshow('image_MRT', PICT)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

