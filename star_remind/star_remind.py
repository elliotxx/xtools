#coding=utf8
import re
import os,sys
import socket
import urllib,urllib2,cookielib
import smtplib
from email.mime.text import MIMEText
from email.header import Header

timeout = 30                             # 超时时间
charset = 'utf-8'		# 请求页面的编码格式
subject = '【更新提示】'	# email 中的主题
content = ''			# email 中的内容
isRenew = False			# 是否有更新
record_file = os.path.join(sys.path[0],'record.dat')      # 记录文件
conf_file = os.path.join(sys.path[0],'conf.ini')                # 配置文件
renew_dict = {}                 # 更新记录
my_email = ''                      # 邮箱地址
my_password = ''                   # 邮箱授权码
github_username = ''            # github 用户名
github_password = ''            # github 密码


def send_email(sub,cont):
    # send email
    global my_email,my_password
    sender = my_email                   # 发送方
    receiver = [my_email]               # 收件方
    subject = sub                       # 邮件主题
    smtpserver = 'smtp.qq.com'          # 邮箱服务器
    username = my_email                 # 用户名
    password = my_password		# 授权码

    msg = MIMEText(cont, 'html', 'utf8')	# 设置内容
    msg['Subject'] = Header(subject, 'utf8')	# 设置主题
    msg['From'] = sender			# 设置发送方
    msg['To'] = ','.join(receiver)		# 设置接收方
    smtp = smtplib.SMTP_SSL(smtpserver,465)
    #smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

def Init():
    global renew_dict,my_email,my_password,timeout,github_username,github_password
    # 设置超时时间
    socket.setdefaulttimeout(timeout)
    print '正在加载邮箱地址和授权码……'
    try:
        fp = open(conf_file,'r')
    except Exception,e:
        print '加载失败，conf.ini文件不存在'
        raise Exception,e
    lines = fp.readlines()
    my_email = lines[1].strip()     # 加载邮箱地址
    my_password = lines[3].strip()  # 加载邮箱授权码
    if len(lines)>4:
        github_username = lines[5].strip()   # 加载github用户名
        github_password = lines[7].strip()   # 加载github密码
    fp.close()

    print '正在加载更新记录……'
    # 提取更新情况记录
    try:
        fp = open(record_file,'r')
    except:
        open(record_file,'w')
        fp = open(record_file,'r')
    for line in fp:
        items = line.split(':#:')
        key = items[0].strip()
        value = items[1].strip()
        renew_dict[key] = value

    fp.close()


def RenewCheck(key,src_url,des_url,pattern_str,charset):
    # 检查更新
    global subject,content,isRenew,renew_dict,github_username,github_password
    host = 'http://'+src_url.split('//')[1].split('/')[0]   # 检查网站的host地址

    # 其它全局变量
    host = 'http://github.com'
    login_url = 'https://github.com/login'
    post_url = 'https://github.com/session'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    username = github_username
    password = github_password

    # 构建opener
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

    request = urllib2.Request(login_url,headers=headers)
    response = opener.open(request)
    # 获取token
    print '正在获取token……'
    token_pattern = re.compile('<input name="authenticity_token" type="hidden" value="(.*?)"',re.S)
    token = re.findall(token_pattern,response.read().decode('utf8'))[0]
    #print token

    # 构造post数据
    postdata = urllib.urlencode({
        'commit':'Sign in',
        'utf8':'%E2%9C%93',
        'authenticity_token':token,
        'login':username,
        'password':password
        })

    # 验证登陆
    print '正在登录github……'
    request = urllib2.Request(post_url,postdata,headers)
    response = opener.open(request)
    #print response.read()

    # 访问用户主页面
    print '正在访问用户主页……'
    request = urllib2.Request(host,headers=headers)
    response = opener.open(request)
    html = response.read().decode('utf8')

    # 匹配star
    print '正在匹配star信息……'
    pattern = re.compile(r'<div class="alert watch_started simple">.*?<a.*?>(.*?)</a> starred <a href="/(.*?)/(.*?)"',re.S)
    items = re.findall(pattern,html)

    # 找到最近的star
    isF = False
    for item in items:
        if item[1]==github_username:
            isF = True
            items = item
            break
    if not isF:
        print '最近没有人star你的项目'
        return

    # 清洗数据
    items = map(lambda x:x.strip(),items)

    # 输出解析结果
    star_user = items[0].encode('utf8')
    repo_name = items[2].encode('utf8')
    title = ' '.join(items)
    #print title

    # 判断是否有更新
    cur = title.encode('utf8')
    if renew_dict.has_key(key): # 判断之前有无记录
        last = renew_dict[key]
    else:
        last = None
    if cur != last or last==None:
        # 如果有更新，发送邮件提示
        isRenew = True

        # 更新记录
        renew_dict[key] = cur
        fp = open(record_file,'w')
        for item,value in renew_dict.items():
            fp.write('%s:#:%s\n'%(item,value))
        fp.close()

        print 'github上有新的star，发送邮件……'
        subject += '%s '%(key)
        content += 'Github上 <strong>%s</strong> 刚刚star了你的项目 <strong>%s</strong> ，戳这里去看看：%s<br/>'%(star_user,repo_name,des_url)
    else:
        # 没有更新
        print '最近没有人star你的项目'


def main():
    global subject,content,isRenew
    isRenew = False

    # 提取更新情况记录
    Init()

    # 登录github
    RenewCheck('github star',\
            'https://github.com/',\
            'https://github.com/',\
            r'<div class="alert watch_started simple">.*?<a.*?>(.*?)</a> starred <a href="/(.*?)/(.*?)"',\
            'utf8'\
            )   # github star


    if isRenew:
        send_email(subject+'有更新！',content)


if __name__ == '__main__':
    try:
        main()
    except Exception,e:
        print '[ERROR]:%s'%e

