import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scipy import ndimage
import numpy as np

import cv2
import matplotlib.pyplot as plt


def im_kde(coords,width=1280, height=720,sigma=25):
    x = np.zeros((height,width))
    for i,j in coords:
        x[j,i]=255
    heat_map = ndimage.gaussian_filter(x, sigma=sigma)*4
    heat_map[heat_map>1]=1
    return heat_map

def overay_heatmap(im, heatmap):
    heatmap=cv2.applyColorMap(np.uint8(heatmap*255), cv2.COLORMAP_PARULA)
    heat_map=cv2.addWeighted(im, 0.6, heatmap, 0.4, 0)
    return heat_map

class HeatMap:
    def get_xy_all_detections(self, detections):
        detections = np.array(detections)
        coords = pd.DataFrame({
            "x_coords": detections[:, 0],
            "y_coords": detections[:, 1]
        })
        


if __name__ == '__main__':
    detections = np.array([
        [785, 556], [75, 560], [285, 586], [286, 586], [285, 587], [230, 586], [310, 586], [295, 586]
    ])
    
    im=cv2.imread('../floor1_plan_new.png')
    heatmap=im_kde(detections)
    heatmap=cv2.applyColorMap(np.uint8(heatmap*255), cv2.COLORMAP_PARULA)
    heat_map=cv2.addWeighted(im, 0.6, heatmap, 0.4,0)
    plt.imshow(heat_map[:,:,[2,1,0]])
    plt.show()
    

    