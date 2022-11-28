#!/usr/bin/env python
# coding: utf-8

# ### Intersection over Union (IoU)
# This script will calculate the Intersection over Union (IoU) for two bounding boxes. The IoU is a measure of how much overlap there is between two bounding boxes on a single image. The IoU is calculated as the area of overlap divided by the area of union between two bounding boxes. The value of the IoU is a number between 0 and 1, with 1 representing perfect overlap and 0 representing no overlap. The IoU is used to determine if a proposed bounding box accurately describes an object in an image. The IoU is also used to determine if proposed bounding boxes accurately describe the same object in different images. The IoU is calculated as follows:
# $$
# IoU = \frac{Area\ of\ Overlap}{Area\ of\ Union}
# $$

# In[1]:


def compute_iou(boxA, boxB):
    """
    Compute the Intersection over Union (IoU) of two bounding boxes.
    Parameters:
        boxA (list): The first bounding box. The box is specified in the format
            [x, y, width, height].
        boxB (list): The second bounding box. The box is specified in the format
            [x, y, width, height].
    Returns:
        iou (float): The Intersection over Union (IoU) of the two bounding boxes.
    """
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou
