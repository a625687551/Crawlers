# coding:utf-8

import requests
import json
import re
import time
import asyncio

headers = {
    "cookie": "UM_distinctid=16918298cda9f5-076566b03504b6-5701631-1fa400-16918298cdb29b; token=7646ef58f0c29257-3d99ee02f4b2faed; uid=499808; uname=%E6%89%8B%E6%9C%BA%E7%94%A8%E6%88%B7499808; role=3; PHPSESSID=91eliqedlfgan8q8fv0qbi3n6e; ssid=91eliqedlfgan8q8fv0qbi3n6e; CNZZDATA1259748782=2059279747-1550887473-https%253A%252F%252Fwww.baidu.com%252F%7C1550968206",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}


class JulyQuestion(object):
    def __init__(self):
        self.question_ids = []
        self.time_off = 3
        self.file_path = "question.txt"

    def get_question_list(self, url):
        """这个其实可以省略，直接用其中的翻页功能即可"""
        for i in range(1, 9):
            list_info = requests.get(url.format(i), headers=headers).json()
            time.sleep(self.time_off)
            ids = map(lambda x: x["ques_id"], list_info["data"])
            self.question_ids.extend(ids)
        print("get all ids")

    def parse_html(self, url):
        response = requests.get(url, headers=headers).text
        question_info = re.findall('var data = {"quesInfo":(.*?"is_coll":\d+})', response, re.S)
        ques_pos = re.findall('var rate = {"key":(\d+),"count":141}', response, re.S)
        res_json = json.loads(question_info[0])
        images = re.findall("<img  src=\'(.*?)\'/>", res_json["analysis"], re.S)
        return res_json, ques_pos[0], images

    def parse_url_to_html(self, url):
        res_json, qus_ord, image_list = self.parse_html(url)
        title = "{}. {}".format(qus_ord, res_json.get("ques", "what fuck"))
        # 绝对地址换成相对地址
        content = res_json["analysis"]
        content = re.sub("<img  src=.*?aliyuncs.com/Public/Image/Question/|<img  src=.*?aliyuncs.com/",
                         "![](image_file/", content)
        content = re.sub("'/>", ")", content)
        # with open("{}.md".format(title[:50].strip("?| ")), "w", encoding="gb18030") as f:
        #     f.write("{}\n{}".format(title, content))
        with open("面试题集合.md", "a+", encoding="gb18030") as f:
            f.write("{}\n{}\n".format(title, content))
        print("download image list {}".format(len(image_list)))
        self.download_image(image_list)
        print("finish {}".format(title))
        time.sleep(self.time_off)

    def download_image(self, image_list):
        """下载图片，改成异步操作"""
        for url in image_list:
            name = url.split("/")[-1]
            response = requests.get(url, headers=headers).content
            with open("image_file/{}".format(name), "wb") as f:
                f.write(response)

    def run(self):
        list_url = "https://api.julyedu.com/ques/qa?kp_id=23&page={}"
        info_url = "https://www.julyedu.com/question/big/kp_id/23/ques_id/{}"
        print("get list")
        self.get_question_list(list_url)
        print("question ids {}".format(len(self.question_ids)))
        if len(self.question_ids) < 141:
            print("bad nums")
            raise Exception
        # self.question_ids = ["919", "1004", "1056"]
        for i in self.question_ids:
            print("parse {}".format(i))
            self.parse_url_to_html(info_url.format(i))


if __name__ == '__main__':
    july_qus = JulyQuestion()
    july_qus.run()
