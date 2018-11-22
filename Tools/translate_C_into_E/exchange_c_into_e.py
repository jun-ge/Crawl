import os
from pypinyin import lazy_pinyin,pinyin
#修改当前文件夹
def change_c_into_e(dirs):
    for i in dirs:
        old_name = path +'%s'%i

        b = lazy_pinyin(i)
        newname = ''.join(b)

        newname = path+'%s'%newname

        os.rename(old_name,newname)


if __name__ =='__main__':
    path = "./"
    dirs = os.listdir(path)
    change_c_into_e(dirs)
    c=os.getcwd()
