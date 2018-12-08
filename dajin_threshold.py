import numpy as np
import cv2

def show_img(name,img):
	cv2.namedWindow(name)#cv2.WINDOW_NORMAL可以手动改变大小
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

class dajin_threshold(object):
	def read(self,input):#读入要处理的图片
		if type(input)==str:
			self.original_img=cv2.imread(input)
			self.gray_img=cv2.cvtColor(self.original_img,cv2.COLOR_BGR2GRAY)
			#self.gray_img=self.original_img
			show_img('The original image',self.gray_img)
		else:
			self.gray_img=input
			show_img('The original image',self.gray_img)
	
	def otsu(self):
		gray_statistics={}#像素的灰度值统计
		for i in range(256):
			gray_statistics[i]=0
		s=self.gray_img.shape
		for i in range(s[0]):
			for j in range(s[1]):
				gray_statistics[self.gray_img[i][j]]+=1
		t_old=128
		while True:
			left_value=0;right_value=0;left_num=0;right_num=0
			for i in range(0,t_old+1):
				left_value+=i*gray_statistics[i]
				left_num+=gray_statistics[i]
			for j in range(t_old+1,255):
				right_value+=j*gray_statistics[j]
				right_num+=gray_statistics[j]
			t_new=int((left_value/left_num+right_value/right_num)/2)
			#print(t_new)
			if t_new==t_old:
				break
			else:
				t_old=t_new
		threshold_img=np.zeros((s[0],s[1]))
		for i in range(s[0]):
			for j in range(s[1]):
				if self.gray_img[i][j]>t_new:
					threshold_img[i][j]=255
				else:
					threshold_img[i][j]=0
		threshold_img=np.uint8(threshold_img)
		cv2.imwrite('C:/Users/Administrator/Desktop/open_dajin.bmp',threshold_img)
		show_img('open_dajin',threshold_img)
	
	def main(self):
		self.otsu()
example=dajin_threshold()
example.read('C:/Users/Administrator/Desktop/open.bmp')
example.main()




