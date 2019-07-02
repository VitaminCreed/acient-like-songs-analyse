#encoding=utf-8
import re
import os
import jieba
import jieba.analyse
import json
import pygal
import wordcloud
from collections import Counter


jieba.load_userdict(r"意象词典.txt")
stopwords_=['不知','不得','不见','不能','不如','不是','何必','不可','处处','何时','谁知','何如','如何','何处','何人','何事']
screen_words=['，','。','在','不','有','与','去','为','无','是','人','我','谁','还','上','来','将','中','亦','多','更',
	'欲','日','得','见','已','时','-','年','向','又','尽','下','道','一','却','从','如','新','之','到','和','皆','看',
	'好','未','出','何处','兮','）','不知','后','事','起','对','自','□','里','若','坐','开','”','曾','才','岂','能','过',
	'听','地','路','今日','吾','处','此','同','前','}','高','{','生','他','且','不可','入','“',']','[','即','说','行',
	'便','不见','今','应','知','初','君','被','无人','都','但','吹','犹','至','也','作','久','岁','似','不得','共','非',
	'间','相','声','？','闻','可','外','垂','使','所','三','如何','遶','随','隔','连','迟','身','罢','待','把','须',' ','的'
	,'你','\n','这','着','/','就','再','曾','了','而','她','要','(',')','那','只','做','、']



def files_combination(file_path):           #将一个文件夹下的所有文件诗词句合并
	words=''
	i=1
	for file_name in os.listdir(file_path):
		print(i)
		i=i+1
		words=words+words_combination(file_path+'\\'+file_name)
	return words

def words_combination(file_name):           #将一个文件中的诗词句提取出来
	sentence_combination=''
	with open(file_name,'r',encoding='UTF-8') as f:
		shiji=json.load(f)                  #载入诗句
		for zidian in shiji:
			shi=zidian["paragraphs"]
			for sentence in shi:
				sentence_combination=sentence+sentence_combination
	return sentence_combination
	
def create_cloud(words,stop_words,name):  
	cut_words = jieba.cut(words)       #生成词云图片
	word_co=','.join(cut_words)
	w=wordcloud.WordCloud(font_path=r'C:\Windows\Fonts\STKAITI.TTF',
		background_color="white",width=2000,height=1500,stopwords=stopwords_,
		max_words=300,max_font_size=225)
	w.generate(word_co)              #生成词云
	file_path=name+'_picture.png'    #保存至图片
	w.to_file(file_path)

def create_chart(words,stop_words,name):  #绘制统计图表
	cut_words = jieba.cut(words)                     
	count = Counter(cut_words)          #统计字频
	sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)#从大到小排序
	
	i=0                                        #绘制图表
	while i<100:
		if sorted_count[i][0] in screen_words:
			del sorted_count[i]
		else:
			i=i+1
	chart=pygal.Bar()
	chart.title=name
	x_lables=[]
	y_lable=[]
	for item in sorted_count[0:35]:
		x_lables.append(item[0])
		y_lable.append(item[1])
	chart.x_labels=x_lables
	chart.x_title='词'
	chart.y_title='频率'
	chart.add('cipin',y_lable)
	chart_path=name+'_chart.svg'
	chart.render_to_file(chart_path)
	

def screen(words):        #过滤函数，将诗句中掺杂的标点符号和注释过滤掉，仅保留纯正的诗句
	s_words = re.sub('（.*?）', '', words)
	s_words = re.sub('《.*?》', '', s_words)
	s_words = re.sub('【.*?】', '', s_words)
	#s_words = re.sub('(.*?)', '', s_words)
	return s_words

def creat_all(name):    #将所有对诗词进行处理的函数串联起来
	path='ziliao\\'+name
	words=files_combination(path)
	words=screen(words)
	create_cloud(words,stopwords_,name)
	create_chart(words,screen_words,name)
	
def lyric():           #对歌词进行处理的函数
	lyric=''
	for file_name in os.listdir('lyric'):    #载入歌词文件
		with open('lyric/' + file_name) as lrc:
			for line in lrc:
				words = re.sub(r'\[.+\]', '', line) 
				if '：' not in words:
					lyric=lyric+words
	cut_words = jieba.cut(lyric) # Jieba中文分词，将一句歌词切割成多个词语	
	create_cloud(lyric,stopwords_,'xiandai')#创建词云
	create_chart(lyric,screen_words,'xiandai')#创建图表
	
	
if __name__=='__main__':
	creat_all('wudai')
	creat_all('tangshi')
	creat_all('songshi')
	creat_all('songci')
	lyric() 
