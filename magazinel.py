from bs4 import BeautifulSoup
import requests,json
from    selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class MagazineScraper:
    def __init__(self,browser="chrome"):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        self.driver=self.webdriver_setup(browser)

    def webdriver_setup(self):
        match self.browser.lower():
            case 'chrome':
                options = ChromeOptions()
                options.add_argument('--headless')  # Executar em modo headless
                driver = webdriver.Chrome(service=ChromeService(), options=options)
            case 'firefox':
                options = FirefoxOptions()
                options.add_argument('--headless')  # Executar em modo headless
                driver = webdriver.Firefox(service=FirefoxService(), options=options)
            case 'edge':
                options = webdriver.EdgeOptions()
                options.add_argument('--headless')  # Executar em modo headless
                driver = webdriver.Edge(service=webdriver.EdgeService(), options=options)
            case 'opera':
                options = webdriver.ChromeOptions()  # Opera é baseado em Chromium
                options.add_argument('--headless')  # Executar em modo headless
                driver = webdriver.Opera(service=webdriver.OperaService(), options=options)
            case 'safari':
                driver = webdriver.Safari()
            case _:
                raise ValueError("Unsupported browser")
        return driver

    def connect(self, url):
        res = requests.get(url)
        self.driver.get(url)
        if  res.status_code == 200:
            self.soup = BeautifulSoup(res.text, 'html.parser')
            self.get_product()
        else:
            print(f"Error: Unable to connect to the URL. Status code: {res.status_code}")

    def get_product(self):
        # self.title_element=self.soup.find('h1', {'data-testid':'heading-product-title'})
        # self.title=title_element.get_text(strip=True) if self.title_element else None
        # print(self.title)
        # self.price_element=self.soup.find('span', class_= 'sc-dcJsrY eLxcFM sc-eHsDsR eGPZvr')
        # self.price=(
            # self.price_element.text.strip().replace('R$ ', '').replace(',', '.').strip()
        # )
        # self.dojson()
        
        title_element = self.driver.find_element(By.XPATH, '//h1[@data-testid="heading-product-title"]')
        self.title = title_element.text if title_element else "Título não encontrado"
        
        # Captura o preço do produto
        price_element = self.driver.find_element(By.CLASS_NAME, 'price')
        self.price = (
            price_element.text.replace('R$', '').replace('.', '').replace(',', '.').strip()
            if price_element else "Preço não encontrado"
        )
    def dojson(self):
        product_info = {
            'title':self.title,
            'price':float(self.price) 
        }
        if product_info:
            product_info_json=json.dumps(product_info, ensure_ascii=False,incident=4)
            print(product_info_json)

if  __name__=="__main__":
    url = "https://www.magazineluiza.com.br/aparador-pelos-philips-one-blade-qp1424-10-philips-novo/p/237634500/pf/papp/"
    magascraper = MagazineScraper()
    magascraper.connect(url)