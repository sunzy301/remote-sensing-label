# coding=utf-8
# 图片爬虫
# 用于CNN fine-tuned数据获取
import re
import urllib.request
import os
import socket
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import tkinter
import tkinter.filedialog

def proceed_a_word(word,phantomjs_path,base_directory):
    print("当前关键词:"+word)
    print(base_directory)
    target_directroy=base_directory+'/'+word+'/'
    browser=webdriver.PhantomJS(phantomjs_path)
    URL="http://image.baidu.com/search/index?tn=baiduimage&word="+urllib.request.quote(word)+"/"
    try:
        browser.set_window_size(25000000,25000000)
        browser.get(URL)
        time.sleep(1)
    except:
        browser.quit()
        return -1
    try:
        os.mkdir(base_directory+'/'+word)
    except:
        print("创建文件夹失败")
        browser.quit()
        return -2
    info_file=open(target_directroy+word+'.txt','w')
    time.sleep(2)
    to_bottom="var q=document.documentElement.scrollTop=25000000"#This sentence is influence by the window size.
    browser.execute_script(to_bottom)
    imglist=browser.find_elements_by_class_name("imgitem")
    img_no=1
    for imgitem in imglist:
        try:
            img_URL=imgitem.get_attribute("data-objurl")
            img_title=imgitem.get_attribute("data-title")
            urllib.request.urlretrieve(img_URL,target_directroy+'%s.jpg' % img_no)
            info_file.write(img_title+'\n')
            print('%s'%img_no)
            img_no+=1
            if img_no>1000:
                break
        except:
            pass
    info_file.close()
    browser.quit()
    return 0
        
        
socket.setdefaulttimeout(10)
print("选择phantomjs可执行文件")
phantomjs_path=tkinter.filedialog.askopenfilename()
print("选择关键词文件")
file_words=tkinter.filedialog.askopenfile()
base_directory=tkinter.filedialog.askdirectory()
word_no=0
current_word=file_words.readline()
current_word=current_word.strip('\n')
while current_word!='':
    search_failed_times=0
    while True:
        if proceed_a_word(current_word,phantomjs_path,base_directory)==-1:
            search_failed_times+=1
            if search_failed_times>20:
                print("当前关键词搜索失败")
                break
            else:
                print("连接失败,正在重新尝试")
        else:
            break
    word_no+=1
    current_word=file_words.readline()
    current_word=current_word.strip('\n')
print("处理结束")