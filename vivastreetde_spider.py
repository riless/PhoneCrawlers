#! /usr/bin/python2.7

from functions import *


class VivastreetdeSpider(CrawlSpider):
	outputHandle = open('vivastreetde.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date) VALUES')

	starttime = datetime.now()
	name = "vivastreetde"
	allowed_domains = ["anzeigen-strasse.de"]
	start_urls = [
		"http://anzeigen-strasse.de"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("anzeigen-strasse.de",)),
			callback='parse_page', follow=True
		),
	)

	total = 68496
	indicatif = '49'
	country = 'de'
	i = 1
	err = 0
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)

		try:
			location = hxs.select('//dl/dd/div/text()').extract()[0]
			phone = hxs.select('//span[@id="phone_number"]/text()').extract()[0]
			phone = phone.replace(' ', '')
			if phone[0] == '0':
				phone = phone[1:]
			if phone[:2] != self.indicatif:
				phone = self.indicatif+phone

			location = location.split(',')[1].strip() 
			norm_location = normalize( location )

			crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			duration = (datetime.now() - self.starttime).total_seconds()
			speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
			speedmin = math.ceil( ( self.i / duration ) * 60 )
			taux = (self.i * 100) / (self.i + self.err)

			progression =  ((self.i + self.err) * 100) / self.total

			if len(phone) >=8 and len(phone) <=15 and len(location) != 0:
				self.outputHandle.write(u'("'+phone+'", "'+self.country+'", "'+location.decode('utf8')+'", "'+norm_location+'", "'+crawl_datetime+'"),'+"\n")
				print "[{}] {}% [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {}".format(self.i, taux, progression, int(speedmin), int(speed), phone, crawl_datetime, location.decode('utf8'), norm_location )
				self.i += 1
			else:
				self.err += 1
		except:
			self.err += 1

