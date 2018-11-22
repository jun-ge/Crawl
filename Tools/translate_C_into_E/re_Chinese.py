import re
from pypinyin import lazy_pinyin,pinyin
from importlib import import_module
#修改文件里的中文名字
def marry_c(chinese_string):
    pattern =re.compile(r'[\u4E00-\u9FA5]?.*?[\u4E00-\u9FA5]')
    c=re.findall(pattern,chinese_string)
    return c
def exchange_c_into_e(match_c_s):
    d= lazy_pinyin(match_c_s)
    return d
def ff_open():
    root_path = "scrapyProj.credit"
    """path = s.split("-", 1)[0]
    print(path)
    md = import_module(root_path + "." + path + "." + s)"""
    with open('D:\\spiderheart\\scrapyProj\\credit\\shiyaojian\\shiyaojian-neimengguxingzhengchufa.py','r',encoding='utf-8') as f:
        content = f.readlines()
        print(type(content))
        for line in content:
            c = marry_c(line)
            if (type(c) == list):
                c = ''.join(c)
                e = exchange_c_into_e(c)
                e = ''.join(e)
                print(e)
                with open('D:\\spiderheart\\scrapyProj\\credit\\shiyaojian\\shiyaojian-neimengguxingzhengchufa.py',
                          'w+') as f:
                    content = f.write(e)
                    print(content)




if __name__ == '__main__':
    content = ff_open()
    #print(content)
    #chinese_string='spiderName：食药监-内蒙古行政处罚12222中车'


