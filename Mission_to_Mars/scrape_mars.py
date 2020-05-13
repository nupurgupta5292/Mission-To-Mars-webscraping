#Importing Dependancies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

#Function to initialize browser
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # Scraping data from NASA Mars News Site
    browser = init_browser()

    # Declaring empty dictionary to store all Mars data
    mars_data = {}

    # URL for NASA Mars News Site
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest_news = soup.find('div', class_='list_text')

    #print(latest_news)

    news_title = latest_news.a.text
    news_p = latest_news.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_p)
    mars_data['news_title'] = news_title
    mars_data['news_subtitle'] = news_p

    #Closing browser after scraping
    browser.quit()

    #-------------------------------------------------------------------------
    # Scraping data from JPL Mars Space Images - Featured Image
    browser = init_browser()

    # URL for NASA Mars News Site
    url_JPL= 'https://www.jpl.nasa.gov'
    #print(url_JPL+'/spaceimages/?search=&category=Mars')
    browser.visit(url_JPL+'/spaceimages/?search=&category=Mars')

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('div', class_='carousel_items')

    #print(featured_image)

    # To get the full size image, I'll be exporting the 'wallpaper' size url, which is bigger than the 'mediumsize' url that the FULL IMAGE button opens
    image_url = image.article['style']
    #print(featured_image_url)

    # To extract the url from the style element 
    start = image_url.find("url('")
    end = image_url.find("');")

    featured_image_url = image_url[start+len("url('"):end]
    featured_image_url_final = url_JPL + featured_image_url

    # print(featured_image_url_final)
    mars_data['featured_image'] = featured_image_url_final

    # Close the browser after scraping
    browser.quit()

    #---------------------------------------------------------------------------
    # Scraping data from Mars Weather Twitter
    browser = init_browser()

    # URL for Mars Weather Twitter Page
    url_twitter= 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Upon inspecting the Twitter page, we know the tweet text is contained in the 'div' tag with following classes
    # Getting the 'div' section that contains the latest tweet
    try:
        tweet = soup.find('div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o')

        #Getting the span tag that contains the text of the latest tweet (fifth span tag in the above 'div')
        tweet_text = tweet.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[4].text.strip()
        tweet_text = tweet_text.replace('\n', ' ')
        print(tweet_text)

    except:
        tweet_text = 'Latest Tweet on Mars Weather could not be retrieved. Please inspect the HTML code'
        print(tweet_text)
    
    mars_data['temp_tweet'] = tweet_text

    #Closing browser after scrapping
    browser.quit()

    #---------------------------------------------------------------------------
    # Scraping data from Mars Facts Webpage

    #Scraping Mars Facts webpage using .read_html() function from Pandas library
    browser = init_browser()
    url_facts = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(url_facts)
    mars_facts

    #Selecting the right table
    mars_facts_table = mars_facts[0]

    #Renaming columns to make it more meaningful
    mars_facts_table.columns = ['Parameter', 'Value']

    #Setting index to 'Parameter'
    mars_facts_table = mars_facts_table.set_index('Parameter')
    mars_data['mars_facts_table'] = mars_facts_table.to_html()

    #---------------------------------------------------------------------------
    # Scraping data from USGS Astrogeology site

    # URL for SGS Astrogeology site
    url_SGS= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_SGS)

    # Declaring empty list to store image header and image url
    hemisphere_pics = []

    # looping through the four tags and load the data into the empty list
    for i in range (4):
        time.sleep(4)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("h2",class_='title').text
        partial = soup.find("div", class_='downloads')
        #print(partial)
        img_url = partial.find('a')['href']
        #print(img_url)
        post = {"img_title": title, "img_url": img_url}
        hemisphere_pics.append(post)
        browser.back()

    mars_data['hemisphere_pics'] = hemisphere_pics

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
