import nibabel as nib

from skimage import exposure
from skimage.transform import resize
import numpy as np
import cv2 as cv

DRAWING = False
IX, IY = -1, -1
PICT = None

def draw(event, x, y, flags, param):
    global IX, IY, DRAWING, PICT
    if event == cv.EVENT_LBUTTONDOWN:
        DRAWING = True
        IX, IY = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if DRAWING:
            cv.line(PICT, (IX, IY), (x, y), (255, 0, 0), 3)
            IX, IY = x, y

    elif event == cv.EVENT_LBUTTONUP:
        DRAWING = False
        cv.line(PICT, (IX, IY), (x, y), (255, 0, 0), 3)


def new_frame(x):
    pict = data[:, :, x].T
    norm = (pict - np.min(pict) / np.max(pict) - np.min(pict))
    ecv = exposure.equalize_hist(norm)
    ecv = resize(ecv, (1000, 1000), anti_aliasing = 1)
    global PICT
    PICT = cv.merge([ecv, ecv, ecv])



img3D = nib.load('IXI020-Guys-0700-T1.nii.gz')
data = img3D.get_fdata()
shapka = data.shape[2]
cv.namedWindow('image_MRT')
cv.createTrackbar('Slice_MRT', 'image_MRT', 0, shapka-1, new_frame)
cv.setMouseCallback("image_MRT", draw)


while 1:
    if PICT is None:
        new_frame(0)
    cv.imshow('image_MRT', PICT)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    if k == ord('s'):
        cv.imwrite('C:\screen.png', PICT)

