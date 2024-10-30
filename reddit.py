from bs4 import BeautifulSoup
import requests
import pandas as pd

class RedditScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    def connect(self, url):
        res = requests.get(url)
        if res.status_code == 200:
            self.soup = BeautifulSoup(res.content, 'html.parser')
            self.get_posts()
        else:
            print(f"Error: Unable to connect to the URL. Status code: {res.status_code}")

    def get_posts(self):
        posts_data = []
        try:
            posts = self.soup.find_all('article', {'class': 'w-full m-0'}, limit=3)
            for post in posts:
                title = upvotes = full_link = ''
                title_tag = post.find('a')
                if title_tag:
                    title = title_tag.get_text()
                else:
                    print("No title found")
                print(title)

                link = post.find('a').get('href')
                if link.startswith('/'):
                    full_link = f"https://www.reddit.com{link}"  
                print(full_link)
                
                # Tenta encontrar o número de upvotes na página HTML
                upvote_tag = post.find('faceplate-number')
                if upvote_tag:
                    upvotes = upvote_tag.get('number')
                else:
                    # Se não encontrar, tenta obter os dados via JSON
                    upvotes = self.get_json_upvotes(link)

                print(f"Upvotes: {upvotes}")

                posts_data.append({
                    'Title': title,
                    'Upvotes': upvotes,
                    'Link': full_link,
                })
            self.save_to_csv(posts_data)
        except Exception as e:
            print(f"Error: {e}")

    def get_json_upvotes(self, link):
        # Faz a requisição à API JSON para obter os dados do post
        json_url = f"https://www.reddit.com{link}.json"
        try:
            response = requests.get(json_url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                # Imprime a estrutura do JSON para verificar
                # print(data)
                
                # Verifica se a estrutura é a esperada
                if len(data) > 0 and 'data' in data[0] and 'children' in data[0]['data'] and len(data[0]['data']['children']) > 0:
                    return data[0]['data']['children'][0]['data']['ups']
                else:
                    print("Unexpected JSON structure or no children found.")
                    return 0
            else:
                print(f"Error: Unable to fetch JSON data. Status code: {response.status_code}")
                return 0
        except Exception as e:
            print(f"Error fetching JSON: {e}")
            return 0

    def save_to_csv(self, data):
        df = pd.DataFrame(data)
        df.to_csv('reddit_posts.csv', index=False)
        print("Data saved to reddit_posts.csv")

if __name__ == "__main__":
    url = "https://www.reddit.com/r/programming/"
    reddit_scraper = RedditScraper()
    reddit_scraper.connect(url)
