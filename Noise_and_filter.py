import cv2
import random
import itertools
import copy
import numpy

def show_img(name,img):
	cv2.namedWindow(name)#cv2.WINDOW_NORMAL可以手动改变大小
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
class Noise(object):#噪声
	def read(self,path):#读入要处理的图片
		self.original_img=cv2.imread(path)
		self.img=cv2.cvtColor(self.original_img,cv2.COLOR_BGR2GRAY)
		show_img('The original image',self.img)
			
		
	def salt_and_pepper_noise(self,SNR):#增加椒盐噪声
		im=copy.copy(self.img)
		s=im.shape
		ns=int((1-SNR)*s[0]*s[1])
		random_list=list(itertools.product(range(s[0]),range(s[1])))
		random_coordinate=random.sample(random_list,ns)#生成随机的不重复的二维坐标
		for i in random_coordinate:
			r=random.randint(0,1)
			if r==0:
				im[i[0]][i[1]]=0
			else:
				im[i[0]][i[1]]=255
		cv2.imwrite('salt_and_pepper_noise.jpg',im)
		show_img('Slat and perpper noise',im)
		return im
	
	def gaussian_noise(self,Xmean,sigma):#增加高斯噪声
		im=copy.copy(self.img)
		s=im.shape
		for i in range(s[0]):
			for j in range(s[1]):
				r=int(random.gauss(Xmean,sigma))
				im[i][j]=im[i][j]+r
				if im[i][j]>255:
					im[i][j]=255
				elif im[i][j]<0:
					im[i][j]=0
		cv2.imwrite('Gaussian noise.jpg',im)
		show_img('Gaussian noise',im)
		
	def impluse_noise(self,SNR,type):#可选择脉冲噪声类型 type={'white','black'}
		im=copy.copy(self.img)
		s=im.shape
		ns=int((1-SNR)*s[0]*s[1])
		random_list=list(itertools.product(range(s[0]),range(s[1])))
		random_coordinate=random.sample(random_list,ns)#生成随机的不重复的二维坐标
		if type=='white':
			for i in random_coordinate:
				im[i[0]][i[1]]=255
			cv2.imwrite('Impluse noise(White).jpg',im)
			show_img('Impluse noise(White)',im)
		else:
			for i in random_coordinate:
				im[i[0]][i[1]]=0
			cv2.imwrite('Impluse noise(Black).jpg',im)
			show_img('Impluse noise(Black)',im)

class Filter(object):#滤波
	def __init__(self,img):
		s=img.shape
		print(s)
		#if s[2] == 3:
			#self.bgr_img=img
		#else:
		self.grey_img=img
	
	def median_filter(self,Kernel):#中值滤波
		im=cv2.medianBlur(self.grey_img,Kernel)
		show_img('Median filter',im)
		cv2.imwrite('Median filter.jpg',im)
		return(im)
		
	def mean_filter(self,m,n):#均值滤波
		im=cv2.blur(self.grey_img,(m,n))
		show_img('Mean filter',im)
		cv2.imwrite('Mean filter.jpg',im)
		return(im)
	
	def grey_histogram_equalization(self):#灰色图直方图均衡化
		gray_statistics={}#像素的灰度值统计
		normalized_statistis={}#每一个像素值得频率计算
		translate_table={}#像素转换表
		new_img=copy.copy(img)
		for i in range(256):
			gray_statistics[i]=0
			normalized_statistis[i]=0
		s=self.grey_img.shape
		for i in range(s[0]):
			for j in range(s[1]):
				gray_statistics[self.grey_img[i][j]]+=1
		total=s[0]*s[1]
		for i in gray_statistics:
			normalized_statistis[i]=gray_statistics[i]/total
		for i in range(256):
			translate_table[i]=round(255*self.sum(normalized_statistis,i))
		for i in range(s[0]):
			for j in range(s[1]):
				new_img[i][j]=translate_table[self.grey_img[i][j]]
		show_img('Histogram Equalization',new_img)
		cv2.imwrite('Histogram Equalization.jpg',im)
	
	def bgr_histogram_equalization(self):#因为考虑到bgr三个维度，所以比灰度要再增加两个维度，其他步骤相同
		bgr_statistics=[{},{},{}]
		normalized_statistics=[{},{},{}]
		translate_table=[{},{},{}]
		new_img=copy.copy(self.bgr_img)
		for m in bgr_statistics:
			for i in range(256):
				m[i]=0
		print('The initial bgr_statistics has done!')
		for n in normalized_statistics:
			for i in range(256):
				n[i]=0
		print('The initial normalized_statistics has done!')
		s=self.bgr_img.shape
		total=s[0]*s[1]
		for i in range(s[0]):
			for j in range(s[1]):
				for index in range(3):
					bgr_statistics[index][self.bgr_img[i][j][index]]+=1
				print('(%d,%d) bgr_statistics has done!' % (i,j))
		print('The bgr_statistics has done!!')
		for index in range(3):
			for i in range(256):
				normalized_statistics[index][i]=bgr_statistics[index][i]/total
			print('normalized_statistics[%d] has done!' % index)
		for index in range(3):
			for i in range(256):
				translate_table[index][i]=round(255*self.sum(normalized_statistics[index],i))
			print('translate_table[%d] has done!' % index)
		for i in range(s[0]):
			for j in range(s[1]):
				for index in range(3):
					new_img[i][j][index]=translate_table[index][self.bgr_img[i][j][index]]
				print(new_img[i][j])
		show_img('Bgr Histogram Equalization',new_img)
		cv2.imwrite('Bgr Histogram Equalization.jpg',new_img)

	def sum(self,dict,num):#求和函数
		total=0
		for i in range(num):
			total+=dict[i]
		return total

'''		
im=Noise()
im.read('00367.png')
img=im.gaussian_noise(0,45)
img=im.impluse_noise(0.8,'white')
img=im.impluse_noise(0.8,'black')
img=im.salt_and_pepper_noise(0.8)
img=cv2.imread('landscape.jpg')
f=Filter(img)
f.median_filter(5)
f.mean_filter(3,5)
f.grey_histogram_equalization()
f.bgr_histogram_equalization()
'''