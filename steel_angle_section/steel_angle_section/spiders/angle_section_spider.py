import scrapy
from steel_angle_section.items import AngleSectionItem
import re
import pandas as pd


COUNTRY_PREFIX = 'pl'
SITE_URL = 'http://www.staticstools.eu/'
UNIT = 'mm'

#data.loc[len(data)]=[data[1].iloc[-1], '']
#data.drop([1], axis=1, inplace=True)
#data = pd.DataFrame([i.split(r' ') for i in data[0].map(str)])
#data.drop([1], axis=1, inplace=True)
#data.drop(df.head(1).index, inplace=True)
#df.columns=['symbol', 'value', 'unit']
class QuotesSpider(scrapy.Spider):
    name = "angle_sections"

    def start_requests(self):
        #response.css('div.row-fluid img::attr(src)').get()
        
        yield scrapy.Request(url=SITE_URL + COUNTRY_PREFIX,
                             callback=self.parse)

    def parse(self, response):
        
        all_cross_sections_links = response \
                                            .css('ul.nav-main.dropdown li a::attr(href)') \
                                            .extract()

        # append site root url
        all_cross_sections_links = [SITE_URL + item for item in all_cross_sections_links]

        # check if site links are unchanged as 19.08.2018
        have_they_not_changed = map(lambda x: 'pl/profile-' in x,
                                all_cross_sections_links)

        # if any of this strings does not 
        if not all(have_they_not_changed):
            return
        
        #all_cross_sections = [item[11:] for item in all_cross_sections_links]
        for url in all_cross_sections_links:
            yield scrapy.Request(url=url, callback=self.parse2)

    def parse2(self, response):
        all_categories = response.css('form select.form-control.bottom-space option::attr(value)').extract()
        all_links = []
        for category in all_categories:
            all_links.append(response.url + '/' + category + '/' + UNIT)

        for link in all_links:
            yield scrapy.Request(url=link, callback=self.parse3)

    def parse3(self, response):
        data = response.xpath("//table").extract()
        data = pd.read_html(data[0])[0]
        data.loc[len(data)]=[data[1].iloc[-1], '']
        data.drop([1], axis=1, inplace=True)
        data = pd.DataFrame([i.split(r' ') for i in data[0].map(str)])
        data.drop([1], axis=1, inplace=True)
        data.drop(data.head(1).index, inplace=True)
        data.columns = ['symbol', 'value', 'unit']

        item = AngleSectionItem()


        symbols = list(data['symbol'])
        item = generate_item_dynamically(symbols)

        for i in range(len(data)):
            item[data.iloc[i]['symbol']] = data.iloc[i]['value']

        """
        DIGITS_RE = re.compile('\d+')
        test = response.css('table.table.table-a td::text').extract()

        ostateczne = []

        for item5 in test:
            result = DIGITS_RE.search(item5)
            if result:
                ostateczne.append(result[0])

        self.log(ostateczne)
        
        item = AngleSectionItem()
        item['oznaczenie'] = "HE300C"
        item['wysokosc_przekroju'] = ostateczne[0] + " mm"
        
        
        
        item['szerokosc_przekroju'] = ostateczne[1] + " mm"
        item['grubosc_stopki'] = ostateczne[2] + " mm"
        item['grubosc_srodnika'] = ostateczne[3] + " mm"
        item['promien_przejscia'] = ostateczne[4] + " mm"
        item['wys_prostej_czesci'] = ostateczne[5] + " mm"
        item['odl_srodka_ciezkosci'] = ostateczne[6] + " mm"
        item['odl_srodka_scinania'] = ostateczne[7] + " mm"
        item['pochylenie_glo_osi_bezwl'] = ostateczne[8] + " mm^(2)"

        item['masa_na_jednostke_dlug'] = ostateczne[9] + " kg*m^(-1)"
        item['pole_przekroju']
        
        item['pole_powierzchni_ksztaltownika']

        item['geo_model_bezwl_ciala_plaskiego']
        item['modul_sprezystosci']
        item['modul_plastycznosci']
        item['promien_bezwladnosci']
        item['moment_statyczny_pola_figury_plaskiej']
        item['polarny_promien_bezwladnosci_przekroju']
        item['wycinkowy_moment_bezwladnosci']
        item['promien_bezwladnosci_skrecania']
        item['moment_bezwladnosci_przy_skrecaniu']
        item['stala_modulu_przy_skrecaniu']
        item['promien_bezwzladnosci_wzgledem_centra_scinania']
        item['moment_odsrodkowy']
        
        
        """
        yield item
        
def generate_item_dynamically(fields):
    item = scrapy.Item()
    for field in fields:
        item.fields[field] = scrapy.Field()
    return item