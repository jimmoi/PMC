import cv2
import numpy as np

class PerspectiveTransform2D:
  ''''
  Transform position in 3D perspective to 2D perspective 
  '''
  def __init__(self ,input_points=None ,output_points=None):
    '''
    Parameters
        ----------
        input_points : np.float32
            4 referent point counter clockwise in 3D perspective
        output_points : np.float32
            4 referent point in 2D perspective that same position input_points
    '''
    if input_points != None:
      self.fit(input_points ,output_points)

  def fit(self, input_points , output_points):
    '''
    Parameters
        ----------
        input_points : np.float32
            4 referent point counter clockwise in 3D perspective
        output_points : np.float32
            4 referent point in 2D perspective that same position input_points
    '''
    if len(input_points) != 4:
        raise Exception("PerspectiveTransform2D.fit input_points size wrong")
    if len(output_points) != 4:
        raise Exception("PerspectiveTransform2D.fit output_points size wrong")
    if np.any(input_points < 0):
        raise Exception("PerspectiveTransform2D.fit input_points x,y cant be negative value")
    if np.any(output_points < 0):
        raise Exception("PerspectiveTransform2D.fit output_points x,y cant be negative value")

    self.transform_matrix=cv2.getPerspectiveTransform(input_points ,output_points)

  def transform(self ,point):
    '''
    Parameters
        ----------
        point : list
           [x,y] in old perspective that want to convert to 2D perspective
    '''
    if any(unit<0 for unit in point):
        raise Exception("PerspectiveTransform2D.transform point x,y cant be negative value")
    
    bypass = 1
    x_relative_size,y_relative_size,size_scale=np.dot(self.transform_matrix ,point+[bypass])
    x = x_relative_size/size_scale
    y = y_relative_size/size_scale
    newpoint=(int(x) ,int(y))
    return newpoint

if __name__ == "__main__":
    input_pts = np.float32([[80,1286],[3890,1253],[3890,122],[450,115]]) # ตำแหน่งบนกล้อง
    output_pts = np.float32([[100,100],[100,3900],[2200,3900],[2200,100]]) # ตำแหน่งบนแผนผังอาคาร
    mapping=PerspectiveTransform2D()
    mapping.fit(input_pts,output_pts)
    old_point=[500,1000]
    x,y=mapping.transform(old_point)
    print(x,y)