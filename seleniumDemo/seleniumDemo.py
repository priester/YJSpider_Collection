from selenium import webdriver
from  bs4 import BeautifulSoup
import time
import  requests
import re
def youjiUrlList():
    #所有的种子url
    urls = {}

    broswer = webdriver.Chrome()
    broswer.get('http://www.mafengwo.cn/yj/11886/')

    soup = BeautifulSoup(str(broswer.page_source),'lxml')

    urlList = soup.find_all('li', attrs={'class': 'post-item clearfix'})

    numSpan = soup.find_all('span',attrs={'class':'count'})[0]
    # 获取总页数哦
    totalPage = numSpan.find_all('span')[0]


    for url in urlList:
        a = url.find_all('a')[0]
        authorSpan = url.find_all('span',attrs={'class':'author'})[0]
        author = authorSpan.find_all('a')[1].text;
        article_url = a['href']
        urls[author] = article_url


    if int(totalPage.text) <=1:
        return urls
    else:
        page_num = int(totalPage.text)
        path = '/html/body/div[2]/div[4]/div/div[4]/div/'
        for i in  range(1,page_num):
            # 模拟翻页动作
            try:

                nexturl = 'http://www.mafengwo.cn/yj/11886/1-0-{page}.html'.format(page=i+1)
                broswer.get(nexturl)
                time.sleep(3)
                soup = BeautifulSoup(str(broswer.page_source), 'lxml')
                urlList = soup.find_all('li', attrs={'class': 'post-item clearfix'})
                for url in urlList:
                    a = url.find_all('a')[0]
                    authorSpan = url.find_all('span', attrs={'class': 'author'})[0]
                    author = authorSpan.find_all('a')[1].text;
                    article_url = a['href']
                    urls[author] = article_url
            except:
                print('所在页' + str(i))

    print(len(urls))
    # broswer.quit()
    return urls




def saveUrls(urls):
    for vaule in urls.values():
        with open('./urls.txt', 'a') as fp:
            fp.write(vaule + '\r\n')


# 1将所有的链接保存起来
# saveUrls(youjiUrlList())













# get_all_content()

#
# broswer = webdriver.Chrome()
# broswer.get('http://www.mafengwo.cn/yj/11886/')





# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

import random,requests,time,re



def get_random_header():

    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    headers={'User-Agent':random.choice(USER_AGENTS),'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",'Accept-Encoding':'gzip','Access-Control-Allow-Origi':'*'}
    return headers

def   scraw_proxies(page_num,scraw_url="http://www.xicidaili.com/nt/"):
    scraw_ip=list()
    available_ip=list()
    for page in range(1,page_num):
        print("抓取第%d页代理IP" %page)
        url=scraw_url+str(page)
        r=requests.get(url,headers=get_random_header())
        r.encoding='utf-8'
        pattern = re.compile('<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)
        scraw_ip= re.findall(pattern, r.text)
        for ip in scraw_ip:
            if(test_ip(ip)==True):
                print('%s:%s通过测试，添加进可用代理列表' %(ip[0],ip[1]))
                available_ip.append(ip)
            else:
                pass
        print("代理爬虫暂停10s")
        time.sleep(10)
        print("爬虫重启")
    print('抓取结束')
    return available_ip

def test_ip(ip,test_url='http://2017.ip138.com/ic.asp',time_out=3):
    proxies={'http': ip[0]+':'+ip[1]}
    try_ip=ip[0]
    #print(try_ip)
    try:
        r=requests.get(test_url,headers=get_random_header(),proxies=proxies,timeout=time_out)
        if r.status_code==200:
            r.encoding='gbk'
            result=re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',r.text)
            result=result.group()
            if result[:9]==try_ip[:9]:
                print(r.text)
                print('测试通过')
                return True
            else:
                print('%s:%s 携带代理失败,使用了本地IP' %(ip[0],ip[1]))
                return False
        else:
            print('%s:%s 请求码不是200' %(ip[0],ip[1]))
            return False
    except:
        print('%s:%s 请求过程错误' %(ip[0],ip[1]))
        return False




# avaiable_ip = scraw_proxies(3)
# print(avaiable_ip)

# [('120.92.21.238', '10000')];

def get_Content(url,line):

    line = line+1
    # proxies = get_random_ip(get_ip_list())
    r = requests.get(url,headers=get_random_header(),)
    soup = BeautifulSoup(r.text,'lxml')
    try:
        # 1.查找游记的文字内容
        content = soup.find_all('div', attrs={'class': 'va_con _j_master_content'})[0].text;
        re.findall(r'\S', content)
        wordList = re.findall(r'\S+', content);
        pureContent = ''.join(wordList)
        print(pureContent)
        print(len(pureContent))
        with open('./success_url.txt','a') as fp:
            fp.write(url + '\r\n')
        #     2.保存到txt
        with open('./hengshan_youji.txt', 'a') as fp:
            fp.write( '%d:' % line + pureContent + '\r\n')
    except Exception as err:
        with open('./fail_url.txt','a') as fp:
            fp.write(url+'\r\n')
            print('保错的url:' +url)
            print(err)


# 2. 抓取所有的游记内容
def get_all_content():

    urls = []

    success_urls = []

    with open('./success_url.txt','r') as fp:
        lines = fp.readlines()
        for line in lines:
            full_url = line.strip()
            success_urls.append(full_url)


    with open('./urls.txt') as fp:
        lines = fp.readlines()
        for line in lines:
            full_url = 'http://www.mafengwo.cn' + line.strip()

            print(full_url)
            if full_url not in success_urls:

                time.sleep(1)
                get_Content(full_url, lines.index(line))

# get_all_content()

get_Content('http://www.mafengwo.cn/i/3282928.html',1200)