# Web Scraping Homework - Mission to Mars
# Importing the relevant modules and packages
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def open_browser():
    # User log in for Windows Users
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = open_browser()

    #----------------------------------------------------#
    # Nasa Mars News
    #----------------------------------------------------#
    
    # URL to visit
    url = 'https://mars.nasa.gov/news/'

    # Browser Engine to load the URL
    browser.visit(url)

    # Setting up the html
    html = browser.html

    # Parsing with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Creating a variable for the first news title

    li_slide = soup.find_all('li', class_='slide')

    # Obtaining the body of the artile
    try:
        li_slide = soup.find_all('li', class_='slide')
        news_title = li_slide[0].find('div', class_='content_title').text.strip()
        news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    except(IndexError):
        
        time.sleep(10)
        
        # Setting up the html
        html = browser.html

        # Parsing with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        li_slide = soup.find_all('li', class_='slide')
        news_title = li_slide[0].find('div', class_='content_title').text.strip()
        news_p = soup.find_all('div', class_='article_teaser_body')[0].text
        

      

    browser.quit()

    #----------------------------------------------------#
    # JPL Mars Space Images - Featured Image
    #----------------------------------------------------#

    browser = open_browser()

    # URL to visit
    fi_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Browser Engine to load the URL
    browser.visit(fi_url)

    # Setting up the html
    fi_html = browser.html

    # Parsing with BeautifulSoup
    fi_soup = BeautifulSoup(fi_html, 'html.parser')

    # Base URL for Image
    base_url = 'https://www.jpl.nasa.gov'

    # Pausing for 10 seconds
    time.sleep(10)

    # Obtaining the featured image
    featured_image_pre = fi_soup.find('article', class_='carousel_item')['style'].strip('background-image: url') #Strip will remove these characters which are not required for the URL
    

    # Since we stil have the apostrophes and circle brackets within the strings, these will also need to be removed
    start = featured_image_pre.find("('") + len("('")
    end = featured_image_pre.find("')")
    substring = featured_image_pre[start:end]
    

    # Featured Image URL
    # As the Featured Image keeps changing on the website, the URL will be updated accordingly 
    browser.quit()
    featured_image = base_url + substring

    #----------------------------------------------------#
    # Mars Facts
    #----------------------------------------------------#

    # Establishing the URL
    table_url = 'https://space-facts.com/mars/'

    # Data Frame for tables
    table_df = pd.read_html(table_url)

        # Seperating the tables
    mars_profile_1 = table_df[0]
    mars_profile = mars_profile_1.rename(columns={0:'Description',1:'Value'}).set_index('Description')
    
    # Second Table comparing Mars to Earth
    mars_vs_earth = table_df[1].set_index('Mars - Earth Comparison')
    

    # Exporting the tables back to html
    marsprofile = mars_profile.to_html()

    marsvsearth = mars_vs_earth.to_html()

    #----------------------------------------------------#
    # Mars Hemispheres
    #----------------------------------------------------#

    browser = open_browser()

    # New URL to retreive the featured image
    img_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # New Browser Option
    img_browser = browser.visit(img_url)

    # Setting up the HTML for images
    img_html = browser.html

    # Setting up Beautiful Soup to obtain images
    img_soup = BeautifulSoup(img_html, 'html.parser')

    # Creating lists to append the data
    title_name = []

    # Setting up a web query
    results = img_soup.find_all('div', class_='description')

    # Iterating through the site to append the lists
    for result in results:
        h3 = result.find('h3').text
        title_name.append(h3)
    

    browser.quit()

    # Creating a dictionary with links to images
    hemisphere_image_urls = [
        {'Title':title_name[0],"image_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    
        {'Title':title_name[1],"image_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},

        {'Title':title_name[2],"image_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},

        {'Title':title_name[3],"image_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"}
    ]

    # Setting up the Mars Dictionary for the Website
    mars_web_page_dict = {}
    mars_web_page_dict['news_title'] = news_title
    mars_web_page_dict['news_body'] = news_p
    mars_web_page_dict['featured_image'] = featured_image
    mars_web_page_dict['mars_facts'] = marsprofile
    mars_web_page_dict['mars_vs_earth']=marsvsearth
    mars_web_page_dict['mars_hemisphere_images_url'] = hemisphere_image_urls
    

    return mars_web_page_dict   










