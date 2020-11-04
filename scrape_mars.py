from splinter import Browser
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from time import sleep


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    mars_data = {}

#Mars News Scrape
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    try:
        news_title = soup.find('li', class_ = "slide").find('div', class_='content_title').text
        title_text = soup.find('li', class_ = "slide").find('div', class_='article_teaser_body').text

        mars_data['news_title'] = news_title
        mars_data['title_text'] = title_text

    except:
        sleep(1)
        browser.reload()

        news_title = soup.find('div', class_='content_title').text
        title_text = soup.find('div', class_='article_teaser_body').text

        mars_data['news_title'] = news_title
        mars_data['title_text'] = title_text

#Mars Featured Image Scrape
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    jplbase = 'https://www.jpl.nasa.gov'
    browser.visit(jpl_url)
    browser.is_element_present_by_id("images", 1)
    image_html = browser.html
    image_bs = bs(image_html, 'html.parser')
    feature_image = image_bs.find(id="images")
    img_src = feature_image.find(class_ = "button fancybox")["data-fancybox-href"]
    featured_image_url = jplbase + img_src

    mars_data['featured_image_url'] = featured_image_url

#Scraping Space Facts for Mars data table
    space_facts = 'https://space-facts.com/mars/'
    browser.visit(space_facts)
    mars_html = browser.html
    mars_bs = bs(mars_html, 'html.parser')
    mars_table = mars_bs.find('table', class_='tablepress tablepress-id-p-mars')
    mars_df = pd.read_html(str(mars_table))[0]
    mars_df.columns = ['Description','Parameters']
    mars_df = mars_df.set_index(['Description'])
    mars_html = mars_df.to_html()
    
    mars_data['mars_html'] = mars_html

#Connect to Mars hemisphere website 
    mars_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere)
    urlbase = 'https://astrogeology.usgs.gov/'
    mars_hemisphere_html = browser.html
    mars_hemisphere_bs = bs(mars_hemisphere_html, 'html.parser')
    mars_hemisphere = mars_hemisphere_bs.find_all('img', class_ ='thumb')

    mars_hemisphere_image_urls= []

    for hemisphere in mars_hemisphere:
        image_title = hemisphere.attrs['alt'].replace('Enhanced thumbnail','')
        image_src = hemisphere.attrs['src']
        image_url = urlbase + image_src 
        mars_hemisphere_image_urls.append({'Title':image_title,'Image_URl':image_url})

    mars_hemisphere_image_urls

    mars_data['mars_hemisphere_image_urls'] = mars_hemisphere_image_urls
    

    browser.quit()

    return mars_data
