import cv2
import numpy as np
def show_img(name,img):
	cv2.namedWindow(name)#cv2.WINDOW_NORMAL可以手动改变大小
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
img = cv2.imread('C:/Users/Administrator/Desktop/test.jpg')  
rows, cols, ch = img.shape  
print(rows,cols)
pts1 = np.float32([[0, 0], [cols - 1, 0], [0, rows-1]])  
pts2 = np.float32([[0,rows*0.1], [cols-1+50,rows*0.1], [0, rows*0.9]])  
  
M = cv2.getAffineTransform(pts1, pts2)  
dst = cv2.warpAffine(img, M, (cols+50, rows))  
#cv2.imwrite('test_new.jpg',dst)
show_img('test',dst)