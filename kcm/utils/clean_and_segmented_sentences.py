# -*- coding: utf-8 -*-
import os
# ja
# MeCab has some bug
# so i cannot put these import statement into ja function scope ...
# TH: to install pythainlp for stopwords and segmentation, please install by the command line
# pip install pythainlp
# import MeCab
# mecab = MeCab.Tagger("-Ochasen")

def clean_and_segmented_sentences(lang, article):
	""" Do segmentation and removing stopwords for a wiki page

	Parameters
	----------
	lang : {str}. is the same abbreviation as wiki use
	article : {str}. plain text of wiki page. In kcm/__init__.py, var article is the plain text of wiki page for clean_and_segmented_sentences function

	Returns
	-------
	seg : {generator}, shape (numbers of sentences in an article, numbers of words in a sentence)
	An 2d array which contains bunches of segmentations of a sentence.
	e.g., [
		[['cake', 'n'], ['food', 'n']]
		...
		...
		...
	]
	"""
	if lang == 'zh':
		return zh(article)
	elif lang == 'th':
		return th(article)
	elif lang == 'en':
		pass
	elif lang == 'ja':
		return ja(article)

def zh(article):
	# for zh 
	from udicOpenData.stopwords import rmsw
	from opencc import OpenCC
	from itertools import chain
	openCC = OpenCC('s2t')

	def peek(iterable):
		try:
			first = next(iterable)
		except StopIteration:
			return None
		return True, chain([first], iterable)

	for i in article['text'].split('。'):
		seg = rmsw(openCC.convert(i), flag=True)
		seg = peek(seg)
		if seg is None:
			continue
		else:
			boolean, seg = seg
			yield seg

