#coding=utf8
# windows环境oss下载程序
from __future__ import print_function
import oss2
import sys,os

def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

def download(filename):
    auth = oss2.Auth('您的AccessKeyId', '您的AccessKeySecret')
    bucket = oss2.Bucket(auth, '您的Endpoint', '您的Bucket名')
    bucket.get_object_to_file(filename,filename, progress_callback=percentage)
        
def start(filename):
        curdir_list = os.listdir('.')
        filename = filename.decode('utf8').encode('gbk')
        print('start downloading [%s]......'%filename)
        if filename in curdir_list:
            raise Exception,'%s already in the current directory,can\'t download.'%filename
        else:
            download(filename.decode('gbk').encode('utf8'))
            print('Download success.')

if __name__=='__main__':
    # 获取下载列表
    if len(sys.argv)==1:
        files = raw_input('Please input download filename : ')
        files = files.strip().decode('gbk').encode('utf8').split()
    elif len(sys.argv)>=2:
        files = sys.argv[1:]
        files = map(lambda x:x.decode('gbk').encode('utf8'),files)
        
    # 开始下载
    for i,filename in enumerate(files):
        print ("[%d]"%(i+1),end=' ')
        try:
            start(filename)
        except Exception,e:
            print('Download failed.')
            print('[ERROR]:%s'%e)
            # 删除多余创建的文件
            if str(e).find('already')==-1 and os.path.exists(filename):
              os.remove(filename)
    # 下载完成
    os.system('pause')
        
    
