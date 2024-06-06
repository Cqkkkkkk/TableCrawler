import pdb
import scrapy
from scrapy.http import Response

class TableSpiderMSCreate(scrapy.Spider):
    name = "mscreate"
    start_urls = [
        """
        https://create.microsoft.com/en-us/templates/employee-recognition
        """
    ]

    def parse(self, response: Response):
        # return super().parse(response, **kwargs)
        
        cards = response.css('div[role="listitem"]')
        for card in cards:
            # pdb.set_trace()
            url = card.css('a.TemplateThumbnailCard_thumbnailImageWrapper__cxweM::attr(href)').get()
            
            yield {
                "url": response.urljoin(url)
            }
            
    
