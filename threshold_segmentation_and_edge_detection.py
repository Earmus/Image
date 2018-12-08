import numpy as np
import cv2
import math
import copy
def show_img(name,img):
	cv2.namedWindow(name)#cv2.WINDOW_NORMAL可以手动改变大小
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

class dajin_threshold(object):
	pass
class edge_detection(object):
	def __init__(self,path):
		original_img=cv2.imread(path)
		original_img=cv2.cvtColor(original_img,cv2.COLOR_BGR2GRAY)
		self.s=original_img.shape
		zero=np.zeros(self.s[0])
		self.add_0_img=np.insert(original_img,0,values=zero,axis=1)
		self.add_0_img=np.insert(self.add_0_img,self.s[1]+1,values=zero,axis=1)
		zero=np.zeros(self.s[1]+2)
		self.add_0_img=np.insert(self.add_0_img,0,values=zero,axis=0)
		self.add_0_img=np.insert(self.add_0_img,self.s[0]+1,values=zero,axis=0)

	def roberts(self):
		roberts_img=np.zeros((self.s[0],self.s[1]))
		for i in range (self.s[0]):
			for j in range (self.s[1]):
				roberts_img[i][j]=abs(int(self.add_0_img[i][j])-int(self.add_0_img[i+1][j+1]))+abs(int(self.add_0_img[i+1][j])-int(self.add_0_img[i][j+1]))
				if roberts_img[i][j]>255:
					roberts_img[i][j]=255
				elif roberts_img[i][j]<0:
					roberts_img=0
		roberts_img=np.uint8(roberts_img)
		show_img('Roberts',roberts_img)
		cv2.imwrite('C:/Users/Administrator/Desktop/lena_roberts.bmp',roberts_img)
	
	def sobel(self):
		mask1=[[-1,0,1],[-2,0,2],[-1,0,1]]
		mask2=[[1,2,1],[0,0,0],[-1,-2,-1]]
		sobel_img1=np.zeros((self.s[0],self.s[1]))
		sobel_img2=np.zeros((self.s[0],self.s[1]))
		sobel_img=np.zeros((self.s[0],self.s[1]))
		for i in range(self.s[0]):
			for j in range(self.s[1]):
				original_list=self.generate_original_list(i,j,self.add_0_img)
				sobel_img1[i][j]=abs(self.convolution_operation(original_list,mask1))
				if sobel_img1[i][j]>255:
					sobel_img1[i][j]=255
		sobel_img1=np.uint8(sobel_img1)
		#cv2.imwrite('C:/Users/Administrator/Desktop/lena_sobel1.bmp',sobel_img1)
		show_img('Sobel1',sobel_img1)
		for i in range(self.s[0]):
			for j in range(self.s[1]):
				original_list=self.generate_original_list(i,j,self.add_0_img)
				sobel_img2[i][j]=abs(self.convolution_operation(original_list,mask2))
				if sobel_img2[i][j]>255:
					sobel_img2[i][j]=255
		#cv2.imwrite('C:/Users/Administrator/Desktop/lena_sobel2.bmp',sobel_img2)
		sobel_img2=np.uint8(sobel_img2)
		show_img('Sobel2',sobel_img2)
		'''
		for i in range(self.s[0]):
			for j in range(self.s[1]):
				temp=math.sqrt((int(sobel_img1[i][j]))**2+(int(sobel_img2[i][j]))**2)
				if temp>255:
					sobel_img[i][j]=255
				else:
					sobel_img[i][j]=temp
		cv2.imwrite('C:/Users/Administrator/Desktop/lena_sobel.bmp',sobel_img)
		sobel_img=np.uint8(sobel_img)
		show_img('Sobel',sobel_img)
		'''
		for i in range(self.s[0]):
			for j in range(self.s[1]):
				temp=(int(sobel_img1[i][j])+int(sobel_img2[i][j]))/2
				if temp>255:
					sobel_img[i][j]=255
				else:
					sobel_img[i][j]=temp
		#cv2.imwrite('C:/Users/Administrator/Desktop/lena_sobel_sum.bmp',sobel_img)
		sobel_img=np.uint8(sobel_img)
		show_img('Sobel',sobel_img)
	
	
	def laplace(self):
		mask1=[[0,1,0],[1,-4,1],[0,1,0]]
		mask2=[[1,1,1],[1,-8,1],[1,1,1]]
		laplace_img1=np.zeros((self.s[0],self.s[1]))
		laplace_img2=np.zeros((self.s[0],self.s[1]))
		for i in range(self.s[0]):
			for j in range(self.s[1]):
				original_list=self.generate_original_list(i,j,self.add_0_img)
				laplace_img1[i][j]=self.convolution_operation(original_list,mask1)
				if laplace_img1[i][j]>255:
					laplace_img1[i][j]=255
				elif laplace_img1[i][j]<0:
					laplace_img1[i][j]=0
		laplace_img1=np.uint8(laplace_img1)
		cv2.imwrite('C:/Users/Administrator/Desktop/lena_laplace1.bmp',laplace_img1)
		show_img('Laplace1',laplace_img1)
		for i in range(self.s[0]):
			for j in range(self.s[1]):
				original_list=self.generate_original_list(i,j,self.add_0_img)
				laplace_img2[i][j]=self.convolution_operation(original_list,mask2)
				if laplace_img2[i][j]>255:
					laplace_img2[i][j]=255
				elif laplace_img2[i][j]<0:
					laplace_img2[i][j]=0
		laplace_img2=np.uint8(laplace_img2)
		cv2.imwrite('C:/Users/Administrator/Desktop/lena_laplace2.bmp',laplace_img2)
		show_img('Laplace2',laplace_img2)
	
	def kirsch(self):
		seq1=[(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0),(1, 0)]
		seq2=[(0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0),(0, 0)]
		seq3=[ (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0),(0, 0),(0, 1)]
		unit=np.ones((3,3))
		unit=3*unit
		mask=[]
		for i in range(8):
			temp=copy.copy(unit)
			temp[seq1[i][0]][seq1[i][1]]=-5
			mask.append(temp)
		for i in range(8):
			temp=copy.copy(mask[i])
			temp[seq2[i][0]][seq2[i][1]]=-5
			mask[i]=temp
		for i in range(8):
			temp=copy.copy(mask[i])
			temp[seq3[i][0]][seq3[i][1]]=-5
			mask[i]=temp
		for i in range(8):
			mask[i][1][1]=0
		kirsch_img=np.zeros((self.s[0],self.s[1]))
		for i in range(self.s[0]):
			for j in range(self.s[1]):
				temp_list=[]
				original_list=self.generate_original_list(i,j,self.add_0_img)
				for k in range(8):
					temp=self.convolution_operation(original_list,mask[k])
					temp_list.append(temp)
				max_num=max(temp_list)
				if max_num>128:
					max_num=255
				elif max_num<128:
					max_num=0
				kirsch_img[i][j]=max_num
		kirsch_img=np.uint8(kirsch_img)
		cv2.imwrite('C:/Users/Administrator/Desktop/kirsch_img_128.bmp',kirsch_img)
		show_img('kirsch_img',kirsch_img)
		#print(mask)
	
	def generate_original_list(self,i,j,arr):
		temp=[]
		temp.append([arr[i-1][j-1],arr[i-1][j],arr[i-1][j+1]])
		temp.append([arr[i][j-1],arr[i][j],arr[i][j+1]])
		temp.append([arr[i+1][j-1],arr[i+1][j],arr[i+1][j+1]])
		return temp
	
	def convolution_operation(self,original_list,mask):
		result=0
		#print(type(original_list[0][0]))
		for i in range (3):
			for j in range(3):
				result+=original_list[i][j]*mask[i][j]
		#print(type(result))
		return result
	
	def main(self):
		self.roberts()
		self.sobel()
		self.laplace()
		self.kirsch()
example=edge_detection('C:/Users/Administrator/Desktop/lena.bmp')
example.main()