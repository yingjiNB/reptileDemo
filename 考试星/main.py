# -- coding: utf-8 --
import requests
from lxml import etree
import csv
url = 'https://exam.kaoshixing.com/exam/exam_check?examInfoId=1479608&examResultsId=90932504'
headers = {

    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "cookie": "laat=41676bc7-c159-47cd-b661-e0063072e3fc; sessionId=aaa1wgOuAIy62hFdjDLPy; KSX_CID=339516; JSESSIONID=aaa7RFirVyHa6-vdgYVPy",
    "pragma": "no-cache",
    "referer": "https://exam.kaoshixing.com/exam/result/inquire?examResultsId=90925827&type=1",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

}
res = requests.get(url=url, headers=headers,verify=False).text
html = etree.HTML(res)
questions = html.xpath("//span[@class='question-name']/span/text()")
option_letter = html.xpath("//div[@class='answers']//span[@class='words']/span[@class='words-option']/text()")
option = html.xpath("//div[@class='answers']//span[@class='words']/text()")
answers  = html.xpath("//div[3]/div[5]/div[2]/text()")

merged_list = [option_letter[i] + option[i] for i in range(min(len(option_letter), len(option)))]

options = []

# 遍历列表，每4个元素一组
for i in range(0, len(merged_list), 4):
    combined_string = ''.join(merged_list[i:i+4])
    options.append(combined_string)

print(questions)
print(options)
print(answers )
with open('quiz_questions.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 写入表头
    writer.writerow(['题目', '选项', '答案'])

    # 写入题目、选项和答案
    for i in range(len(questions)):
        print(options[i])
        writer.writerow([questions[i], options[i], answers[i]])