import os
from pypinyin import lazy_pinyin,pinyin

from importlib import import_module
import re

#修改spiderheart文件夹里的中文名字
def change_c_into_e(dirs):
    print(dirs)
    for i in dirs:
        path='./'
        old_name = path +'%s'%i
        print(old_name)
        b = lazy_pinyin(i)
        newname = ''.join(b)
        print(newname)
        newname = path+'%s'%newname
        print(newname)
        os.rename(old_name,newname)

def file_jia(spider_name):
    path = spider_name.split("-", 1)[0]
    print(path)
    md = import_module(root_path + "." + path + "." + spider_name)
    print(md)
    for i in ff:
        f(i)
def marry_c(chinese_string):
    pattern =re.compile(r'[\u4E00-\u9FA5]?.*?[\u4E00-\u9FA5]')
    c=re.findall(pattern,chinese_string)
    return c
def match_spj(dir):
    pattern = re.compile(r'scrapyProj')
    b = []
    for i in dir:
        s = re.findall(pattern,i)
        s=''.join(s)
        s=s.replace(' ','')
        b.append(s)
    #b=b.pop('')
    print(b)
def main():
    path = "./"
    dir = os.listdir(path)
    print(dir)
    match_spj(dir)
    #change_c_into_e(dirs)
    c = os.getcwd()
    #print(c)
    ff = ['住建部-云南建筑']
    dirs = file_jia(ff)
    #print(dirs)

if __name__ =='__main__':
    main()
