import cv2
import numpy as np
import matplotlib.pyplot as plot

def image_binarization( image ):

 
 
	for row in range( 0, row_length ):
		for column in range( 0, column_length ):
			if image[row][column]>127:
				image[row][column]=255
			else:
				image[row][column]=0
			#if image[ row ][ column ] == bg_color:
				#if bg_color > 127:
					#image[ row ][ column ] = 255
				#else:
					#image[ row ][ column ] = 0
 
			#else:
				#if bg_color > 127:
				   # image[ row ][ column ] = 0
				#else:
				   # image[ row ][ column ] = 255
 
 
	return image
 
def image_row_split( image ):
	 
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
 
def image_char_split( image, image_row_splited ):
 
	image_save( "image_test.png", image )
 
	bg_color = 255
	row_length = len( image )
	column_length = len( image[ 0 ] )
 
	is_last_blank_column = True
	last_left_line_index = 0
	chars_splited = []
	for column in range( 0, column_length ):
		is_column_blank = True
		for row in range( 0, row_length ):
			if image[ row ][ column ] == bg_color:
				pass
			else:
				is_column_blank = False
				break
 
		if is_last_blank_column == is_column_blank:
			pass
		else:
			if is_column_blank == False:
				for row in range( 0, row_length ):
					image_row_splited[ row ][ column - 1 ] = 0
 
				# 找到本列字符的开始列号
				last_left_line_index = column
			else:
				single_char = []
				for row in range( 0, row_length ):
					image_row_splited[ row ][ column ] = 0
 
					# 有了开始和结束的列号，然后逐行复制，形成一个完整的字符
					single_char.append( image[ row ][ last_left_line_index : column ] )
 
				# 将分割出的每一个字符加入List
				# 注意需要将Python的List转换为numpy的多维数组（即png图像）
				chars_splited.append( np.asarray( single_char ) )
 
			is_last_blank_column = is_column_blank
 
	return chars_splited
 
def main():
	 
	image = image_read( "C:/Users/Administrator/Desktop/3.jpg", mode = cv2.IMREAD_GRAYSCALE )
	image_save( "number_gray.png", image )
	 
	image_binary = image_binarization( np.copy( image ) )
	image_save( "number_binary.png", image_binary )
 
	# 得到分好行的图像及划了分割线的完整图像
	image_row_lined, image_row_splited = image_row_split( np.copy( image_binary ) )
 
	# 逐行进行分割
	for r in range( 0, len( image_row_splited ) ):
		image_save("number_in_row_"+str(r)+".png",image_row_splited[r])
 
		# 得到每一行所分割出的字符
		image_char_splited =image_char_split(np.copy(image_row_splited[r]), np.copy(image_row_lined))
		 
		# 对每一个字符进行处理
		for c in range( 0, len( image_char_splited ) ):
 
			# 行假设图像的高>宽，则设定最长的边是高
			max_length = len( image_char_splited[ c ] )
			# 计算高宽比
			ratio = max_length / len( image_char_splited[ c ][ 0 ] )
 
			if len( image_char_splited[ c ][ 0 ] ) > max_length:
				# 如果高<宽
				# 设定最长的边是宽
				max_length = len( image_char_splited[ c ][ 0 ] )
				# 计算宽高比
				ratio = max_length / len( image_char_splited[ c ] )
 
				# 将高<宽的图像放大10倍，并使其高=宽 
				large_image = cv2.resize( image_char_splited[ c ], 
						( max_length * 10, 
							int(len(image_char_splited) * ratio * 10))) 
			else: 
				# 如果高>宽
				# 将高>宽的图像放大10倍，并使其高=宽
				large_image = cv2.resize( image_char_splited[ c ], 
						( max_length * 10, 
							int(len(image_char_splited[0])*ratio*10)))
 
			# 放大之后的图像会再次变为灰度图（依图像放大的算法而定）
			# 需要将放大之后的图像再次手动处理为二值图，然后保存
			image_save( "number_" + str( r ) + "_" + str( c ) + ".png", 
				image_binarization( large_image )) 
 
if __name__ == "__main__":
	 
	main()