def th(article):
	# Parameters
	# ----------
	# article = {'url': 'https://th.wikipedia.org/wiki?curid=792', 'title': 'โอเพนออฟฟิศดอตอ็อก', 'id': '792', 'text': 'โอเพนออฟฟิศดอตอ็อก\n\nโอเพนออฟฟิศดอตอ็อก ( ย่อว่า OO.o หรือ OOo) เป็นชุดซอฟต์แวร์สำนักงานที่ทำงานบนหลายระบบปฏิบัติการ เผยแพร่ในรูปแบบซอฟต์แวร์เสรี เขียนขึ้นโดยใช้ชุดเครื่องมือส่วนต่อประสานกราฟิกของตัวเอง รองรับรูปแบบโอเพนด็อกคิวเมนต์ (ODF) ซึ่งเป็นมาตรฐานไอเอสโอ/ไออีซีเพื่อการแลกเปลี่ยนข้อมูล และใช้เป็นรูปแบบแฟ้มพื้นฐาน อีกทั้งยังรองรับรูปแบบเอกสารจากไมโครซอฟท์ ออฟฟิศ และอื่น ๆ กระทั่งเดือนพฤศจิกายน พ.ศ. 2552 โอเพนออฟฟิศดอตอ็อกรองรับมากกว่า 110 ภาษา \n\nโอเพนออฟฟิศดอตอ็อกพัฒนาต่อยอดมาจากสตาร์ออฟฟิศ (StarOffice) ซอฟต์แวร์สำนักงานจากสตาร์วิชัน (StarVision) ซึ่งภายหลังถูกควบกิจการโดยซัน ไมโครซิสเต็มส์ เมื่อเดือนสิงหาคม พ.ศ. 2542 รหัสต้นฉบับของชุดซอฟต์แวร์นี้เผยแพร่เมื่อเดือนกรกฎาคม พ.ศ. 2543 ด้วยจุดประสงค์เพื่อช่วงชิงส่วนแบ่งตลาดจากไมโครซอฟท์ ออฟฟิศ โดยเพิ่มทางเลือกเสรีต่อผู้ใช้และผู้พัฒนา รุ่นหลัง ๆ ของสตาร์ออฟฟิศจะใช้โอเพนออฟฟิศดอตอ็อกเป็นพื้นฐานแทน และเพิ่มองค์ประกอบที่เป็นกรรมสิทธิ์ของสตาร์ออฟฟิศ \n\nซอฟต์แวร์และโครงการนี้อาจเรียกอย่างไม่เป็นทางการว่า "โอเพนออฟฟิศ" แต่ชื่อนี้เป็นเครื่องหมายการค้าของบริษัทในเนเธอร์แลนด์ ซึ่งก่อตั้งโดย Wouter Hanegraaff และมีการใช้ชื่อนี้ในออเรนจ์สหราชอาณาจักรอีกเช่นกัน จึงทำให้โครงการนี้ต้องใช้ชื่อว่า "โอเพนออฟฟิศดอตอ็อก" เป็นชื่อทางการ \n\nในประเทศไทย เคยมีการนำ โอเพนออฟฟิศดอตอ็อกมาพัฒนาต่อเพื่อให้ใช้งานภาษาไทยได้ โดยสองตัวหลักที่เป็นที่รู้จักกันในวงกว้าง คือ ปลาดาวออฟฟิศ ที่สนับสนุนโดย ซัน ไมโครซิสเต็มส์ (ประเทศไทย) และ ออฟฟิศทะเล ที่พัฒนาโดยเนคเทค \n\nในปีค.ศ. 1999 ซันไมโครซิสเต็มส์ได้ซื้อซอฟต์แวร์ สตาร์ออฟฟิศ จากบริษัทซอฟต์แวร์ของเยอรมนีชื่อ สตาร์ดิวิชัน ซันได้อนุญาตให้ใช้สตาร์ออฟฟิศ เวอร์ชัน 5.2 ได้โดยไม่มีค่าใช้จ่าย ในปีค.ศ. 2000 ซันได้เผยแพร่ซอร์สโค้ดของสตาร์ออฟฟิศภายใต้สัญญาอนุญาต LGPL และ Sun Industry Standards Source License (SISSL) เพื่อจะสร้างชุมชนโอเพนซอร์ส โครงการใหม่ที่ตั้งขึ้นมีชื่อว่า OpenOffice.org เว็บไซต์ของโอเพนออฟฟิศดอตอ็อกเริ่มเปิดใช้งานในเดือนตุลาคม ปี 2000\nโอเพนออฟฟิศดอตอ็อก 1.0 เปิดตัวในเดือนพฤษภาคม ค.ศ. 2002\n\nซันประกาศยุติการใช้งาน SISSL ในปี ค.ศ. 2005 โครงการโอเพนออฟฟิศดอตอ็อกจึงใช้เพียงสัญญาอนุญาตแบบ LGPL ในเวอร์ชันหลังจากนั้นมา โอเพนออฟฟิศดอตอ็อกเปิดตัวโปรแกรมเวอร์ชัน 2.0 ในเดือนตุลาคม ค.ศ. 2005 โดยใช้รูปแบบไฟล์ OpenDocument แทน OpenOffice.org XML\n\nโอเพนออฟฟิศดอตอ็อก 3.0 เปิดตัวในเดือนตุลาคม ค.ศ. 2008 โดยสามารถเปิดเอกสารในรูปแบบ Office Open XML ได้ และรองรับรูปแบบไฟล์ OpenDocument 1.2\n\nซันไมโครซิสเต็มส์ยังคงทำตลาดสตาร์ออฟฟิศเป็นซอฟต์แวร์เชิงพานิชย์ โดยใช้โอเพนออฟฟิศดอตอ็อกเป็นฐาน และเพิ่มความสามารถบางอย่างเข้าไป\n\n\n\n\n'}
	# for th
	from pythainlp.corpus import stopwords
	from pythainlp.tokenize import word_tokenize
	from pythainlp.tag import pos_tag
	import string
	punctuation = list(string.punctuation)
	extraPunctions = ['。','/','(',')','.','ํ','|','๐','OO','o','ก','ข','ฃ','ค','ฅ','ฆ','ง','จ','ฉ','ช','ซ','ฌ','ญ','ฎ','ฏ','ฐ','ฑ','ฒ','ณ','ด','ต','ถ','ท','ธ','น','บ','ป','ผ','ฝ','พ','ฟ','ภ','ม','ย','ร','ล','ว','ศ','ษ','ส','ห','ฬ','อ','ฮ']
	for e in extraPunctions:
		punctuation.append(e)
	thstopwords = stopwords.words('thai')
	for line in article['text'].split('\n'): 
		if line:
			line = [i for i in word_tokenize(line,engine='newmm') if i not in thstopwords and i not in punctuation]
			if not line: 
				continue
			POSlist = pos_tag(line,engine='artagger')
			yield POSlist

def ja(article):
	for line in article['text'].split('。'):
		line = line.strip()
		if line:
			yield ((i.split('\t')[0], None) for i in mecab.parse(line).split('\n')[:-2])

if __name__ == '__main__':
	# Change lang to the one you're testing now
	lang = 'zh'

	article = {
		'text':'the context of a wiki page written in your language'
	}
	for i in clean_and_segmented_sentences(lang, article):
		print(list(i))
