#! /usr/bin/python2.7

from functions import *


class TopannoncesSpider(CrawlSpider):
	outputHandle = open('topannonces.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date, depart) VALUES')

	starttime = datetime.now()
	name = "topannonces"
	allowed_domains = ["topannonces.fr"]
	start_urls = [
		"http://www.topannonces.fr/pro/annonce-vente-maison-v23261807.html"
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=("topannonces.fr",)),
			callback='parse_page', follow=True
		),
	)

	total = 1083418
	indicatif = '36'
	country = 'fr'
	i = 1
	err = 0	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)
		try:
			print "[+]"+response.url
			print hxs.select('//*[@id="contacttelpopover"]/div/table/tbody/tr/td[2]/span/text()').extract()
			print hxs.select('//div[@id="infoad_content"]/table/tbody/tr[2]/td[2]/text()').extract()
			print hxs.select('//div[@id="contacttelpopover"]/div/table/tbody/tr/td/span/text()').extract()

			print phone, depart, location
			phone = phone.replace(' ', '')
			if phone[0] == '0':
				phone = phone[1:]
			if phone[:2] != self.indicatif:
				phone = self.indicatif+phone

			depart = depart.strip()[:2]
			location = location.title()

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
		except:
			self.err += 1

