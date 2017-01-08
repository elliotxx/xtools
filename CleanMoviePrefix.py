# coding=gbk
import os
import re
import string

def isMov(filename):
    # 判断是否为电影文件
    suffix = filename.split('.')[-1].lower()      # 提取后缀
    pattern = re.compile(r'mpg|mpeg|m2v|mkv|dat|vob|avi|wmv|rm|ram|rmvb|mov|avi|mp4|qt|viv')
    if pattern.search(suffix):  # 匹配是否为电影格式
        return True
    else:
        return False

if __name__=='__main__':
    #  遍历当前目录
    print '处理中……'
    cnt = 1
    for fp in os.listdir(os.getcwd()):
        if os.path.isfile(fp) and isMov(fp):  # 是电影文件
            if fp[0]=='[':      # 去掉开头的[]
                index = fp.find(']')
                if index!=-1:
                    print '[%d] %s ==> %s'%(cnt,fp,fp[index+1:])
                    os.rename(fp,fp[index+1:])
                    fp = fp[index+1:]
                    cnt+=1
                    
            elif fp[:2]=='【':   # 去掉开头的【】
                index = fp.find('】')
                if index!=-1:
                    print '[%d] %s ==> %s'%(cnt,fp,fp[index+2:])
                    os.rename(fp,fp[index+2:])
                    fp = fp[index+2:]
                    cnt+=1
                    
            if fp[0] =='.' or fp[0]=='-':     # 去掉开头的'.' 或 '-'
                print '[%d] %s ==> %s'%(cnt,fp,fp[1:])
                os.rename(fp,fp[1:])
                
    if cnt==1:
        print '没有需要处理的电影文件'
    else:
        print '处理完毕'
