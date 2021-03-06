#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "mengdj@outlook.com"
import os
import time
import csv
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from io import StringIO
from lxml import etree
"""
西祠代理IP
"""
class Proxy(object):
    def __init__(self, site='httpbin.org/ip', start=1, stop=2):
        """
        初始化
        :param site:        网站
        :param start:       起步页1
        :param stop:        终止页2
        """
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self._xici_url_list = ('https://www.xicidaili.com' + t + (str(p) if p > 1 else '') for t in('/nn/', '/nt/', '/wn/', '/wt/') for p in range(start, stop))
        self._xici_target_list = []
        self._proxy_site = site
        self._file = 'proxy.csv'
        if self._validate_data() is False:
            raise Exception('can\'t found proxy source data')

    def each(self, num=1, protocol='HTTPS', timeout=1):
        """
        迭代器获取代理
        :param num:         返回数目
        :param protocol:    应用协议HTTPS/HTTP
        :param timeout:     超时
        :return:
        """
        prev_index = -1
        while num:
            ret = self.find(1, protocol=protocol, timeout=timeout, prev=prev_index)
            if ret:
                prev_index = ret[0]['INDEX']
                yield ret[0]
                num -= 1
            else:
                break

    def find(self, num=1, protocol='HTTPS', timeout=1, prev=-1):
        """
        查到可用代理ip
        :param num:         返回数目
        :param protocol:    应用协议HTTPS/HTTP
        :param timeout:     超时
        :param prev:        上一个可用索引（无需设置，仅供迭代器）
        :return:
        """
        assert protocol != '' and num != 0
        protocol_lower = protocol.lower()
        url = '://'.join((protocol_lower, self._proxy_site))
        ret = []
        with requests.session() as session:
            session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
            session.headers['Accept-Language'] = "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
            session.keep_alive = True
            prev = prev + 1 if prev > 0 else 0
            for ip in self._xici_target_list[prev:]:
                if protocol == ip['PROTOCOL']:
                    proxy_data = {protocol_lower: r'%s://%s:%d/' % (protocol_lower, ip['IP'], ip['PORT'])}
                    try:
                        resp = session.head(url, proxies=proxy_data, timeout=timeout, verify=False)
                        if resp.reason == 'OK':
                            ret.append({'INDEX': ip['INDEX'], 'IP': ip['IP'], 'PORT': ip['PORT'], 'PROTOCOL': ip['PROTOCOL'],'PROXY': proxy_data})
                            if len(ret) == num:
                                break
                        resp.close()
                    except:
                        continue
        return ret

    def _validate_data(self):
        """
        请求代理数据（使用了西祠代理）
        :return:
        """
        if (os.path.exists(self._file) is False) or (int(time.time()) - int(os.path.getmtime(self._file)) >= 3600):
            wb = StringIO()
            writer = csv.writer(wb)
            with requests.session() as session:
                session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
                session.headers['Accept-Language'] = "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
                csv_data = []
                i = 0
                for p in self._xici_url_list:
                    resp = session.get(p, verify=False)
                    if resp.reason == 'OK' and resp.text != '':
                        doc = etree.HTML(resp.text)
                        items = doc.xpath(r'//table[@id="ip_list"]/tr[position()>1]')
                        for item in items:
                            csv_data.clear()
                            tdis = item.xpath('td')
                            ii = 0
                            for tdi in tdis:
                                if ii in (1, 2, 3, 4, 5, 9):
                                    if ii == 3:
                                        tmp_a = tdi.find('a')
                                        if tmp_a is not None:
                                            csv_data.append(tmp_a.text)
                                        else:
                                            csv_data.append('')
                                    else:
                                        csv_data.append(tdi.text)
                                ii += 1
                            self._xici_target_list.append({'INDEX': i, 'IP': csv_data[0], 'PORT': int(csv_data[1]), 'PROTOCOL': csv_data[4]})
                            writer.writerow(csv_data)
                            i += 1
                # 写入文件
                if wb.getvalue():
                    with open(self._file, 'w', newline='') as w: w.write(wb.getvalue())
        if not self._xici_target_list:
            with open(self._file, 'r', newline='') as o:
                reader = csv.reader(o)
                i = 0
                for row in reader:
                    self._xici_target_list.append({'INDEX': i, 'IP': row[0], 'PORT': int(row[1]), 'PROTOCOL': row[4]})
                    i += 1
        return len(self._xici_target_list) != 0
# End Of File proxy.py
