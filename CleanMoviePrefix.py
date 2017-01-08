# coding=gbk
import os
import re
import string

def isMov(filename):
    # �ж��Ƿ�Ϊ��Ӱ�ļ�
    suffix = filename.split('.')[-1].lower()      # ��ȡ��׺
    pattern = re.compile(r'mpg|mpeg|m2v|mkv|dat|vob|avi|wmv|rm|ram|rmvb|mov|avi|mp4|qt|viv')
    if pattern.search(suffix):  # ƥ���Ƿ�Ϊ��Ӱ��ʽ
        return True
    else:
        return False

if __name__=='__main__':
    #  ������ǰĿ¼
    print '�����С���'
    cnt = 1
    for fp in os.listdir(os.getcwd()):
        if os.path.isfile(fp) and isMov(fp):  # �ǵ�Ӱ�ļ�
            if fp[0]=='[':      # ȥ����ͷ��[]
                index = fp.find(']')
                if index!=-1:
                    print '[%d] %s ==> %s'%(cnt,fp,fp[index+1:])
                    os.rename(fp,fp[index+1:])
                    fp = fp[index+1:]
                    cnt+=1
                    
            elif fp[:2]=='��':   # ȥ����ͷ�ġ���
                index = fp.find('��')
                if index!=-1:
                    print '[%d] %s ==> %s'%(cnt,fp,fp[index+2:])
                    os.rename(fp,fp[index+2:])
                    fp = fp[index+2:]
                    cnt+=1
                    
            if fp[0] =='.' or fp[0]=='-':     # ȥ����ͷ��'.' �� '-'
                print '[%d] %s ==> %s'%(cnt,fp,fp[1:])
                os.rename(fp,fp[1:])
                
    if cnt==1:
        print 'û����Ҫ����ĵ�Ӱ�ļ�'
    else:
        print '�������'
