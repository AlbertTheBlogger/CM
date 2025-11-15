from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
import os
import django
from .models import (WeiboPost)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CommentManager.settings')  # 替换为你的项目名称
django.setup()

"""def get_html_by_keyword(keyword):
    # 设置Edge选项
    edge_options = Options()
    edge_options.use_chromium = True
    # 如果需要无头模式（无界面运行）
    # edge_options.add_argument("--headless")
    # 指定Edge WebDriver的路径
    service = Service(executable_path='D:\edgedriver\msedgedriver.exe')
    # 初始化WebDriver
    driver = webdriver.Edge(service=service, options=edge_options)
    # 访问微博页面
    driver.get(f"https://s.weibo.com/weibo?q={keyword}&xsort=hot&Refer=hotmore")
    # 等待页面加载完成
    time.sleep(15)  # 可以根据实际情况调整等待时间
    # 获取页面源代码
    html = driver.page_source
    # 保存到文件
    with open(f'关键词数据.txt', 'w', encoding='utf-8') as file:
        file.write(html)
        print("OK")
    # 关闭浏览器
    driver.quit()"""


def get_html_by_keyword(keyword):
    # 设置Edge选项
    edge_options = Options()
    edge_options.use_chromium = True
    # 如果需要无头模式（无界面运行）
    # edge_options.add_argument("--headless")
    # 指定Edge WebDriver的路径
    service = Service(executable_path='D:\edgedriver\msedgedriver.exe')
    # 初始化WebDriver
    driver = webdriver.Edge(service=service, options=edge_options)
    # 访问微博页面
    driver.get(f"https://s.weibo.com/weibo?q={keyword}&xsort=hot&Refer=hotmore")
    # 等待页面加载完成
    time.sleep(15)  # 可以根据实际情况调整等待时间
    # 获取页面源代码
    html = driver.page_source
    # 关闭浏览器
    driver.quit()
    return html


def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到\n")
    except Exception as e:
        print(f"读取文件时出现错误: {e}\n")


"""def extract_weibo_data(file_path):
    # 存储提取的数据
    data = []
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(content, 'html.parser')
        # 正则表达式匹配微博数据
        pattern = re.compile(r'<div action-type="feed_list_item" mid="(\d+)" class="card-wrap">.*?<a href="//weibo\.com/(\d+)?.*?" target="_blank" nick-name="(.*?)".*?<div class="from"><a href="//weibo\.com/.*?" target="_blank" suda-data=".*?">(.*?)</a>.*?</div>.*?<p node-type="feed_list_content".*?class="txt">(.*?)</p>', re.S)
        # 找到所有匹配的微博数据
        for match in pattern.finditer(content):
            mid = match.group(1)
            user_id = match.group(2)
            username = match.group(3)
            time = match.group(4)
            text = match.group(5).strip()
            data.append((mid, user_id, username, time, text))
        # 将结果保存为txt文件
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for item in data:
                output_file.write(f"Mid: {item[0]}, User ID: {item[1]}, Username: {item[2]}, Time: {item[3]}, Text: {item[4]}\n")
        print("数据提取完成，已保存为", output_path, "文件。")
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查文件路径。\n")
    except Exception as e:
        print(f"提取数据时出现错误: {e}\n")
    columns = ['MId','Uer ID','Username','Time','Text']
    data = pd.DataFrame(data,columns=columns)
    return data"""


def extract_weibo_data(html_content):
    try:
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')
        # 正则表达式匹配微博数据
        pattern = re.compile(
            r'<div action-type="feed_list_item" mid="(\d+)" class="card-wrap">.*?<a href="//weibo\.com/(\d+)?.*?" target="_blank" nick-name="(.*?)".*?<div class="from"><a href="//weibo\.com/.*?" target="_blank" suda-data=".*?">(.*?)</a>.*?</div>.*?<p node-type="feed_list_content".*?class="txt">(.*?)</p>',
            re.S)
        # 找到所有匹配的微博数据
        for match in pattern.finditer(str(soup)):
            mid = match.group(1)
            user_id = match.group(2)
            username = match.group(3)
            time = match.group(4)
            text = match.group(5).strip()

            # 保存到数据库
            WeiboPost.objects.get_or_create(
                mid=mid,
                defaults={
                    'user_id': user_id,
                    'username': username,
                    'time': time,
                    'text': text
                }
            )
        print("数据提取完成，并已保存到数据库。")
    except Exception as e:
        print(f"提取数据时出现错误: {e}")


"""get_html_by_keyword('小米手机')
a = read_txt_file('关键词数据.txt')
print(extract_weibo_data('关键词数据.txt'))"""

if __name__ == '__main__':
    keyword = '小米手机'
    # 获取页面源代码
    html_content = get_html_by_keyword(keyword)
    # 提取数据并保存到数据库
    extract_weibo_data(html_content)
