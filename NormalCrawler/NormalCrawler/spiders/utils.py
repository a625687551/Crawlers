# -*- coding: utf8 -*-
import logging
import time
import re
import datetime
import socket
import struct
import platform

import dateformatting

logger = logging.getLogger(__name__)
days = 3


def is_time_out(time_str, days=days):
    if not time_str:
        return True
    st = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    delta = time.time() - time.mktime(st)
    return delta >= days * 24 * 3600


def parse_re(content, pattern, num=None):
    if num is None:
        num = 0
    rets = re.findall(pattern, content)
    lr = len(rets)
    if lr > 0:
        if num >= lr:
            logger.error('Re Num Error! Total length {0}, num {1}'.format(lr, num))
            return ''
        return rets[num]
    logger.info(u'Not find {0}'.format(pattern))
    return ''


def parse_xpath(content, xpath_str, num=None, join_str=''):
    if num is None:
        num = 0
    rets = content.xpath(xpath_str)
    lr = len(rets)
    if lr > 0:
        if num == 'all':
            return join_str.join([i.strip() for i in rets]) + join_str
        if num >= lr:
            logger.error('Xpath Num Error! Total length {0}, num {1}'.format(lr, num))
            return ''
        return rets[num]
    logger.info(u'Not find {0}'.format(xpath_str))
    return ''


def stand_time(time_str):
    logger.debug('time_str: %s', time_str)
    post_time = dateformatting.parse(time_str)
    if post_time is None:
        post_time = '2000-1-1 00:00:00'
    else:
        post_time = post_time.strftime('%Y-%m-%d %H:%M:%S')
    return post_time


def get_ip_str():
    if platform.system() == 'Windows':
        myname = socket.gethostname()
        myaddr = socket.gethostbyname(myname)
        myaddr = '192.168.1.40'
    else:
        import fcntl
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'enp8s0'))
        except:
            try:
                inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth1'))
            except:
                inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'enp4s0f1'))
        myaddr = socket.inet_ntoa(inet[20:24])
    ip_last = int(myaddr.split('.')[-1])
    return ip_last
