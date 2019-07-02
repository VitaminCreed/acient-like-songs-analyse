#encoding=gbk
from snownlp import SnowNLP
import re
import random
import os
import jieba
import jieba.analyse
import json
import pygal
import wordcloud
from collections import Counter


stopwords_=['不知','不得','不见','不能','不如','不是','何必','不可','处处','何时','谁知','何如','如何','何处','何人','何事']
screen_words=['，','。','在','不','有','与','去','为','无','是','人','我','谁','还','上','来','将','中','亦','多','更',
	'欲','日','得','见','已','时','-','年','向','又','尽','下','道','一','却','从','如','新','之','到','和','皆','看',
	'好','未','出','何处','兮','）','不知','后','事','起','对','自','□','里','若','坐','开','”','曾','才','岂','能','过',
	'听','地','路','今日','吾','处','此','同','前','}','高','{','生','他','且','不可','入','“',']','[','即','说','行',
	'便','不见','今','应','知','初','君','被','无人','都','但','吹','犹','至','也','作','久','岁','似','不得','共','非',
	'间','相','声','？','闻','可','外','垂','使','所','三','如何','遶','随','隔','连','迟','身','罢','待','把','须',' ','的'
	,'你','\n','这','着','/','就','再','曾','了','而','她','要','(',')','那','只','做','、']

pos=0 #诗歌的积极概率
l_pos=0 #歌词的积极概率
l=0 #选取的诗歌数量
l_l=1 #选取的歌词数量
def files_combination(file_path): #遍历一个文件夹下所有诗词文件  
    words=''  
    i=1  
    for file_name in os.listdir(file_path):  
        print(i)  
        i=i+1  
        hh=words_combination(file_path+'\\'+file_name)  
        words=words+hh  
    return words  
  
def words_emotion(file_name):#从文件中随机抽取古诗词  
    sentence_combination=''  
    global pos #使用全局变量  
    global l  
    with open(file_name,'r',encoding='UTF-8') as f:  
        shiji=json.load(f)  
        for zidian in shiji:  
            shi=zidian["paragraphs"]  
            for sentence in shi:  
                a=random.randint(0,100)#生成随机数  
                if a==30:#随机抽样，选取原文本的百分之一  
                    s = SnowNLP(sentence)#进行情感分析  
                    pos=pos+s.sentiments  
                    l=l+1#统计选取的数量  
                    sentence_combination=sentence+sentence_combination  
    return sentence_combination  
def lyric_emotion():#对歌词进行情感分析
	global l_l
	global l_pos
	lyric=''
	for file_name in os.listdir(r'\lyric'):
		with open(r'lyric\\' + file_name) as lrc:
			for line in lrc:
				words = re.sub(r'\[.+\]', '', line) 
				if '：' not in words:
					l_l=l_l+1
					s=SnowNLP(words)
					l_pos=l_pos+s.sentiments
					lyric=lyric+words

def gulong():#古龙小说的分析
	p1=0
	l1=0
	for file_name in os.listdir(r'ziliao\《古龙全集 76部》全(TXT)作者：古龙'):
		with open(r'ziliao\《古龙全集 76部》全(TXT)作者：古龙\\' + file_name) as f2:
			p2=0
			l2=0
			for line in f2:
				a=random.randint(0,100)#生成随机数  
				if a<30:
					l2=l2+1
					s=SnowNLP(line)
					p2=p2+s.sentiments
			p2=p2/l2
			print(file_name+' '+str(p2))
	
def create_cloud(words,stop_words,name):  
	cut_words = jieba.cut(words)       #生成词云图片
	word_co=','.join(cut_words)
	w=wordcloud.WordCloud(font_path=r'C:\Windows\Fonts\STKAITI.TTF',
		background_color="white",width=2000,height=1500,stopwords=stopwords_,
		max_words=300,max_font_size=225)
	w.generate(word_co)
	file_path=name+'_picture.png'
	w.to_file(file_path)
	
def xuezhong():  #雪中悍刀行的分析
	words=''
	with open(r'ziliao\雪中悍刀行.txt') as f2:
		p2=0
		l2=0
		for line in f2:
			a=random.randint(0,100)#生成随机数  
			if a<10:
				l2=l2+1
				s=SnowNLP(line)
				p2=p2+s.sentiments
				print(a)
				words=words+line
		p2=p2/l2
		print(str(p2))
	return words

if __name__=='__main__':
	
	words=xuezhong()
	create_cloud(words,stopwords_,'xuezong')
	

