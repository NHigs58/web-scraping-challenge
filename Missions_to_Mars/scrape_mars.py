# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import pymongo


def scrape():

    mars_dict ={}

  # Mars News URL of page to be scraped
    browser = Browser("chrome", headless = False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    title_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    news_title = title_soup.find('div', class_='content_title').text
    news_par = title_soup.find('div', class_='rollover_description_inner').text
    browser.quit()

    # Mars Image to be scraped
    browser = Browser('chrome', headless=False)
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_image_url)
    time.sleep(5)
    image_soup = BeautifulSoup(html, 'html.parser')
    image_link = image_soup.find('img', src = True)
    # Retrieve featured image link
    featured_image_url = image_link['src']
    browser.quit()

    # Mars weather to be scraped
    mars_weather_url = 'https://twitter.com/MarsWxReport?lang=en'
    browser = Browser('chrome', headless=False) 
    browser.visit(mars_weather_url)
    time.sleep(5)
    weather_soup = BeautifulSoup(browser.html, 'html.parser')
    # Retrieve latest tweet with Mars weather info
    mars_weather = weather_soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text
    browser.quit()

    # Mars facts to be scraped, converted into html table
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(mars_facts_url)
    mars_facts = mars_facts_table[2]
    mars_facts.columns = ["Description", "Value"]
    mars_html_table = mars_facts.to_html()
    mars_html_table.replace('\n', '')
    
    # Mars hemisphere name and image to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser('chrome', headless=False)
    browser.visit(hemispheres_url)
    time.sleep(5)
    hemispheres_html = browser.html
    pics_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    # Mars hemispheres products data
    all_mars_hemispheres = pics_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    hemisphere_image_urls = []
    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url        
        hemisphere_image_urls.append(image_dict)
        browser.quit()
    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_par": news_par,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict