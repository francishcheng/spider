import scrapy
from datetime import datetime
import time
import re
from ..items import PachongItem
from ..settings import MAX_PAGE 
class SpiderSpider(scrapy.Spider):
    name = 'spider'
    # allowed_domains = ['helmenyun.cn']
    vendor = 'vendor298'
    start_urls = ['https://www.helmenyun.cn/index.php/DataManage/data_list/{page}']
    data_list_url = 'https://www.helmenyun.cn/index.php/DataManage/data_list/{page}'
    detail_url = 'https://www.helmenyun.cn/index.php/DataManage/data_detail?sql={vendor}&SNcode={SNcode}&sTime={sTime}&RecordID={RecordID}'
    def start_requests(self):
        
        for url in self.start_urls:
            yield scrapy.Request(url=url.format(page=1), callback=self.parse)

    def parse(self, response):
        # print(response.body)
        print(response.url)
        page = int(response.url.split('/')[-1])
        trs = response.xpath('//tbody[@class="TbodyList"]//tr')
        # RecordIDs , ItemIDs , BatchIDs , sSampleIDs , sItemNames , sBatchCodes , sTimes , Concentrations , Judges, CValues , TValues =  ([] for i in range(11)) 
        # res = []
        for tr in trs:
            item = PachongItem() 
            item['RecordID'] = tr.xpath('./td[@class="RecordID"]/text()').get(default='') 
            item['ItemID'] = tr.xpath('./td[@class="ItemID"]/text()').get(default='') 
            item['BatchID'] = tr.xpath('./td[@class="BatchID"]/text()').get(default='') 
            item['sSampleID'] = tr.xpath('./td[@class="sSampleID"]/text()').get(default='') 
            item['sItemName'] = tr.xpath('./td[@class="sItemName"]/text()').get(default='')
            item['sBatchCode'] = tr.xpath('./td[@class="sBatchCode"]/text()').get(default='')
            item['sTime'] = tr.xpath('./td[@class="sTime"]/text()').get(default='')
            item['Concentration'] = tr.xpath('./td[@class="Concentration"]/text()').get(default='')
            item['Judge'] = tr.xpath('./td[@class="Judge"]/text()').get(default='') 
            item['CValue'] = tr.xpath('./td[@class="CValue"]/text()').get(default='') 
            item['TValue'] = tr.xpath('./td[@class="TValue"]/text()').get(default='')
            item['SNcode'] = tr.xpath('./td[@class="check-bight"]/input/@value').get(default='')   
            item['sTimeNumber'] = tr.xpath('./td[@class="sTime"]/input/@value').get(default='')
            # res.append(item)
            yield scrapy.Request(self.detail_url.format(vendor=self.vendor, SNcode=item['SNcode'], sTime=item['sTimeNumber'], RecordID=item['RecordID']), callback=self.parse_detail, meta={'item':item}, dont_filter=True)    
        # print('RecordIDs', RecordIDs)
        # print('ItemIDs', ItemIDs)
        # print('BatchIDs', BatchIDs)
        # print('sSampleIDs', sSampleIDs)
        # print('sItemNames', sItemNames)
        # print('sBatchCodes', sBatchCodes)
        # print('sTimes', sTimes)
        # print('Concentrations', Concentrations)
        # print('Judges', Judges)
        # print('CValues', CValues)
        # print('TValues', TValues)
        # for ele in res:
        #     print(ele)
        # print(self.data_list_url.format(page=page))
        if page<=MAX_PAGE:
            yield scrapy.Request(self.data_list_url.format(page=page+1), callback=self.parse, dont_filter=True) 
        else:
            print('sleep 5min')
            time.sleep(5*60)
            yield scrapy.Request(self.data_list_url.format(page=1), callback=self.parse, dont_filter=True) 
        
    def parse_detail(self, response):
        # print(response.url)
        # print(response.meta['item'])
        item = response.meta['item']

        script = response.xpath('//script')[-1].extract()
        pattern = re.compile('curvePoint="(.*?)"') 
        res = re.search(pattern, script)
        points = res.groups(0)[0]
        item['points'] = points        
        item['address'] = response.xpath('./span[@class="address"]/text()').get(default='')   
        item['data_bight']  = response.xpath('//div[@class="data-bight"]/p').get(default='')
        item['create_time'] = datetime.now()
        yield item

        
