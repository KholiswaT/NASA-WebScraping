from splinter import Browser
from bs4 import BeautifulSoup as bs
import re


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

#Mars News Scrape
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find_all('div', class_='content_title')[1].text
    title_text = soup.find_all('div', class_='article_teaser_body')[0].text

#Mars Featured Image Scrape
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    image_html = browser.html
    image_bs = bs(image_html, 'html.parser')
    featured_images = image_bs.find('article', class_='carousel_item')['style']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_images


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
    
#Connect to Mars hemisphere website 
    mars_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere)
    
    mars_hemisphere_html = browser.html
    mars_hemisphere_bs = bs(mars_hemisphere_html, 'html.parser')
    mars_hemisphere = mars_hemisphere_bs.find_all('img', class_ ='thumb')

    mars_hemisphere_image_urls= []

    for hemisphere in mars_hemisphere:
        image_title = hemisphere.attrs['alt'].replace('Enhanced thumbnail','')
        image_url = hemisphere.attrs['src']
        mars_hemisphere_image_urls.append({'Title':image_title,'Image URl':image_url})

    mars_hemisphere_image_urls

    return mars
