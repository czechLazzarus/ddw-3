import scrapy
import nltk

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://blog.idnes.cz/']

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "USER_AGENT": "scarp",
        "DEPTH_LIMIT": 20
    }

    def parse(self, response):
        patternLastName = [
            (r'[A-Z]{1}.*ova$', 'GW'),
            (r'[A-Z]{1}', 'GM'),
        ]
        patternSurnameName = [
            (r'[A-Z]{1}.*a$', 'GW'),
            (r'[A-Z]{1}', 'GM'),
        ]
        regexp_tagger_last_name = nltk.RegexpTagger(patternLastName)
        regexp_tagger_surname = nltk.RegexpTagger(patternSurnameName)

        for page in response.css('div.art'):
            title = page.css('h3 > a ::text').extract_first()
            description = page.css('p.perex ::text').extract_first()
            info = page.css('div.art-info ::text').extract_first()
            author = page.css('h4 > a ::text').extract_first()
            author_profile = page.css('h4 > a ::attr(href)').extract_first()
            date = info.split("|")[0]
            karma = info.split("|")[1]
            reads = info.split("|")[2].split(" ")[2]
            author = author.replace(u'\u00e1',"a")
            list_surname = regexp_tagger_surname.tag([author.split(" ")[0]])
            list_lastname = regexp_tagger_last_name.tag([author.split(" ")[1]])
            print(list_surname)
            print(list_lastname)
            for x, y in enumerate(list_lastname):
                genderTag_lastname = y[1]
            for x, y in enumerate(list_surname):
                genderTag_surname = y[1]
            if genderTag_lastname == genderTag_surname:
                if genderTag_lastname == "GW":
                    gender = "woman"
                elif genderTag_lastname == "GM":
                    gender = "man"
                else:
                    gender = "unknown"
            else:
                gender = "unknown"
            yield {'author':author,'gender': gender,'author_profile':author_profile, 'title': title, 'description': description,'date':date,'karma': karma,'total_reads':reads}

        next_page = response.css('div.col-a > table > tr > td.tar > a ::attr(href)').extract_first()

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
