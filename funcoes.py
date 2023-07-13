from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


url = 'https://www.situacao-cadastral.com'
cpf = ''


def abre_navegador(url):
    servico = Service(ChromeDriverManager().install())
    option = Options()
    option.add_argument('--headless=new')
    navegador = webdriver.Chrome(service=servico, options=option)
    navegador.delete_all_cookies()
    navegador.get(url)
    return navegador


def busca_cpf(cpf, navegador):
    input_cpf = navegador.find_element(By.ID, "doc")
    input_cpf.send_keys(cpf)
    input_cpf.send_keys(Keys.RETURN)


def coleta_resultado_do_navegador_quando_cpf_existe(navegador):
    documento = navegador.find_elements(By.XPATH, "//div[@id='resultado']/span[@class='dados documento']")
    documento = documento[0].get_attribute('innerHTML')
    try:
        nome = navegador.find_elements(By.XPATH, "//div[@id='resultado']/span[@class='dados nome']")
        nome = nome[0].get_attribute('innerHTML')
    except:
        nome = None
    situacao = navegador.find_elements(By.XPATH, "//div[@id='resultado']/span[@class='dados situacao']/span")
    situacao = situacao[0].get_attribute('innerHTML')
    texto = navegador.find_elements(By.XPATH, "//div[@id='resultado']/span[@class='dados texto']/p")
    texto = texto[0].get_attribute('innerHTML')
    return [documento, nome, situacao, texto]


def coleta_resultado_do_navegador_quando_cpf_invalido(navegador):
    mensagem = navegador.find_elements(By.ID, "mensagem")
    try:
        mensagem = mensagem[0].get_attribute('innerHTML')
    except:
        mensagem = "Ocorreu um erro durante a busca."
    return [mensagem.replace('\n', '')]


def consulta_cpf(url=url, cpf=cpf):
    navegador = abre_navegador(url)
    busca_cpf(cpf, navegador)
    try:
        resultado = coleta_resultado_do_navegador_quando_cpf_existe(navegador)
        navegador.quit()
        return resultado
    except:
        resultado = coleta_resultado_do_navegador_quando_cpf_invalido(navegador)
        navegador.quit()
        return resultado


if __name__ == '__main__':
    print(consulta_cpf())
