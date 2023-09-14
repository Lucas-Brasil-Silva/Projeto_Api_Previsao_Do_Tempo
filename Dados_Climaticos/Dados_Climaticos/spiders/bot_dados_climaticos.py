import scrapy
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from scrapy.selector import Selector
from time import sleep

def iniciar_driver():
    """ Inicializa e retorna uma instância do driver do Google Chrome configurado com opções personalizadas.

    Retorna:
        selenium.webdriver.Chrome: Uma instância do driver do Google Chrome.

    Configurações Personalizadas:
        - Idioma: Português do Brasil
        - Tamanho da janela: 1000x1000 pixels
        - Modo headless (sem interface gráfica)
        - Exclui logs do Chrome
        - Desabilita a solicitação de download
        - Desativa notificações do navegador
        - Permite downloads automáticos

    Nota:
        Certifique-se de ter o Chrome WebDriver instalado e no PATH do sistema.
        Certifique_se de ter a biblioteca Selenium instalada e configurada corretamenta. """

    chromeOptions = Options()
    LOGGER.setLevel(logging.WARNING)
    arguments = ['--lang=pt-BR', 'window-size=1000,1000', '--headless']
    for argument in arguments:
        chromeOptions.add_argument(argument)

    chromeOptions.add_experimental_option(
        'excludeSwitches', ['enable-logging'])

    chromeOptions.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(options=chromeOptions)

    return driver

class DadosClimaticosSpider(scrapy.Spider):
    """ Uma spider Scrapy para coletar dados climáticos de várias cidades a partir do site do INMET (Instituto Nacional de Meteorologia).

    A spider visita uma lista de URLs de previsão do tempo e extrai informações climáticas relevantes de cada página.

    Parâmetros:
        name (str): Nome da spider.

    Métodos:
        urls(self, file='codigo_IBGE.txt'): Gera uma lista de URLs individuais com base em códigos de cidades em um arquivo de entrada.
        start_requests(self): Inicializa as solicitações para as URLs especificadas.
        parse(self, response): Analisa as páginas de previsão do tempo e extrai informações climáticas.

    Configuração:
        Certifique-se de ter a biblioteca Scrapy instalada e configurada corretamente.

    """
    name = 'botdadosclimaticos'
    link = ['https://previsao.inmet.gov.br/3550308',
    'https://previsao.inmet.gov.br/4205407',
    'https://previsao.inmet.gov.br/4106902',
    'https://previsao.inmet.gov.br/3304557']

    def urls(self,file='codigo_IBGE.txt'):
        """
        Gera uma lista de URLs individuais que levam ao site do INMET (Instituto Nacional de Meteorologia) com a previsão do tempo correspondente a cada cidade.
        
        Parâmetros:
            file (str): O nome do arquivo de entrada que contém os códigos de cidade.
        
        Retorna:
            list: Uma lista com 5570 URLs geradas com base nos códigos de cidade.

        """
        with open(file,'r',encoding='UTF-8') as arquivo:
            codigos = arquivo.read().split(';')
            return ['https://previsao.inmet.gov.br/' + codigo for codigo in codigos]

    def start_requests(self):
        """ Inicializa as solicitações para as URLs especificadas. """
        urls_ = self.urls()
        for url in urls_:
            yield scrapy.Request(url=url,callback=self.parse, meta={'next_url':url})
    
    def parse(self,response):
        """
        Analisa as páginas de previsão do tempo e extrai informações climáticas.

        Parâmetros:
            response (scrapy.http.Response): A resposta HTTP da página da web.
        """
        driver = iniciar_driver()
        driver.get(response.meta['next_url'])
        sleep(2)
        response_webdriver = Selector(text=driver.page_source)
        yield {
            'cidade data':response_webdriver.xpath("//div//section[@class='grid grid-template-columns-2 no-border align-left'][1]/div/font/b/text()").get(),
            'codicao meteorologica':response_webdriver.xpath("//section[@id='row-1']//div[@class='grid grid-template-columns-2-minmax no-border']//font/text()").getall()[1].replace(':',''),
            'temperatura minima':response_webdriver.xpath("//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[0],
            'temperatura maxima':response_webdriver.xpath("//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[2],
            'umidade minima':response_webdriver.xpath("//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[5],
            'umidade maxima':response_webdriver.xpath("//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[4],
            'vento':response_webdriver.xpath("//div[@class='item']//section[@class='grid grid-template-columns-2 no-border']/div[@class='item']/font/text()").getall()[3]
        }
        yield {
            'cidade data':response_webdriver.xpath("//div//section[@class='grid grid-template-columns-2 no-border align-left'][2]/div/font/b/text()").get(),
            'codicao meteorologica':response_webdriver.xpath("//section[@id='row-2']//div[@class='grid grid-template-columns-2-minmax no-border']//font/text()").getall()[1].replace(':',''),
            'temperatura minima':response_webdriver.xpath("//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[6],
            'temperatura maxima':response_webdriver.xpath("//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[8],
            'umidade minima':response_webdriver.xpath("//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[11],
            'umidade maxima':response_webdriver.xpath("//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[10],
            'vento':response_webdriver.xpath("//div[@class='item']//section[@class='grid grid-template-columns-2 no-border']/div[@class='item']/font/text()").getall()[9]
        }
        for element in response_webdriver.xpath("//div[starts-with(@class,'row-')]"):
            yield {
                'cidade data':element.xpath(".//section[@class='grid grid-template-columns-1 no-border align-left']/div/font/b/text()").get(),
                'codicao meteorologica':element.xpath(".//section[@class='grid grid-template-columns-2-minmax no-border align-left']/div/font/text()").get().replace(':',''),
                'temperatura minima':element.xpath(".//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[0],
                'temperatura maxima':element.xpath(".//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[2],
                'umidade minima':element.xpath(".//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[5],
                'umidade maxima':element.xpath(".//section[@class='grid grid-template-columns-4']/div/font/text()").getall()[4],
                'vento':element.xpath(".//section[@class='grid grid-template-columns-2']/div/font/text()").getall()[1]
            }