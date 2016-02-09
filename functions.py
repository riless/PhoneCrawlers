#! /usr/bin/python2.7

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from datetime import datetime
import math
import os
import unicodedata
import re
import string
import subprocess
import urllib
import time
import re

def strip_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def ocr(img):
	filename = str(time.time())+'.gif'
	urllib.urlretrieve(img, '/tmp/'+filename)
	proc = subprocess.Popen(['convert /tmp/'+filename+' /tmp/'+filename+'.png && gocr -i /tmp/'+filename+'.png -C 0-9 && rm /tmp/'+filename+'*'], stdout=subprocess.PIPE, shell=True)
	(phone, err) = proc.communicate()
	return phone.rstrip().replace(' ', '')

def strip(s, pattern):
	return re.sub(pattern, '', s)

def match(s, pattern):
	m = re.search(r''+pattern, s.encode('utf8'))
	if m:
		return m.group()
	return ''
def normalize(s):
	s = u''+s.decode('utf8')
	s = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
	return strip(s.lower(), '[^a-z]')
