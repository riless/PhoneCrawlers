#! /usr/bin/python2.7
# -*- coding: utf-8 -*- 

from functions import *


class AnibisSpider(CrawlSpider):

	name = "ani"
	url = "www.anibis.ch"
	country = 'ch'
	indicatif = '41'
	total =  3030000
	prefix = ('74', '76', '77', '78', '79')

	i = 1 # avoid devision by 0
	err = 0
	wr = 0

	starttime = datetime.now()

	outputHandle = open(name+'.sql', 'a')
	outputHandle.write('INSERT IGNORE INTO numbers(phone, country, city_nice, city, date) VALUES')

	allowed_domains = [url]
	start_urls = [
		"http://"+url
	]

	rules = (
		Rule(
			SgmlLinkExtractor(allow_domains=(url,)),
			callback='parse_page', follow=True
		),
	)
	

	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)
		# print "[+]",response.url
		location = hxs.select('//span[@class="property-description"]/div/a/text()').extract()
		phones = hxs.select('//div[@class="contact-form highlight-box whiteBG"]/div[@class="property"]/span[@class="property-description"]/text()').extract()
		
		# try:
		if len(phones)>0 and len(location)>0:
			location = strip(location[0], '^[0-9]+').encode('utf8')
			location = strip(location, '\s*\(.+\)\s*$')

			norm_location = normalize( location )

			for phone in phones:
				phone = strip(phone, '[^0-9]')
				phone = strip(phone, '^0*')

				if phone[:len(self.indicatif)] != self.indicatif:
					phone = self.indicatif+phone
				
				# print phone, location

				crawl_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

				duration = (datetime.now() - self.starttime).total_seconds()
				speed = math.ceil( ( self.i / duration ) * 3600 * 24 )
				speedmin = math.ceil( ( self.i / duration ) * 60 )
				t =  (self.i + self.err + self.wr)
				taux = (self.i * 100) / t
				tauxWr = (self.wr * 100) / t 

				progression =  ((self.i + self.err) * 100) / self.total

				regex_prefix = "("
				for p in self.prefix:
					regex_prefix += p+"|"
				regex_prefix = regex_prefix[:-1] # get rid of the last |
				regex_prefix += ")"

				separator = ''
				if (t > 1):
					separator = ','

				if ( match(phone, '^'+self.indicatif+regex_prefix) ):
					self.outputHandle.write( '{}\n("{}", "{}", "{}", "{}", "{}")'.format(separator, phone, self.country, location, norm_location, crawl_datetime) );
					print "[{}] {}% OK {}% Wr [progress: {}%] ({}/min - {}/24h) | {} | {} | {} | {}".format(self.i, taux,tauxWr, progression, int(speedmin), int(speed), phone, crawl_datetime, location, norm_location )

					self.i += 1
				else:
					self.wr += 1
	# 	else:
	# 		self.wr += 1

		# except:
		# 	self.err += 1

