import numpy as np
import cv2
import math
import copy
def show_img(name,img):
	cv2.namedWindow(name)#cv2.WINDOW_NORMAL可以手动改变大小
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

class fourier_filter(object):
	def __init__(self,path):
		self.original_img=cv2.imread(path,0)
	
	def high_pass_filter(self,img,threshold):
		f=np.fft.fft2(img)
		fshift=np.fft.fftshift(f)
		row,col=img.shape
		mask=np.ones(img.shape)
		mask[int(row/2-threshold):int(row/2+threshold),int(col/2-threshold):int(col/2+threshold)]=0
		fshift=fshift*mask
		fdshift=np.fft.ifftshift(fshift)
		img_new=np.uint8(np.abs(np.fft.ifft2(fdshift)))
		cv2.imwrite('C:/Users/Administrator/Desktop/high_pass_filter.bmp',img_new)
		show_img('new',img_new)
	
	def low_pass_filter(self,img,threshold):
		f=np.fft.fft2(img)
		fshift=np.fft.fftshift(f)
		row,col=img.shape
		mask=np.zeros(img.shape)
		mask[int(row/2-threshold):int(row/2+threshold),int(col/2-threshold):int(col/2+threshold)]=1
		fshift=fshift*mask
		fdshift=np.fft.ifftshift(fshift)
		img_new=np.uint8(np.abs(np.fft.ifft2(fdshift)))
		cv2.imwrite('C:/Users/Administrator/Desktop/low_pass_filter.bmp',img_new)
		show_img('new',img_new)

	def add_space_domain_sin(self,img):
		s=img.shape
		new_img=copy.copy(img)
		for i in range(s[0]):
			for j in range(s[1]):
				new_img[i][j]=img[i][j]+150*0.2*math.sin(0.3*math.pi*j+math.pi*1.6)
				if new_img[i][j]>255:
					new_img[i][j]=255
				elif new_img[i][j]<0:
					new_img[i][j]=0
		new_img=np.uint8(new_img)
		cv2.imwrite('C:/Users/Administrator/Desktop/add_space_domain_sin.bmp',new_img)
		show_img('new',new_img)
	
	def add_frequency_domain_sin(self,img,d0):
		s=img.shape
		f=np.fft.fftshift(np.fft.fft2(img))
		f[int(s[0]/2+1)][int(s[1]/2+1-d0)]=0.3*f.max()
		f[int(s[0]/2+1)][int(s[1]/2+1+d0)]=0.3*f.max()
		new_img=np.abs(np.fft.ifft2(np.fft.ifftshift(f)))
		new_img=np.uint8(self.normalize(s,new_img))
		cv2.imwrite('C:/Users/Administrator/Desktop/add_frequency.bmp',new_img)
		show_img('add frequency',new_img)
		
	def gaussian_pass_filter(self,img,rh,rl,c,D0):
		s=img.shape
		print(s)
		log_img=np.zeros(s)
		for i in range(s[0]):
			for j in range(s[1]):
				log_img[i][j]=math.log(img[i][j]+1)
		f=np.fft.fftshift(np.fft.fft2(log_img))
		new_fh=copy.copy(f)
		new_fl=copy.copy(f)
		center_x=s[0]/2
		center_y=s[1]/2
		for i in range(s[0]):
			for j in range(s[1]):
				D=math.sqrt((i-center_y)**2+(j-center_x)**2)
				h_h=(rh-rl)*(1-math.exp(c*(-D**2/D0**2)))+rl
				h_l=(rh-rl)*(math.exp(c*(-D**2/D0**2)))+rl
				new_fh[i][j]=h_h*f[i][j]
				new_fl[i][j]=h_l*f[i][j]
		new_h_img=np.exp(np.fft.ifft2(np.fft.ifftshift(new_fh)))-1
		new_l_img=np.exp(np.fft.ifft2(np.fft.ifftshift(new_fl)))-1
		new_h_img=np.abs(new_h_img)
		new_l_img=np.abs(new_l_img)
		new_h_img=self.normalize(s,new_h_img)
		new_l_img=self.normalize(s,new_l_img)
		new_h_img=np.uint8(new_h_img)
		new_l_img=np.uint8(new_l_img)
		cv2.imwrite('C:/Users/Administrator/Desktop/new_h_img.bmp',new_h_img)
		cv2.imwrite('C:/Users/Administrator/Desktop/new_l_img.bmp',new_l_img)
		show_img('new_h_img',new_h_img)
		show_img('new_l_img',new_l_img)
	
	def normalize(self,s,img):
		maximum=img.max()
		minimun=img.min()
		new_img=copy.copy(img)
		for i in range(s[0]):
			for j in range(s[1]):
				new_img[i][j]=int((new_img[i][j]-minimun)/(maximum-minimun)*255)
		return(new_img)

F=fourier_filter('C:/Users/Administrator/Desktop/cave.jpg')
#F.high_pass_filter(F.original_img,6)
#F.low_pass_filter(F.original_img,8)
#F.add_space_domain_sin(F.original_img)
#F.add_frequency_domain_sin(F.original_img,30)
F.gaussian_pass_filter(F.original_img,2.5,0.5,2,10)