# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response

url10 = "https://myasiantv.to/drama/?selOrder=0&selCat=0&selCountry=4&selYear=0&btnFilter=Submit"
headers10 = {
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Language': "en-US,en;q=0.5",
    'DNT': "1",
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'Cache-Control': "no-cache",
    'TE': "Trailers",
}

headers20 = {
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Language': "en-US,en;q=0.5",
    'DNT': "1",
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'Cache-Control': "no-cache",
}

headers30 = {
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Language': "en-US,en;q=0.5",
    'DNT': "1",
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'Cache-Control': "no-cache",
}


class DramaSpider(scrapy.Spider):
    name = 'drama'

    def start_requests(self):
        headers10['Referer'] = "https://myasiantv.to/drama/?selOrder=1&selCat=0&selCountry=0&selYear=0&btnFilter=Submit"
        yield scrapy.Request(url=url10,
                            method="GET",
                            dont_filter=True,
                            callback=self.parse10,
                            headers=headers10)
            
    def parse10(self, response):
        links = list(set(response.xpath('//div[@id="list-1"]//a/@href').extract()))
        links = [link for link in links if link.find('drama/page-')==-1]
        links = links[:1]
        for link in links:
            headers = headers20
            headers['Referer'] = response.request.url
            yield scrapy.Request(url=link+'download/',
                            method="GET",
                            dont_filter=True,
                            callback=self.parse20,
                            headers=headers)
    
    def parse20(self, response):
        episodes = {}
        for episode in response.xpath('//div[@class="play"]//a'):
            val = episode.xpath('@href').extract_first()
            key = episode.xpath('text()').extract_first()
            episodes[key] = val
            break

        for name, link in episodes.items():
            yield scrapy.Request(url=link,
                            method="GET",
                            dont_filter=True,
                            callback=self.parse30,
                            headers=headers30)

    def parse30(self, response):
        videos = response.xpath('//div[@class="mirror_link"]//a/@href').extract()
        yield scrapy.Request(url=videos[-1],
                            method="GET",
                            dont_filter=True,
                            callback=self.parse40,
                            headers=headers30)

    def parse40(self, response):
        with('./Fates.and.Furies.E01.mp4','wb') as f:
            f.write(response.body)
        # inspect_response(response, self)