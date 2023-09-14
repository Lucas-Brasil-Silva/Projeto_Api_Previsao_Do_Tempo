from itemadapter import ItemAdapter
from pymongo import MongoClient

class DadosClimaticosMongoPipeline:
    """
    Uma classe Scrapy Pipeline para processar e armazenar dados climáticos em um banco de dados MongoDB.

    Esta classe recebe itens da spider e os transforma em um formato adequado antes de inseri-los no banco de dados MongoDB.

    Atributos:
        collection_name (str): O nome da coleção no banco de dados onde os dados serão armazenados.

    Métodos:
        __init__(self, mongo_uri, mongo_db): Inicializa a pipeline com as configurações do MongoDB.
        from_crawler(cls, crawler): Cria uma instância da classe a partir das configurações do Scrapy.
        open_spider(self, spider): Inicializa a conexão com o MongoDB antes de começar a coleta de dados.
        close_spider(self, spider): Fecha a conexão com o MongoDB após a coleta de dados e insere os dados processados.
        process_item(self, item, spider): Processa e transforma os itens da spider antes de inseri-los no MongoDB.

    Configuração:
        Certifique-se de ter a biblioteca Scrapy instalada e configurada corretamente.
        Certifique-se de ter a biblioteca pymongo instalada e configurada corretamente.
        Configure as configurações do MongoDB no arquivo de configuração do Scrapy (settings.py) definindo as constantes "MONGO_URI" e "MONGO_DATABASE".

    Exemplo de uso:
        Configure esta classe como uma pipeline no arquivo de configuração do Scrapy:
        ITEM_PIPELINES = {
            'seuprojeto.pipelines.DadosClimaticosMongoPipeline': 300,
        }

    """
    collection_name = "Previsao_do_tempo"

    def __init__(self, mongo_uri, mongo_db):
        """
        Inicializa a pipeline com as configurações do MongoDB.

        Parâmetros:
            mongo_uri (str): A URI de conexão do MongoDB.
            mongo_db (str): O nome do banco de dados MongoDB.
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        Cria uma instância da classe a partir das configurações do Scrapy.

        Parâmetros:
            crawler (scrapy.crawler.Crawler): Uma instância do Crawler do Scrapy.

        Retorna:
            DadosClimaticosMongoPipeline: Uma instância da classe.

        """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        """
        Inicializa a conexão com o MongoDB antes de começar a coleta de dados.

        Parâmetros:
            spider (scrapy.spiders.Spider): A instância da spider atual.

        """
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.novos_dados = []

    def close_spider(self, spider):
        """
        Fecha a conexão com o MongoDB após a coleta de dados e insere os dados processados.

        Parâmetros:
            spider (scrapy.spiders.Spider): A instância da spider atual.

        """
        self.db[self.collection_name].delete_many({})
        for dado in self.novos_dados:
            self.db[self.collection_name].insert_one(dado)
        self.client.close()

    def process_item(self, item, spider):
        """
        Processa e transforma os itens da spider antes de inseri-los no MongoDB.

        Parâmetros:
            item (scrapy.Item): O item a ser processado.
            spider (scrapy.spiders.Spider): A instância da spider atual.

        Retorna:
            scrapy.Item: O item processado.

        """
        dados = ItemAdapter(item).asdict()
        cidade_data_ = dados['cidade data'].replace(',','-').split('-') 
        dados_processados = {
            'cidade':cidade_data_[0],
            'data':cidade_data_[2] + '-' + cidade_data_[3],
            'codicao meteorologica':dados['codicao meteorologica'],
            'temperatura':str((int(dados['temperatura minima'].replace('°C',''))+int(dados['temperatura maxima'].replace('°C','')))//2)+'°C',
            'umidade':str((int(dados['umidade minima'].replace('%',''))+int(dados['umidade maxima'].replace('%','')))//2)+'%',
            'vento':dados['vento']
        }
        self.novos_dados.append(dados_processados)
        return item