from bs4 import BeautifulSoup
import requests
import pandas as pd

class RedditScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    def connect(self, url):
        res = requests.get(url)
        if  res.status_code == 200:
            self.soup = BeautifulSoup(res.content, 'html.parser')
            self.get_posts()
        else:
            print(f"Error: Unable to connect to the URL. Status code: {res.status_code}")

    def get_posts(self):
        posts_data = []
        try:
            posts = self.soup.find_all('article', {'class': 'w-full m-0'}, limit=3)
            for post in posts:
                title=upvotes=full_link=''
                title_tag=post.find('a')
                if title_tag:
                    title=title_tag.get_text()
                else:
                    print("No title found")
                print(title)

                link = post.find('a').get('href')
                if link.startswith('/'):
                    full_link = f"https://www.reddit.com{link}"  
                print(full_link)

                upvote_tag=post.find('span')
                if upvote_tag:
                    upvotes = upvote_tag.get('pretty number')
                else:
                    print("No upvotes found")
                print(upvotes)
                
                posts_data.append({
                    'Title': title,
                    'Upvotes': upvotes,
                    'Link': full_link,
                })
            self.save_to_csv(posts_data)
        except Exception as e:
            print(f"Error: {e}")

    def save_to_csv(self, data):
        df = pd.DataFrame(data)
        df.to_csv('reddit_posts.csv', index=False)
        
        print("Data saved to reddit_posts.csv")

if __name__ == "__main__":
    url = "https://www.reddit.com/r/programming/"
    reddit_scraper = RedditScraper()
    reddit_scraper.connect(url)