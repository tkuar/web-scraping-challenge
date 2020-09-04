# Dependencies
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
from config import path


def init_browser():

    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': path}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    """
        Scrape NASA Mars News site for latest article title and summary, 
        JPL Mars Space Images site for featured image url,
        Mars Weather twitter account for latest weather tweet, 
        Mars Facts webpage for the table containg facts about the planet, 
        USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres, 
        and  Return a dictionary with all of the scraped data.
    """
    browser = init_browser()

    # Visit NASA Mars News site using splinter
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    # Allow webpage to load
    time.sleep(10)

    # HTML Object
    news_html = browser.html

    # Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(news_html, 'html.parser')

    # Retrieve the element that contains the latest article title and summary paragraph
    news_title = news_soup.find('ul', class_='item_list').find('li', class_='slide').find(
        'div', class_='list_text').find('div', class_='content_title').find('a')

    news_p = news_soup.find('ul', class_='item_list').find('li', class_='slide').find(
        'div', class_='list_text').find('div', class_='article_teaser_body')

    # Get only the text from the retrieved data
    news_title = news_title.text
    news_p = news_p.text

    # Print title and paragraph
    print(f'NASA Mars News title: {news_title}')
    print('----------------')
    print(f'NASA Mars News summary: {news_p}')

    # Visit `JPL Mars Space Images - Featured Image` url using splinter
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    # Allow webpage to load
    time.sleep(10)

    # HTML Object
    img_html = browser.html

    # Parse HTML with Beautiful Soup
    img_soup = BeautifulSoup(img_html, 'html.parser')

    # Retrieve the featured image url info
    featured_img = img_soup.find('article', class_='carousel_item')['style']

    # Extract only the url to image
    img_url = featured_img.replace(
        "background-image: url('", "").replace("');", "")

    # Create full url to full-size featured image
    featured_image_url = 'https://www.jpl.nasa.gov' + img_url

    # Print full url
    print(featured_image_url)

    # Visit Mars Weather twitter account url using splinter
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # Allow webpage to load
    time.sleep(20)

    # HTML Object
    weather_html = browser.html

    # Parse HTML with Beautiful Soup
    weather_soup = BeautifulSoup(weather_html, 'html.parser')

    # Retrieve all the text on the Mars Weather twitter account page
    twitter_text_data = weather_soup.find_all(
        'span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')

    # Create an empty string to hold the latest Mars Weather report tweet
    mars_weather = ''

    # Loop to find the latest Mars Weather report tweet
    for tweet in twitter_text_data:

        # Extract the text
        tweet_text = tweet.text

        # Find the weather report tweet
        if 'insight' and 'sol' in tweet_text:

            # Store that tweet
            mars_weather = tweet_text

            break

    # Print the latest Mars Weather report tweet
    print('----------------')
    print(f'Mars Weather tweet: {mars_weather}')

    # URL to Mars Facts webpage
    facts_url = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    facts_tables = pd.read_html(facts_url)

    # Create dataframe with columns ['description', 'value']
    facts_df = facts_tables[0]
    facts_df.columns = ['description', 'value']

    # Use Panda's `to_html` to generate a HTML table from the dataframe
    facts_html_table = facts_df.to_html(index=False, justify='justify-all', classes='table table-striped')

    # Strip unwanted newlines to clean up the table
    facts_html_table.replace('\n', '')

    # Print the cleaned html table
    print('----------------')
    print(f'Mars Fact Table: {facts_html_table}')

    # Visit USGS Astrogeology site using splinter
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # # Allow webpage to load
    # time.sleep(10)

    # HTML Object
    hemisphere_html = browser.html

    # Parse HTML with Beautiful Soup
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    # Retrieve all the elements that contain Mars hemisphere title and item info
    hemisphere_items = hemisphere_soup.find_all('div', class_='item')

    # Create empty list to hold dictionaries of hemispheres' titles
    # and their image urls
    hemisphere_image_urls_list = []

    # Loop to extract hemispheres' titles and image url
    for item in hemisphere_items:

        # Extract title
        title = item.find('h3').text

        # Extract partial url
        url = item.find('a', class_='itemLink product-item')['href']

        # Visit specific hemisphere page with full image using splinter
        browser.visit('https://astrogeology.usgs.gov' + url)

        # # Allow webpage to load
        # time.sleep(5)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract image src
        url_src = soup.find('img', class_='wide-image')['src']

        # Save full-size image url
        img_url = 'https://astrogeology.usgs.gov' + url_src

        # Append dictionary of title and img_url to hemispheres_list
        hemisphere_image_urls_list.append({'title': title,
                                           'img_url': img_url}
                                          )

    # Exit browser
    browser.quit()

    # Print list of dictionaries
    print('----------------')
    pprint(f'Mars Hemispheres image urls: {hemisphere_image_urls_list}')

    # Dictionary to store all scraped data
    mars_dict = {'news_title': news_title,
                 'news_p': news_p,
                 'featured_image_url': featured_image_url,
                 'mars_weather': mars_weather,
                 'facts_table': facts_html_table,
                 'hemisphere_image_urls': hemisphere_image_urls_list}

    return mars_dict
