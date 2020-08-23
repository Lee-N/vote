from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time


class Vote:
    def __init__(self, name, rank):
        self.name = name
        self.score = 0
        self.rank = rank
        self.url = ""

    def getVote(self):  # 使用接口
        while 1:
            self.url = "https://video.h5.weibo.cn/planet/getData?page_id=1596020167983&namespace=planet&page=1&size=" + str(
                self.rank + 20)
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.url, headers=headers)  # 获取到数据
            json = response.json()
            list = json["data"].get("card_list")[2].get("sub_cards")[2].get("sub_cards")  # 找到列表
            for item in list:
                name = item.get("data").get("title")
                if name == self.name:
                    score = item.get("data").get("score")
                    if score > self.score:
                        print("id:%s" % self.name)
                        print("增加了%d票" % (score - self.score))
                        print("目前票数:%d" % score)
                        self.score = score
            time.sleep(3)

    def getVote2(self):  # 解析页面
        self.url = "https://video.h5.weibo.cn/planet/activepick"
        driver = webdriver.Chrome()
        driver.get(self.url)
        while 1:
            time.sleep(3)  # 等待页面加载
            loadingdom = driver.find_element_by_class_name("loading")
            js = "arguments[0].scrollIntoView(false)"
            page = int(self.rank / 20)  # 一页20个人 计算需要滚动几次 确保找到该人
            for i in range(0, page, 1):
                driver.execute_script(js, loadingdom)
                time.sleep(1)
            list = driver.find_elements_by_class_name("list-title")  # 查找列表
            for item in list:
                name = item.find_element_by_tag_name("h5").text
                if name == self.name:
                    score = int(item.find_element_by_tag_name("span").text)
                    if score > self.score:
                        print("id:%s" % self.name)
                        print("增加了%d票" % (score - self.score))
                        print("目前票数:%d" % score)
                        self.score = score
            driver.refresh()


# vote = Vote("左拆家", 5)  # id和大概的排名
vote = Vote("李子柒", 60)
vote.getVote2()
