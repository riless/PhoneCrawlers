#! /usr/bin/python2.7

from functions import *


class ToutypasseSpider(CrawlSpider):
	outputHandle = open('toutypasse.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date, depart) VALUES')

	starttime = datetime.now()
	name = "toutypasse"
	allowed_domains = ["toutypasse.com"]
	start_urls = [
		"http://www.toutypasse.com/annonce/provence-alpes-cote-d-azur-bouches-du-rhone/appartement-marseille-1-piece-s-21-m2-TOPe5a8c535"
	]


	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("toutypasse.com",)),
			callback='parse_page', follow=True
		),
	)

	total = 2080000
	indicatif = '33'
	country = 'fr'
	i = 1
	err = 0
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)
		# print "[+]"+response.url
		# try:
		depart = hxs.select('//div[@id="column-central"]/div[@class="detail_infos"]/div[1]/ul/li[1]/div[2]/text()').extract()[0]
		if depart.split(',')[0] == 'France':
			location = hxs.select('//div[@id="column-central"]/div[@class="detail_infos"]/div[1]/ul/li[2]/div[2]/text()').extract()[0]
			phone_raw = hxs.select('//div[@id="reply_phone_number"]/script/text()').extract()[0]
			phone_raw = match( phone_raw, '([0-9]{2}#){10}').split('#')

			phone = ''
			for n in phone_raw:
				if n.strip() != '':
					phone += str(int(n)-48)
			if phone[0] == '0':
				phone = phone[1:]
			if phone[:2] != self.indicatif:
				phone = self.indicatif+phone

			depart = depart.split(',')[len(depart) - 1]
			location = location.split('-')[0].strip()
			norm_location = normalize( location )

			crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			duration = (datetime.now() - self.starttime).total_seconds()
			speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
			speedmin = math.ceil( ( self.i / duration ) * 60 )
			taux = (self.i * 100) / (self.i + self.err)

			progression =  ((self.i + self.err) * 100) / self.total

			if len(phone) == 11 and len(location) != '':
				self.outputHandle.write('("'+phone+'", "'+self.country+'", "'+location+'", "'+norm_location+'", "'+crawl_datetime+'", "'+depart+'"),'+"\n")
				print "[{}] {}% [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {} | {}".format(self.i, taux, progression, int(speedmin), int(speed), phone, crawl_datetime, location, norm_location, depart )

				self.i += 1
			else:
				self.err += 1
		# except:
		# 	self.err += 1

