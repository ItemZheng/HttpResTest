# coding=utf-8
import tools
import json
import time
import codecs
from tqdm import *

# 原网页
origin_page = "https://item.jd.com/100005294816.html#comment"

# 请求参数
ip = "https://sclub.jd.com/comment/productPageComments.action"
query_args = {
    "callback": "fetchJSON_comment98vv31",
    "productId": "100005294816",
    "score": "0",
    "sortType": "5",
    "page": "0",
    "pageSize": "10",
    "isShadowSku": "0",
    "rid": 0,
    "fold": 0
}
request_headers = {
    "Referer": "https://item.jd.com/100005294816.html",
    "Sec-Fetch-Mode": "no-cors",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}

# 输出文档，文档名称 JD_productID
f = codecs.open('JD_%s.txt' % (query_args["productId"]), 'w', encoding="utf-8")
f.write("Product Page: %s" % origin_page)
f.write("\n\n\n")

# 每次爬取10条，共10000 条
comment_count = 0
for page in tqdm(range(0, 1200)):
    # 当前爬取第 page 页
    query_args["page"] = str(page)

    # 获取响应信息
    res = tools.plugin_homepage(ip, 10, query_args, request_headers)
    if res['code'] != 200:
        print 'Http Error'
        exit(0)

    # 移除首尾无用字符
    content = res['rsp_body']
    begin = content.find("(")
    end = content.rfind(")")
    content = content[begin + 1:end]

    # json处理
    data = json.loads(content)

    # 获取comments
    comments = data["comments"]
    for i in range(len(comments)):  # 循环遍历所有comments
        comment = comments[i]  # 单条comment
        f.write("### Comment %s ###\n" % (str(comment_count)))
        comment_count = comment_count + 1
        f.write(comment['content'])
        f.write('\n\n\n')

    # 防止 ip 被封，睡眠一秒模拟用户点击
    time.sleep(1)
