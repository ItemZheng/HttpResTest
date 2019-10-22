# coding=utf-8
import tools
import json
import time
import codecs
from tqdm import *

# 天猫
# todo 只能爬取十几个页面就会被封IP
# 原网页
origin_page = "https://detail.tmall.com/item.htm?spm=a230r.1.14.1.28ff5197xnL9Q6&id=533732788971&cm_id=140105335569ed55e27b&abbucket=18"

# 请求参数
ip = "https://rate.tmall.com/list_detail_rate.htm"
query_args = {
    "itemId": "533732788971",
    "sellerId": "697095006",
    "currentPage": "1",
    # "spuId": "901541286",
    # "order": "3",
    # "append": "0",
    # "content": "1",
    # "tagId": "",
    # "posi": "",
    # "picture": "",
    # "groupId": "",
    # "ua": "098%23E1hvI9vRvpWvUpCkvvvvvjiPRszhtjrWPszwtjthPmPWAjYRnLs9tjnCRFMOsjD8R86CvvyvmhO8gRvhuQRrvpvEvvp%2BmKPFCU%2B33QhvCvvhvvm5vpvhvvmv9FyCvvpvvvvvKphv8vvvvUrvpvvvvvmvn6Cvm8IvvUEpphvWh9vv9DCvpvA6vvmmByCv2VoEvpvVmvvC9cavuphvmvvv9b4o6anpmphvLv3jY9vjEixrQjZ7rj6OfaBlMEyfwydI1W2pjE1%2BVd0DyOvOSF6x6fmtSCy4PvAyqU5E%2BdvdhU0HsXZpejXW3E5xKfhT8Z4tIWeQRipCvpvVvvpvvhCv2QhvCvvvvvmrvpvEvv3qm3hBCRrj9phvHnQwx0TUzYswMErr7Y%2F%2FMCLwOHuCRphvCvvvvvv%3D",
    # "needFold": "0",
    # "_ksTS": "1571190862261_821",
    # "callback": "jsonp822"
}
request_headers = {
    "Referer": "https://detail.tmall.com/item.htm?spm=a230r.1.14.1.28ff5197xnL9Q6&id=533732788971&cm_id=140105335569ed55e27b&abbucket=18",
    "Sec-Fetch-Mode": "no-cors",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Cookie": "hng=CN%7Czh-CN%7CCNY%7C156; lid=%E9%98%A1%E9%99%8C%E7%9A%84%E6%97%A0%E8%A7%A3; cna=GYTFFex/czkCAbedoCiLiObS; dnk=%5Cu9621%5Cu964C%5Cu7684%5Cu65E0%5Cu89E3; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=Vq8l%2BKCLjhS4UhJVbhgU&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTbnV%2BPQ33UJg%3D%3D&cart_m=0&tag=8&lng=zh_CN; tracknick=%5Cu9621%5Cu964C%5Cu7684%5Cu65E0%5Cu89E3; lgc=%5Cu9621%5Cu964C%5Cu7684%5Cu65E0%5Cu89E3; t=b4d57979b92db9d9971834758209bc81; csg=e4f6e04f; _tb_token_=fee9330be0153; cq=ccp%3D1; pnm_cku822=098%23E1hvZvvUvbpvUvCkvvvvvjiPRszhtjtVnLzvljD2PmPy0j3bn2qU6jEvRszhsjYRiQhvChCvCCptvpvhphvvvvGCvvpvvPMMvphvCyCCvvvvvvyCvh12DZQvIqUfU16AgbmAdcWKNZAOD46XjLhDN%2BBl5FGDN5WK%2BE7reB69wxJxfBeKfvyf8cc6PqUf8C61D70Xd56OVAileb8rwkY%2B20zUuphvmhCvCbxioJ0vkphvCyEmmvAfeqyCvm3vpvm9MMYvdyCvH2UvvhbIphvZ99vvpGavpComvvC2fyCvH2Uvvhn4; l=dBreC0Jcqc8DTp2QBOCwlurza77tJIRfguPzaNbMi_5Ir1fZubbOkgoQrev6cjWci9LB4GDEhoeTrUZ88Pg6R2Ko99cdvd3HCef..; isg=BM7Okm0xH59featmCySRy2UuH6KQT5JJcqa4YvgXAlH4W2-1YNvqWPaRk8eSw4ph"
}

# 输出文档，文档名称 TM_productID.txt
f = codecs.open('TM_%s.txt' % (query_args["itemId"]), 'w', encoding="utf-8")
f.write("Product Page: %s" % origin_page)
f.write("\n\n\n")

# 每次爬取20条，共8800条
comment_count = 0
for page in tqdm(range(0, 84)):
    # 当前爬取第 page 页
    query_args["currentPage"] = str(page + 1)

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
    comments = data["rateDetail"]["rateList"]
    for i in range(len(comments)):  # 循环遍历所有comments
        comment = comments[i]  # 单条comment
        if comment['rateContent'] != u"此用户没有填写评论!":
            # f.write("### Comment %s ###\n" % (str(comment_count)))
            comment_count = comment_count + 1
            f.write(comment['rateContent'])
            f.write('\n')

        appendComment = comment["appendComment"]
        if appendComment is not None:
            # f.write("### Comment %s ###\n" % (str(comment_count)))
            comment_count = comment_count + 1
            f.write(appendComment['content'])
            f.write('\n')

    # 防止 ip 被封，睡眠一秒模拟用户点击
    time.sleep(3)

f.write('\n\nTotal %s comments\n' % str(comment_count))
