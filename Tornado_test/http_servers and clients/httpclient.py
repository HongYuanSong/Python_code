__author__ = 'shy'
__date__ = '2018/3/29 11:30'

# 阻塞的 HTTP 客户端
#
# from tornado import httpclient
#
# http_client = httpclient.HTTPClient()
# try:
#     response = http_client.fetch("http://www.baidu.com/")
#     print(response.headers)
# except httpclient.HTTPError as e:
#     # HTTPError is raised for non-200 responses; the response
#     # can be found in e.response.
#     print("Error: " + str(e))
# except Exception as e:
#     # Other errors are possible, such as IOError.
#     print("Error: " + str(e))
# http_client.close()


# 非阻塞 HTTP 客户端

from tornado import httpclient


def handle_request(response):
    if response.error:
        print("Error:", response.error)
    else:
        print(response.headers)


if __name__ == '__main__':
    http_client = httpclient.AsyncHTTPClient()
    http_client.fetch("http://www.baidu.com/", handle_request)
