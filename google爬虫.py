from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
import urllib.request
import os, sys
import lxml
import re
import os


curr_time = datetime.datetime.now()
month = curr_time.month
day = curr_time.day

def google_kw(keyword):
    text = ''
    option = webdriver.ChromeOptions()
    chrome_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    driver = webdriver.Chrome(executable_path=chrome_driver)
    action = ActionChains(driver)
    driver.get("http://www.google.com/")
    time.sleep(2)

    input = driver.find_elements_by_xpath('''//input[@class="gLFyf gsfi"]''')[0]
    input.send_keys(keyword)
    input.send_keys(Keys.ENTER)  # 按下enter键
    time.sleep(2)

    pagelist = [2,3,4,5,6,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,]
    # pagelist = [2,3]
    linkIDList = []
    for page in pagelist:
        try:
            print(page)
            pageXPath = '''//*[@id="xjs"]/div/table/tbody/tr/td[{}]/a'''.format(page)
            b = driver.find_element_by_xpath(pageXPath)
            b.click()
            time.sleep(5)
        except Exception as e:
            # print(e)
            print("找不到页面")
        try:
            xpath = '''//*[@id="rso"]/div/div/div[1]/a'''
            for link in driver.find_elements_by_xpath(xpath):
                linkID = link.get_attribute('href')
                if linkID in linkIDList:
                    continue
                else:
                    linkIDList.append(linkID)
                if '.pdf' in linkID or 'cgi' in linkID:
                    print('下载pdf：',str(linkID))
                    download_pdf(linkID,keyword)
                    continue
                elif '.pdf' not in linkID:
                    print(linkID)
                    text = text + str(filterHtmlTag(str(goto_url(linkID))))

            # a = driver.find_element_by_xpath(xpath)
            # action.key_down(Keys.CONTROL).perform()
            # a.click()
            # action.key_up(Keys.CONTROL).perform()
            #
            # windows = driver.window_handles
            # driver.switch_to.window(windows[-1])
            #
            # html_source = driver.page_source
            # text = text + str(filterHtmlTag(html_source))
            #
            # time.sleep(10)
            #
            # driver.close()
            # driver.switch_to.window(windows[0])

        except Exception as e:
            pass
            print(e)
            # print("找不到链接")
    return text

def goto_url(url):
    content = ''
    try:
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        # 构造访问请求
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req, timeout=5)
        content = res.read()
        print('完成')
    except Exception as e:
        print('访问失败')
        # print("找不到链接")
    return content

def download_pdf(url_pdf,kw):
    content = ''
    pdf_name = str(url_pdf).split('/')[-1]
    dir_name = "D:\studyVV\Google\drone\{}".format(kw)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)  # 创建目录或文件夹
    if '.pdf' in pdf_name:
        pdf_path = 'D:\studyVV\Google\drone\{}\{}'.format(kw,pdf_name)
    else:
        pdf_path = 'D:\studyVV\Google\drone\{}\{}.pdf'.format(kw,pdf_name)
    try:
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        # 构造访问请求
        req = urllib.request.Request(url_pdf, headers=headers)
        res = urllib.request.urlopen(req, timeout=10)
        content = res.read()
        with open(pdf_path, 'wb') as f:
            f.write(content)
            f.close()
        print('下载完成')
    except Exception as e:
        print('pdf下载失败')
        # print("找不到链接")
    return content


def save_page_txt(content):
    # 重点
    html = lxml.html.fromstring(content)
    # 获取标签下所有文本
    items = html.xpath("//div[@id='y_prodsingle']//text()")
    # 正则 匹配以下内容 \s+ 首空格 \s+$ 尾空格 \n 换行
    pattern = re.compile("^\s+|\s+$|\n")

    clause_text = ""
    for item in items:
        # 将匹配到的内容用空替换，即去除匹配的内容，只留下文本
        line = re.sub(pattern, "", item)
        if len(line) > 0:
            clause_text += line + "\n"
    print(clause_text)


def filterHtmlTag(htmlstr):
    '''
    过滤html中的标签
    '''
    # 兼容换行
    s = htmlstr.replace('\r\n', '\n')
    s = htmlstr.replace('\r', '\n')

    # 规则
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[\S\s]*?<\s*/\s*script\s*>', re.I)  # script
    re_style = re.compile('<\s*style[^>]*>[\S\s]*?<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\\s*?\/??>', re.I)  # br标签换行
    re_p = re.compile('<\/p>', re.I)  # p标签换行
    re_h = re.compile('<[\!|/]?\w+[^>]*>', re.I)  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    re_hendstr = re.compile('^\s*|\s*$')  # 头尾空白字符
    re_lineblank = re.compile('[\t\f\v]*')  # 空白字符
    re_linenum = re.compile('\n+')  # 连续换行保留1个

    # 处理
    s = re_cdata.sub('', s)  # 去CDATA
    s = re_script.sub('', s)  # 去script
    s = re_style.sub('', s)  # 去style
    s = re_br.sub('\n', s)  # br标签换行
    s = re_p.sub('\n', s)  # p标签换行
    s = re_h.sub('', s)  # 去HTML标签
    s = re_comment.sub('', s)  # 去HTML注释
    s = re_lineblank.sub('', s)  # 去空白字符
    s = re_linenum.sub('\n', s)  # 连续换行保留1个
    s = re_hendstr.sub('', s)  # 去头尾空白字符

    # 替换实体
    s = replaceCharEntity(s)

    return s


def replaceCharEntity(htmlStr):
    '''
      替换html中常用的字符实体
      使用正常的字符替换html中特殊的字符实体
      可以添加新的字符实体到CHAR_ENTITIES 中
      CHAR_ENTITIES是一个字典前面是特殊字符实体  后面是其对应的正常字符
      :param htmlStr:
      '''
    htmlStr = htmlStr
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }
    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlStr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后的字符如（" "--->key = "nbsp"）    去除&;后entity,如>为gt
        try:
            htmlStr = re_charEntity.sub(CHAR_ENTITIES[key], htmlStr, 1)
            sz = re_charEntity.search(htmlStr)
        except KeyError:
            # 以空串代替
            htmlStr = re_charEntity.sub('', htmlStr, 1)
            sz = re_charEntity.search(htmlStr)
    return htmlStr


if __name__ == '__main__':
    keywords = ['drone hardware components','uav hardware components','Unmanned Aerial Vehicle hardware components', 'drone components', 'uav components', 'Unmanned Aerial Vehicle components']
    path = 'd:\\谷歌爬虫'
    for keyword in keywords:
        text = google_kw(keyword)
        textPath = 'D:\studyVV\Google\drone\{}.txt'.format(keyword)
        f2 = open(textPath, 'w',encoding='utf-8')
        f2.write(text)
        f2.close()

