from bs4 import BeautifulSoup
import requests
import  json

class MagazineScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    def connect(self, url):
        res = requests.get(url)
        if  res.status_code == 200:
            self.soup = BeautifulSoup(res.content, 'html.parser')
            self.get_product()
        else:
            print(f"Error: Unable to connect to the URL. Status code: {res.status_code}")

    def get_product(self):
        self.title=self.soup.find('h1', class_= 'product-name').text.strip()
        self.price=self.soup.find('span', class_= 'price').text.strip().replace('R$', '').replace('.', '').replace(',', '.').strip()
        self.dojson()

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