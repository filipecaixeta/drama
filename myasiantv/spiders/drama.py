# -*- coding: utf-8 -*-
import scrapy 
from scrapy.shell import inspect_response
from pprint import pprint

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
            yield scrapy.Request(url=link, #+'download/',
                            method="GET",
                            dont_filter=True,
                            callback=self.parse15,
                            headers=headers)
    
    def parse15(self, response):
        drama = {
            'poster': response.css('img.poster').attrib['src']
        }
        p = response.css('div.movie>div.left>p')
        for key in p:
            tipo = key.css('strong::text').extract_first().strip(':').strip().lower().replace(' ','_')
            if tipo == 'genre':
                valor = key.css('span>a::text').extract()
            else:
                valor = key.css('span::text').extract_first()
            drama[tipo] = valor

        drama['cast'] = drama['cast'].split(', ')
        drama['release_year'] = int(drama['release_year'])
        drama['info'] = '/n'.join(response.css('div.info>p::text').extract())
        drama['rating'] =  float( response.css('span[itemprop=average]>strong::text').extract_first())
        drama['votes'] =  int(response.css('span[itemprop=votes]::text').extract_first())
        drama['trailer'] =  response.css('iframe').attrib.get('src')
        drama['tabela'] = 'description'  

        yield drama

        headers = headers20
        headers['Referer'] = response.request.url


        return

        yield scrapy.Request(url=response.request.url +'download/',
                            method="GET",
                            dont_filter=True,
                            callback=self.parse20,
                            meta = {'drama':drama},
                            headers=headers)
        #inspect_response(response, self)

    def parse20(self, response):
        drama = response.meta['drama']
        #inspect_response(response, self)
        episodes = {}
        for episode in response.xpath('//div[@class="play"]//a'):
            val = episode.xpath('@href').extract_first()
            key = episode.xpath('text()').extract_first()
            episodes[key] = val

        for name, link in episodes.items():
            yield scrapy.Request(url=link,
                            method="GET",
                            dont_filter=True,
                            callback=self.parse30,
                            meta = {'drama':drama},
                            headers=headers30)

    def parse30(self, response):
        videos = response.xpath('//div[@class="mirror_link"]//a/@href').extract()
        yield response.meta['drama']


    def parse40(self, response):
        with('./Fates.and.Furies.E01.mp4','wb') as f:
            f.write(response.body)
        # inspect_response(response, self)