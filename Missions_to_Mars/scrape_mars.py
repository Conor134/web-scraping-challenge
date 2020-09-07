# Import Dependecies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# initialise browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    final_mars_data = {}

    # NASA News
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    news_title = news_soup.find_all('div', class_='content_title')[1].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    ## JPL Mars Space Images - Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    # Click on 'FULL IMAGE'
    browser.click_link_by_partial_text('FULL IMAGE')

    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    # Go to 'more info'
    browser.click_link_by_partial_text('more info')

    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    main_url = 'https://www.jpl.nasa.gov'

    # Scrape the URL
    large_img_url = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = main_url + large_img_url

    ## Scraping Mars data with Pandas
    data_url = "https://space-facts.com/mars/"

    tables = pd.read_html(data_url)
    tables

    mars_data_df = tables[0]
    mars_data_df.columns = ['Description', 'Value']
    mars_data_df.set_index('Description', inplace=True)
    mars_html_table = mars_data_df.to_html('table.html')

    ## Mars Hemispheres
    browser.visit(hemispheres_url)
    html = browser.html

    hemisphere_image_urls = []
    hems_main_url = 'https://astrogeology.usgs.gov'

    # Parse HTML with Beautiful Soup

    hem_soup = BeautifulSoup(html, 'html.parser')

    hemispheres = hem_soup.find_all("div", class_="item")


    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        
        next_image_url = hemisphere.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hems_main_url  + next_image_url)
        
        html = browser.html
        
        hem_soup = BeautifulSoup( html, 'html.parser')
        
        image_url = hems_main_url + hem_soup.find('img', class_='wide-image')['src']
        
        hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})


            
        

    final_mars_data = {
    "news_title": news_title,
    "news_paragraph": news_p,
    "featured_image_url": featured_image_url,
    "mars_facts": mars_data_df,
    "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return final_mars_data  