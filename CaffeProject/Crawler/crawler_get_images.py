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
import threading
import _thread

def create_directory(base_directory,word):
    directory_exist=False
    for directory_name in os.listdir(base_directory+'/'):
        if directory_name==word:
            directory_exist=True
            break
    if directory_exist==False:
        os.mkdir(base_directory+'/'+word)

def analyze_dowload_progress(target_directory,word,last_URL):
    file_existed=False
    for file_name in os.listdir(target_directory):
        if file_name==word+'.txt':
            file_existed=True
            break
    if file_existed==False:
        return 1
    _img_no=0
    origin_file=open(target_directory+word+'.txt','r')
    for line in origin_file:
        if line!='':
            _img_no+=1
        else: 
            break
    _img_no+=1
    origin_file.close()
    for file_name in os.listdir(target_directory):
        if file_name=='%s.jpg'%_img_no:
            os.remove(target_directory+file_name)
            break
    return _img_no

def get_last_URL(target_directory,word):
    origin_file=open(target_directory+word+'.txt','r')
    for line in origin_file:
        if line!='':
            last_URL=line.split(' ',1)[0]
        else: 
            break
    origin_file.close()
    return last_URL
                    

def proceed_a_word(word,phantomjs_path,base_directory):
    print("当前关键词:"+word)
    target_directory=base_directory+'/'+word+'/'
    browser=webdriver.PhantomJS(phantomjs_path)
    URL="http://image.baidu.com/search/index?tn=baiduimage&word="+urllib.request.quote(word)+"/"
    try:
        browser.set_window_size(25000000,25000000)
        browser.get(URL)
        time.sleep(1)
    except:
        browser.quit()
        return -1 
    time.sleep(2)
    to_bottom="var q=document.documentElement.scrollTop=25000000"#This sentence is influence by the window size.
    browser.execute_script(to_bottom)
    imglist=browser.find_elements_by_class_name("imgitem")
    img_no=0
    for imgitem in imglist:
        img_no+=1
    if img_no<600:#This sentence prevents that the page isn't loaded completely.However,there is another situation:the number of images is less than 1000.
        browser.quit()
        return -1
    create_directory(base_directory+"/",word)
    last_URL=''
    img_no=analyze_dowload_progress(target_directory,word,last_URL)
    if img_no==1001:
        print('%s 已经完成'%word)
        browser.quit()
        return 0
    download_start=False
    if img_no==1:
        download_start=True
    else:
        last_URL=get_last_URL(target_directory,word)
    info_file=open(target_directory+word+'.txt','a')
    for imgitem in imglist:
        if download_start==False:
            if imgitem.get_attribute("data-objurl")==last_URL:
                download_start=True
            continue
        try:
            img_URL=imgitem.get_attribute("data-objurl")
            img_title=imgitem.get_attribute("data-title")
            urllib.request.urlretrieve(img_URL,target_directory+'%s.jpg' % img_no)
            info_file.write(img_URL+' '+img_title+'\n')
            info_file.flush()
            print('%s:%s'%(word,img_no))
            img_no+=1
            if img_no>1000:
                break
        except:
            pass
    info_file.close()
    browser.quit()
    return 0
        
def proceed_thread(current_word,phantomjs_path,base_directory):
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
        
socket.setdefaulttimeout(10)
print("选择phantomjs可执行文件")
phantomjs_path=tkinter.filedialog.askopenfilename()
print("选择关键词文件")
file_words=tkinter.filedialog.askopenfile()
print("选择保存根文件夹")
base_directory=tkinter.filedialog.askdirectory()
word_no=0
current_word=file_words.readline()
current_word=current_word.strip('\n')
threads=[]
while current_word!='':
    threads.append(threading.Thread(target=proceed_thread,args=(current_word,phantomjs_path,base_directory)))
    word_no+=1
    current_word=file_words.readline()
    current_word=current_word.strip('\n')
for t in threads:
    t.setDaemon(True)
    t.start()
for t in threads:#Some of the threads are killed before they are finished,which remains a mystery.
    t.join()
print("处理结束")