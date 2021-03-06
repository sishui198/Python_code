__author__ = 'shy'
__date__ = '2018/3/21 16:35'

# 模拟scrapy框架中twisted使用

from twisted.internet import defer
from twisted.web.client import getPage
from twisted.internet import reactor


def download(*args, **kwargs):
    print(args, kwargs)


def stop(*args, **kwargs):
    reactor.stop()


@defer.inlineCallbacks
def task(url):
    v = getPage(url.encode('utf-8'))
    v.addBoth(download)
    yield v


if __name__ == '__main__':
    url_list = [
        "http://www.baidu.com",
        "http://www.bing.com",
    ]
    _active = set()

    for url in url_list:
        d = task(url)
        _active.add(d)

    dd = defer.DeferredList(_active)
    dd.addBoth(stop)
    reactor.run()
