import numpy as np
import cv2
import copy
import Noise_and_filter as filter

def show_img(name,img):
	cv2.namedWindow(name)#cv2.WINDOW_NORMAL可以手动改变大小
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
class expand_erode(object):
	def __init__(self,input):
		if type(input)==str:
			self.gray_img=cv2.imread(input,0)
			self.s=self.gray_img.shape
		else:
			self.gray_img=input
			self.s=self.gray_img.shape
	
	def erode(self,gray_img,size):
		img=self.add_row_and_column(gray_img,size,'erode')
		r=int((size[0]-1)/2)
		c=int((size[1]-1)/2)
		new_img=copy.copy(gray_img)
		for i in range(r,self.s[0]+r):
			for j in range(c,self.s[1]+c):
				temp=img[i-r:i+r+1,j-c:j+c+1]
				new_img[i-r][j-c]=np.max(temp)
		#show_img('new_img',new_img)
		return(new_img)
	
	def expand(self,gray_img,size):
		img=self.add_row_and_column(gray_img,size,'expand')
		r=int((size[0]-1)/2)
		c=int((size[1]-1)/2)
		new_img=copy.copy(gray_img)
		for i in range(r,self.s[0]+r):
			for j in range(c,self.s[1]+c):
				temp=img[i-r:i+r+1,j-c:j+c+1]
				new_img[i-r][j-c]=np.min(temp)
		#show_img('new_img',new_img)
		return(new_img)
		
	def add_row_and_column(self,img,size,type):
		add_r_side=int((size[0]-1)/2)
		add_c_side=int((size[1]-1)/2)
		if type == 'erode':
			add_r_0=np.zeros(self.s[1])
			add_c_0=np.zeros(self.s[0]+add_r_side*2)
			for i in range(add_r_side):
				img=np.insert(img,0,values=add_r_0,axis=0)
				img=np.insert(img,img.shape[0],values=add_r_0,axis=0)
			for i in range(add_c_side):
				img=np.insert(img,0,values=add_c_0,axis=1)
				img=np.insert(img,img.shape[1],values=add_c_0,axis=1)
		elif type == 'expand':
			add_r_0=np.ones(self.s[1])*255
			add_c_0=np.ones(self.s[0]+add_r_side*2)*255
			for i in range(add_r_side):
				img=np.insert(img,0,values=add_r_0,axis=0)
				img=np.insert(img,img.shape[0],values=add_r_0,axis=0)
			for i in range(add_c_side):
				img=np.insert(img,0,values=add_c_0,axis=1)
				img=np.insert(img,img.shape[1],values=add_c_0,axis=1)
		return(img)
	
	def main(self,size):
		open=self.erode(self.gray_img,size)
		#print(open)
		open=self.expand(open,size)
		#print(open)
		#close=self.expand(self.gray_img,size)
		#print(close)
		#close=self.erode(close,size)
		#print(close)
		show_img('open',open)
		#show_img('close',close)
		cv2.imwrite('open.bmp',open)
		#cv2.imwrite('close.bmp',close)
		
		#F=filter.Filter(self.gray_img)
		#F.median_filter(5)
		#F.mean_filter(3,5)
		
		
		
		
example=expand_erode('C:/Users/Administrator/Desktop/cell.bmp')
size=[5,7]
example.main(size)
