""" Descriptions for Person_Dectection.py
Module นี้ทำหน้าที่เกี่ยวกับการตรวจจับคนในภาพเพื่อทำการกำหนดจุด Coordinate สำหรับการ Mapping เข้าแผนที่
Example:
    ในการเรียกใช้ไฟล์นี้
        $python Person_Dectection.py

"""

import cv2
import torch

import numpy as np
import pandas as pd


class PersonDectecter:
    ''''
    Dectect person object in single image
    '''

    def __init__(self, confidence_theshold=0.5):
        """
        Parameters
            ----------
            confidence_theshold : >= 0 and <= 1
        """

        if not(0 <= confidence_theshold <= 1):
            raise Exception(
                "Person_Dectection.__init__ confidence_theshold not in range")

        self.confidence_theshold = confidence_theshold
        self.model = torch.hub.load("ultralytics/yolov5"
                                    ,'yolov5n'
                                    ,force_reload=False)

    def dectect(self, image: np.array) -> pd.DataFrame:
        '''
        Parameters
            ----------
            image : cv2 image color need to convert to RGB
                image that want to dectect person

        Return:
            data_frame colum is (xcenter,ycenter,width,height) foreach person
        '''

        results = self.model(image)
        real_results = self._filter_person(results)
        return real_results

    def _filter_person(self, results):
        """
        Parameters
            ----------
            results: result from prediction
        Return:
            data_frame that have only person and colum is (xcenter,ycenter,width,height)
        """

        df = results.pandas().xywh[0]
        df_only_person = df[df.name.isin(["person"])]
        df_only_person_confienced = df_only_person[df_only_person.confidence >=
                                                   self.confidence_theshold]
        return df_only_person_confienced.drop(columns=["name", "class", "confidence"])


if __name__ == "__main__":
    img = cv2.imread("Dataset/floor1.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    model = PersonDectecter()
    res = model.dectect(img)
    print(res)
