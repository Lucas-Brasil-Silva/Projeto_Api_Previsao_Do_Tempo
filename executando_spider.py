"""
Agendador de Execução de Spider para Coleta de Dados Climáticos

Este script Python foi projetado para agendar e executar periodicamente uma spider de coleta de dados climáticos
desenvolvida com Scrapy. Ele verifica se a spider está em execução, agenda novas execuções e gerencia a execução 
da spider dentro de um intervalo de tempo específico, controlando o uso de recursos da máquina.

Módulos Utilizados:
    - datetime: Para manipulação de data e hora.
    - time: Para operações relacionadas ao tempo.
    - threading.Thread: Para executar a spider em uma thread separada.
    - schedule: Para agendar execuções da spider.
    - psutil: Para verificar os processos em execução.
    - os: Para manipulação de caminhos de diretório.

Funções:
    - verificar_execucao_spider(spider='botdadosclimaticos'): Verifica se a spider está em execução.
    - executar_spider(): Executa a spider no diretório correspondente.
    - main(): Função principal que controla o agendamento da spider.

Configuração:
    - Certifique-se de ter a biblioteca Schedule e Psutil instalada e configurada corretamente.

Uso:
    - Certifique-se de que a spider Scrapy 'botdadosclimaticos' está definida e pronta para ser executada.
    - Execute este script Python para agendar e controlar a execução da spider de coleta de dados climáticos.
    - A execução da spider é agendada para ocorrer todos os dias das 7h às 20h, com intervalos de 1 hora dentro desse período.
    - O script também pausa a execução fora desse horário para economizar recursos da máquina.

Nota:
    - Ajuste as configurações de horário e caminhos de diretório conforme necessário para atender aos requisitos do seu projeto.

"""
from datetime import datetime, time, timedelta
from threading import Thread
from time import sleep
import schedule
import psutil
import os

def verificar_execucao_spider(spider='botdadosclimaticos'):
    for processo in psutil.process_iter(attrs=['pid','name','cmdline']):
        try:
            processo_cmdline = processo.info['cmdline']
            if processo_cmdline and spider in ''.join(processo_cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def executar_spider():
    caminho_spider = os.path.join(os.getcwd().replace('\\','/') + '/Dados_Climaticos')
    func = Thread(target=lambda: os.system(f'cd {caminho_spider} && scrapy crawl botdadosclimaticos'),daemon=True)
    func.start()

def main():
    agenda = schedule.Scheduler()
    while True:
        
        iniciar_execucao = time(7)
        finalizar_execucao = time(20)
        hora_atual = time(datetime.now().hour)

        agenda.run_pending()
        sleep(1)
        
        if not verificar_execucao_spider():
            eventos = agenda.get_jobs()
            if not eventos:
                agenda.every().day.at('07:00').do(executar_spider)

            elif iniciar_execucao < hora_atual < finalizar_execucao:
                if not [True for evento in eventos if evento.unit == 'hours']:
                    agenda.every(1).hour.do(executar_spider)
                    print(agenda.get_jobs())
                    sleep(3420)

            elif hora_atual >= finalizar_execucao:
                if [True for evento in eventos if evento.unit == 'hours']:
                    agenda.cancel_job([evento for evento in eventos if evento.unit == 'hours'][0])
                elif [True for evento in eventos if evento.unit == 'days']:
                    evento_diario = [evento.next_run for evento in eventos if evento.unit == 'days'][0]
                    tempo_evento = timedelta(days=evento_diario.day, hours=evento_diario.hour, minutes=evento_diario.minute, seconds=evento_diario.second)
                    horario_atual = timedelta(days=datetime.now().day, hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second)
                    tempo_restante = (tempo_evento - horario_atual).seconds - 180
                    sleep(tempo_restante)
        else:
            eventos = agenda.get_jobs()
            print(agenda.get_jobs())
            if hora_atual >= finalizar_execucao:
                if [True for evento in eventos if evento.unit == 'hours']:
                    agenda.cancel_job([evento for evento in eventos if evento.unit == 'hours'][0])
            elif [True for evento in eventos if evento.unit == 'hours']:
                agenda.cancel_job([evento for evento in eventos if evento.unit == 'hours'][0])

if __name__ == '__main__':
    main()