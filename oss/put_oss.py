#!/usr/bin/python
#coding=utf8
# linux环境oss上传程序
from __future__ import print_function
import oss2
import sys,os

def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

def upload(filename,filedata):
    auth = oss2.Auth('您的AccessKeyId', '您的AccessKeySecret')
    bucket = oss2.Bucket(auth, '您的Endpoint', '您的Bucket名')
    bucket.put_object(filename, filedata, progress_callback=percentage)


def start(filename):
    curdir_list = os.listdir('.')
    filename = filename
    print('\033[1;36;40m',end='')
    print('start uploading [%s]......'%filename)
    print('\033[0m',end='')
    if filename in curdir_list:
        # 上传文件在当前目录下
        fp = open(filename,'r')
        data = fp.read()
        fp.close()
	upload(filename,data)
        print('\033[0;32;40m',end='')
	print('Upload success.')
        print('\033[0m',end='')
    else:
        raise Exception,'%s is not in the current directory,can\'t upload.'%filename

if __name__=='__main__':
    # 获取下载列表
    if len(sys.argv)==1:
        files = raw_input('Please input upload filename : ')
        files = files.strip().split()
    elif len(sys.argv)>=2:
        files = sys.argv[1:]

    # 开始下载
    for i,filename in enumerate(files):
        print('\033[1;36;40m',end='')
        print ("[%d]"%(i+1),end=' ')
        print('\033[0m',end='')
        try:
            start(filename)
        except Exception,e:
            print('\033[0;31;40m',end='')
            print('Upload failed.')
            print('[ERROR]:%s'%e)
            print('\033[0m',end='')

