#! /usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < unicode_tools.py >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/01 >
#	> Last Changed: 
#	> Description:
#################################################################

#!/usr/bin/env python
 
"""	汉字处理的工具:
	判断unicode是否是汉字，数字，英文，或者其他字符。
	全角符号转半角符号。
	http://www.cppblog.com/sunrise/archive/2012/08/29/188654.html	
"""



def is_chinese(uchar):
	"""判断一个unicode是否是汉字"""
	if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
		return True
	else:
		return False
def is_number(uchar):
	"""判断一个unicode是否是数字"""
	if uchar >= u'\u0030' and uchar<=u'\u0039':
		return True
	else:
		return False
def is_alphabet(uchar):
	"""判断一个unicode是否是英文字母"""
	if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
		return True
	else:
		return False

def main():
	ch1 = u'爱'	
	ch = ch1
	print ch, "is_chinese?", is_chinese(ch)
	print ch, "is_alphabet?", is_alphabet(ch)
	print ch, "is_number?", is_number(ch)
	print ""

	ch2 = u'a'
	ch = ch2
	print ch, "is_chinese?", is_chinese(ch)
	print ch, "is_alphabet?", is_alphabet(ch)
	print ch, "is_number?", is_number(ch)
	print ""

	ch3 = u','
	ch = ch3
	print ch, "is_chinese?", is_chinese(ch)
	print ch, "is_alphabet?", is_alphabet(ch)
	print ch, "is_number?", is_number(ch)
	print ""

if __name__=="__main__":
	main()
