import scrapy
from steel_angle_section.items import AngleSectionItem
import re


class QuotesSpider(scrapy.Spider):
    name = "angle_sections"

    def start_requests(self):
        #response.css('div.row-fluid img::attr(src)').get()
        
        yield scrapy.Request(url='http://www.staticstools.eu/pl/profile-he/HE300C/', callback=self.parse)

    def parse(self, response):
        self.log("TUTAJ RESPONSE")
        self.log(response)

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
        """
        self.log(item)
        """
        
        """
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