# coding=utf8

import urllib2
import chardet
import traceback
import StringIO
import re
import gzip


def plugin_homepage(ip, timeout, query_args, request_headers):
    url = "%s?" % ip
    for k in query_args:
        url = url + str(k) + '=' + str(query_args[k]) + '&'
    url = url[0: -1]

    is_timeout, error_reason, code, header, body, title = get_html(url, timeout, request_headers)
    res = {"ip": ip,
           "rsp_header": header,
           "rsp_body": body,
           "code": code,
           "title": title,
           "is_timeout": is_timeout,
           "error_reason": error_reason}
    return res


def get_html(url, timeout, request_headers):
    headers = request_headers
    is_timeout = False
    error_reason = None
    code = None
    header = None
    body = None
    title = None
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request, timeout=timeout)
        code = response.getcode()
        body = response.read()
        header = str(response.headers)
    except urllib2.HTTPError, e:  # 处理http错误
        print "str(e):%s\nrepr(e):%s\ne:%s\ne.read():%s\n" % (str(e), repr(e), e, e.read())
        error_reason = str(e)
        body = e.read()
        header = e.headers
    except urllib2.URLError, e:
        print traceback.print_exc()
        error_reason = str(e.reason)
        if error_reason == "timed out":  # 判断是否超时
            is_timeout = True
        return is_timeout, error_reason, code, header, body, title
    except Exception, e:
        print traceback.print_exc()
        error_reason = str(e)
        return is_timeout, error_reason, code, header, body, title
    if not header:
        return is_timeout, error_reason, code, header, body, title
    # 解压gzip
    if 'Content-Encoding' in header and 'gzip' in header['Content-Encoding']:
        html_data = StringIO.StringIO(body)
        gz = gzip.GzipFile(fileobj=html_data)
        body = gz.read()
    # 编码转换
    try:
        html_encode = get_encode(header, body).strip()
        if html_encode and len(html_encode) < 12:
            body = body.decode(html_encode).encode('utf-8')
    except:
        pass
    # 获取title
    try:
        title = re.search(r'<title>(.*?)</title>', body, flags=re.I | re.M)
        if title:
            title = title.group(1)
    except:
        pass
    return is_timeout, error_reason, code, str(header), body, title


# 获取html编码
def get_encode(header, body):
    try:
        m = re.search(r'<meta.*?charset=(.*?)"(>| |/)', body, flags=re.I)
        if m:
            return m.group(1).replace('"', '')
    except:
        pass
    try:
        if 'Content-Type' in header:
            Content_Type = header['Content-Type']
            m = re.search(r'.*?charset=(.*?)(;|$)', Content_Type, flags=re.I)
            if m:
                return m.group(1)
    except:
        pass
    chardit1 = chardet.detect(body)
    encode_method = chardit1['encoding']
    return encode_method
