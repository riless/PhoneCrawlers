#! /usr/bin/python2.7

from functions import *


class WannonceSpider(CrawlSpider):
	outputHandle = open('wannonce.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date, depart) VALUES')

	name = "wannonce"
	allowed_domains = ["m.wannonce.com"]
	start_urls = [
		"http://m.wannonce.com/"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("m.wannonce.com",)),
			callback='parse_page', follow=True
		),
	)

	total = 160000000 #source google
	indicatif = '36'
	country = 'fr'
	i = 1
	err = 0

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)
		print response.body
		#try:
		location = hxs.select('//span[@itemprop="addressLocality"]/text()').extract()[0]
		#phone = hxs.select('//div[@id="infos2"]/table/tbody/tr[2]/td//img[3]/@src').extract()[0]
		depart = hxs.select('//span[@itemprop="addressRegion"]/text()').extract()[0]
		fid = mmatch(response.url, '[0-9]+.htm').replace('.htm', '')
		phone = ocr("http://www.wannonce.com/genImg/tel.htm?fid="+fid)
		phone = phone.replace(' ', '')
		if phone[0] == '0':
			phone = phone[1:]
		if phone[:2] != self.indicatif:
			phone = self.indicatif+phone

		location = location.strip()
		norm_location = normalize( location )

		crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		duration = (datetime.now() - self.starttime).total_seconds()
		speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
		speedmin = math.ceil( ( self.i / duration ) * 60 )
		taux = (self.i * 100) / (self.i + self.err)

		progression =  ((self.i + self.err) * 100) / self.total

		if len(phone) == 11 and len(location) != '':
			self.outputHandle.write('("'+phone+'", "'+self.country+'", "'+location+'", "'+norm_location+'", "'+crawl_datetime+'", "'+depart+'"),'+"\n")
			print "[{}] {}% [progress: {}%] ({}/min - {}/24h) - {} - {} - {} - {} - {}".format(self.i, taux, progression, int(speedmin), int(speed), phone, crawl_datetime, location, norm_location, depart )

			self.i += 1
		else:
			self.err += 1
		# except Exception as e:
		# 	self.err += 1
		# 	print e.message

