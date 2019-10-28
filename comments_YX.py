# coding=utf-8
import tools
import json
import time
import codecs
from tqdm import *

# 原网页
origin_page = "http://you.163.com/item/detail?id=1497001&_stat_area=1&_stat_referer=search&_stat_query=%E6%99%BA%E8%83%BD%E9%A9%AC%E6%A1%B6%E7%9B%96&_stat_count=4&_stat_searchversion=0.8"

# 请求参数
ip = "http://you.163.com/xhr/comment/listByItemByTag.json"
query_args = {
    "__timestamp": "1571542566443",
    "itemId": "1497001",
    "tag": "%E5%85%A8%E9%83%A8",
    "size": "20",
    "page": "2",
    "orderBy": "0",
    "oldItemTag": "%E5%85%A8%E9%83%A8",
    "oldItemOrderBy": "0",
    "tagChanged": "0",
}
request_headers = {
    "Host": "you.163.com",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Referer": "http://you.163.com/item/detail?id=1497001&_stat_area=1&_stat_referer=search&_stat_query=%E6%99%BA%E8%83%BD%E9%A9%AC%E6%A1%B6%E7%9B%96&_stat_count=4&_stat_searchversion=76",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cookie": " _ntes_nnid=a5f8709a85801deb763b729ea38a2aa7,1570114561386; ne_analysis_trace_id=1570114561390; s_n_f_l_n3=dd25ba847f5c88281570114561393; _ntes_nuid=a5f8709a85801deb763b729ea38a2aa7; _antanalysis_s_id=1570114561783; vinfo_n_f_l_n3=dd25ba847f5c8828.1.0.1570114561392.0.1570114592377; yx_from=search_pz_baidu_29; yx_aui=4c1c3242-3da0-488a-9941-de39b474514f; mail_psc_fingerprint=8da3405b5f50bae7ef26d8f618eae310; yx_stat_seesionId=4c1c3242-3da0-488a-9941-de39b474514f1571542520149; __f_=1571542520436; yx_s_device=ec1e6d5-08bf-c80e-6ce4-8b1775edc8; yx_s_tid=tid_web_1b72c838fe0b476583d7170a6013b803_20ae983e2_1; yx_show_painted_egg_shell=false; yx_delete_cookie_flag=true; yx_search_history=%5B%22%u667A%u80FD%u9A6C%u6876%u76D6%22%2C%22toto%22%5D; yx_new_user_modal_show=1; yx_page_key_list=http%3A//you.163.com/search%3Fkeyword%3D%25E6%2599%25BA%25E8%2583%25BD%25E9%25A9%25AC%25E6%25A1%25B6%25E7%259B%2596%26timestamp%3D1571542536847%26_stat_search%3DautoComplete%26searchWordSource%3D7%23page%3D1%26sortType%3D0%26descSorted%3Dtrue%26categoryId%3D0%26matchType%3D0%2Chttp%3A//you.163.com/item/detail%3Fid%3D1497001%26_stat_area%3D1%26_stat_referer%3Dsearch%26_stat_query%3D%25E6%2599%25BA%25E8%2583%25BD%25E9%25A9%25AC%25E6%25A1%25B6%25E7%259B%2596%26_stat_count%3D4%26_stat_searchversion%3D76; yx_stat_seqList=v_d7447d6c4a%7Cv_11a8617fe2%3B-1%3Bv_7d8b87a185%3Bc_9d6a819923%3Bv_d7447d6c4a%3B-1; yx_but_id=203d52de02c24f11b5949cd818c1e0bb350a593ac34a25cb_v1_nl; yx_stat_lastSendTime=1571542542043"
}

# 输出文档，文档名称 YX_itemID
f = codecs.open('output/YX_%s.txt' % (query_args["itemId"]), 'w', encoding="utf-8")
f.write("Product Page: %s" % origin_page)
f.write("\n\n\n")

# 每次爬取20条，共10000 条
comment_count = 0
for page in tqdm(range(0, 1340)):
    # 当前爬取第 page 页
    query_args["page"] = str(page + 1)
    query_args["__timestamp"] = str(long(time.time() * 100))

    # 获取响应信息
    res = tools.plugin_homepage(ip, 10, query_args, request_headers)
    if res['code'] != 200:
        print 'Http Error'
        exit(0)

    # json处理
    data = json.loads(res['rsp_body'])

    # 获取comments
    comments = data["data"]["commentList"]
    for i in range(len(comments)):  # 循环遍历所有comments
        comment = comments[i]  # 单条comment
        # f.write("### Comment %s ###\n" % (str(comment_count)))
        comment_count = comment_count + 1
        f.write(comment['content'])
        f.write('\n')

    # 防止 ip 被封，睡眠一秒模拟用户点击
    time.sleep(2)

f.write('\n\nTotal %s comments\n' % str(comment_count))
