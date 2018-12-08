import cv2
import numpy as np
import copy

def show_img(name,img):
	cv2.namedWindow(name)#cv2.WINDOW_NORMAL可以手动改变大小
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def image_binarization(image):
	image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	image= cv2.medianBlur(image,3)
	binary = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,5)
	return binary
	 
	bg_color = 255
	row_length = len( image )
	column_length = len( image[ 0 ] )
 
	image_in_rows = []
 
	is_last_blank_row = True
	last_row_index = 0
	for row in range( 0, row_length ):
		is_row_blank = True
		for column in range( 0, column_length ):
			if image[ row ][ column ] == bg_color:
				pass
			else:
				is_row_blank = False
				break
 
		if is_last_blank_row == is_row_blank:
			pass
		else:
			if is_row_blank == False:
				image[ row - 1 ] = [ 0 for column in range( 0, column_length ) ]
 
				# 本行开始位置的行号
				last_row_index = row
			else:
				image[ row ] = [ 0 for column in range( 0, column_length ) ]
 
				# 已经找到本行开始位置和结束位置的行号，然后复制一行
				image_in_rows.append( image[ last_row_index : row ] )
 
			is_last_blank_row = is_row_blank
 
	# 第一个返回值是划了分行线的完整图像
	# 第二个返回值是一个List，每个元素都是分割出来的一行
	return image, image_in_rows
 

def main():
	image = cv2.imread( "C:/Users/Administrator/Desktop/2.jpg")
	image_binary=image_binarization(copy.copy(image))
	#show_img('binary',image_binary)
	cv2.imwrite('binary.jpg',image_binary)
	
if __name__=="__main__":
	main()
	