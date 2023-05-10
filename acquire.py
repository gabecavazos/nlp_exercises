from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os

def get_codeup_blog_articles():
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    list_of_p_elements = soup.find_all('p')
    list_of_h2_elements = soup.find_all('h2')
    codeup_blog_articles = []

    for i in range(len(list_of_h2_elements)):
        # Create a dictionary for each article
        article_dict = {}
        
        # Extract title using regex
        title_search = re.search('<a href=".+">(.+)</a>', str(list_of_h2_elements[i]))
        if title_search is not None:
            article_dict['title'] = title_search.group(1)
        
        # Extract content using regex
        content_search = re.search('<p>(.+)</p>', str(list_of_p_elements[i*2+1])) # assumes every other p element is content
        if content_search is not None:
            article_dict['content'] = content_search.group(1)
        
        # Add the article to the list
        codeup_blog_articles.append(article_dict)
    return codeup_blog_articles


def get_news_articles(use_cache=True):
    # Define the filename for the cache file
    cache_file = 'news_articles.csv'

    # Check if we should use the cache file
    if use_cache and os.path.exists(cache_file):
        # Read the data from the cache file
        news_articles = pd.read_csv(cache_file).to_dict('records')
    else:
        # The base url
        base_url = "https://inshorts.com/en/read/"
        
        # List of news categories we're interested in
        categories = ["business", "sports", "technology", "entertainment"]

        # List to store the news articles
        news_articles = []

        # Loop over each category
        for category in categories:
            # Fetch the HTML of the page
            response = requests.get(base_url + category)

            # If the GET request is successful, the status code will be 200
            if response.status_code == 200:
                # Get the content of the response
                page_content = response.content

                # Create a BeautifulSoup object and specify the parser
                soup = BeautifulSoup(page_content, 'html.parser')

                # Find all the news cards on the page
                news_cards = soup.find_all('div', class_=['news-card'])

                # Loop over each news card
                for card in news_cards:
                    # Get the title of the news
                    title = card.find('span', itemprop='headline').string

                    # Get the content of the news
                    content = card.find('div', itemprop='articleBody').string

                    # Add the news article to the list
                    news_articles.append({
                        "title": title,
                        "content": content,
                        "category": category
                    })

        # Save the data to the cache file
        pd.DataFrame(news_articles).to_csv(cache_file, index=False)

    # Return the list of news articles
    return news_articles
