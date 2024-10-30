from bs4 import BeautifulSoup
import requests, json, traceback

class MagazineScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    def connect(self, url):
        res = requests.get(url, headers=self.headers)
        if res.status_code == 200:
            self.soup = BeautifulSoup(res.content, 'lxml')
            self.get_product()
        else:
            print(f"Error: Unable to connect to the URL. Status code: {res.status_code}")

    def get_product(self):
        try:
            self.title = self.soup.select_one('[data-testid="heading-product-title"]').get_text().strip()

            self.price = (
                self.soup.select_one('[data-testid="price-value"]').get_text().replace('ou', '').replace('.', '').replace(',', '.').strip()
            )
            self.dojson()
        except Exception as e:
            print(f"Error: {str(e)}")
            traceback.print_exc()

    def dojson(self):
        product_info = {
            'title': self.title,
            'price': self.price 
        }
        if product_info:
            product_info_json = json.dumps(product_info, ensure_ascii=False, indent=4)
            print(product_info_json)

if __name__ == "__main__":
    url = "https://www.magazineluiza.com.br/aparador-pelos-philips-one-blade-qp1424-10-philips-novo/p/237634500/pf/papp/"
    magascraper = MagazineScraper()
    magascraper.connect(url)
