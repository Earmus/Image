import cv2
import numpy as np
import copy

def show_img(name,img):
	cv2.namedWindow(name)#cv2.WINDOW_NORMAL可以手动改变大小
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
class region_growing_method(object):
	def __init__(self,path_two_value,path_gray):
		self.two_value_img=cv2.imread(path_two_value,0)
		self.gray_img=cv2.imread(path_gray,0)
		self.s=self.two_value_img.shape
		self.label_img=np.zeros((self.s[0],self.s[1]))
		self.region_threshold_img=copy.copy(self.two_value_img)
		self.index={}
	
	def rgm(self):
		number=1
		for i in range(self.s[0]):
			for j in range(self.s[1]):
				if self.two_value_img[i][j]==0 and self.label_img[i][j]==0:
					self.generate_region(i,j,number)
					number+=1
	
	def generate_region(self,i,j,number):
		self.index[number]=[(i,j)]
		queue=[(i,j)]
		while len(queue)!=0:
			center=queue.pop(0)
			neighborhood=self.search_neighborhood(center)
			for temp in neighborhood:
				if self.label_img[temp[0]][temp[1]]==0:
					if self.two_value_img[temp[0]][temp[1]]==0:
						queue.append(temp)
						self.index[number].append(temp)
						self.label_img[temp[0]][temp[1]]=1
	
	def search_neighborhood(self,center):
		i=center[0]
		j=center[1]
		neighborhood=[]
		for m in range(-1,2):
			for n in range(-1,2):
				neighborhood.append((i+m,j+n))
		neighborhood.pop(4)
		return(neighborhood)
	
	
	def ostu(self,region): 
		r=0
		gray_statistics={}#像素的灰度值统计
		for i in range(256):
			gray_statistics[i]=0
		for temp in region:
			gray_statistics[self.gray_img[temp[0]][temp[1]]]+=1
		t_old=128
		t_new='original'
		while True:
			left_value=0;right_value=0;left_num=0;right_num=0
			for i in range(0,t_old+1):
				left_value+=i*gray_statistics[i]
				left_num+=gray_statistics[i]
			for j in range(t_old+1,255):
				right_value+=j*gray_statistics[j]
				right_num+=gray_statistics[j]
			if left_num==0 or right_num==0:
				t_new=0
				break
			t_new=int((left_value/left_num+right_value/right_num)/2)
			if t_new==t_old:
				break
			else:
				t_old=t_new
		number=0
		for temp in region:
			if self.gray_img[temp[0]][temp[1]]<t_new:
				self.region_threshold_img[temp[0]][temp[1]]=128
				number+=1
		r=number/len(region)
		return(r)
		#show_img('region_threshold_img',self.region_threshold_img)
		
	def main(self):
		ratio={}
		self.rgm()
		region_number=len(self.index)
		for i in range(region_number):
			r=self.ostu(self.index[i+1])
			ratio[i+1]=r
		print(ratio)
		cv2.imwrite('C:/Users/Administrator/Desktop/region_threshold_img.bmp',self.region_threshold_img)
		show_img('region_threshold_img',self.region_threshold_img)
		
example=region_growing_method('C:/Users/Administrator/Desktop/open_dajin.bmp','C:/Users/Administrator/Desktop/cell.bmp')
example.main()	