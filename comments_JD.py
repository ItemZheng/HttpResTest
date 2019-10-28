# coding=utf-8
import tools
import json
import time
import codecs
from tqdm import *

# 原网页
origin_page = "https://item.jd.com/3604840.html"

# 请求参数
ip = "https://sclub.jd.com/comment/productPageComments.action"
query_args = {
    "callback": "fetchJSON_comment98vv2645",
    "productId": "3604840",
    "score": "0",
    "sortType": "5",
    "page": "0",
    "pageSize": "10",
    "isShadowSku": "0",
    "rid": 0,
    "fold": 0
}
request_headers = {
    "Referer": "https://item.jd.com/3604840.html",
    "Sec-Fetch-Mode": "no-cors",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}

# 输出文档，文档名称 JD_productID
f = codecs.open('output/JD_%s.txt' % (query_args["productId"]), 'w', encoding="utf-8")
f.write("Product Page: %s" % origin_page)
f.write("\n\n\n")

# 每次爬取10条，共10000 条
# 该商品只有1000条有效评论
comment_count = 0
for page in tqdm(range(0, 4300)):
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
    try:
        comments = data["comments"]
    except:
        break
    for i in range(len(comments)):  # 循环遍历所有comments
        comment = comments[i]  # 单条comment
        # f.write("### Comment %s ###\n" % (str(comment_count)))
        comment_count = comment_count + 1
        f.write(comment['content'])
        f.write('\n')

        # 爬取追评
        if "afterUserComment" in comment.keys():
            afterUserComment = comment["afterUserComment"]
            if "content" in afterUserComment.keys():
                # f.write("### Comment %s ###\n" % (str(comment_count)))
                comment_count = comment_count + 1
                f.write(afterUserComment["content"])
                f.write('\n')

    # 防止 ip 被封，睡眠一秒模拟用户点击
    time.sleep(2)

f.write('\n\nTotal %s comments\n' % str(comment_count))
