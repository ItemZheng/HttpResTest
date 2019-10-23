# coding=utf-8
import tools
import json
import time
import codecs
from tqdm import *

# 原网页
origin_page = "https://www.xiaomiyoupin.com/detail?gid=106648"

# 请求参数
ip = "https://www.xiaomiyoupin.com/api/comment/client/product/v1/content"
request_body = {
    "pindex": 1,
    "psize": 10,
    "gid": 106648,
    "tag_name": u"全部",
    "tag_id": 0
}
request_headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": "application/json"
}

# 输出文档，文档名称 YX_itemID
f = codecs.open('output/YP_%s.txt' % (request_body["gid"]), 'w', encoding="utf-8")
f.write("Product Page: %s" % origin_page)
f.write("\n\n\n")

# 每次爬取10条，共960 条
comment_count = 0
for page in tqdm(range(0, 96)):
    # 当前爬取第 page 页
    request_body["pindex"] = page + 1
    json_info = json.dumps(request_body)

    # 获取响应信息
    res = tools.plugin_homepage(ip, 10, None, request_headers, request_body=json_info)
    if res['code'] != 200:
        print 'Http Error'
        exit(0)

    # json处理
    data = json.loads(res['rsp_body'])

    # 获取comments
    comments = data["data"]
    for i in range(len(comments)):  # 循环遍历所有comments
        comment = comments[i]  # 单条comment
        comment_count = comment_count + 1
        f.write(comment['txt'])
        f.write('\n')

    # 防止 ip 被封，睡眠一秒模拟用户点击
    time.sleep(2)

f.write('\n\nTotal %s comments\n' % str(comment_count))
