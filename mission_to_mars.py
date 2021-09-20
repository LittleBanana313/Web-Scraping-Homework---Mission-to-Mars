# Import statements and setup
import time

import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser


def scrape_all():
    # Chrome driver config
    executable_path = {'executable_path': '/Users/connn/Downloads/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit NASA site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Parse HTML results with bsoup
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    slide_element = news_soup.select_one('ul.item_list')

    try:
    # find newest news title
        time.sleep(2)
        news_title = slide_element.find('div', class_='content_title').get_text()
    except:
        news_title = 'error here'

    # Find the newest paragraph text
    # news_paragraph = ''
    try:
        time.sleep(2)
        news_paragraph = slide_element.find('div', class_='article_teaser_body').get_text()
    except:
        news_paragraph = 'error here'

    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    button = img_soup.find_all('button')[1].find_parent()['href']
    button_2 = f'{url}{button}'

    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # open Mars Facts site
    try:
        mars_facts = pd.read_html('https://galaxyfacts-mars.com/')[0]

        # render index, set dataframe cols, display
        mars_facts.reset_index(inplace=False)
        # mars_facts.columns = ['ID', 'Properties', 'Mars', 'Earth']
        mars_facts = mars_facts.to_html(classes='table table-striped')

    except:
        mars_facts = ''

    # print(mars_facts)

    # visit Mars Hemisphere info site
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    img_link_list = []
    # Parse the resulting html with soup
    html = browser.html
    img_soup2 = BeautifulSoup(html, 'html.parser')
    # img_soup2
    links = browser.links.find_by_partial_text('Hemisphere Enhanced')
    for index, link in enumerate(links):
        if index > 0:
            browser.back()
            time.sleep(2)
            links = browser.links.find_by_partial_text('Hemisphere Enhanced')
        link = links[index]
        title = link.text
        link.click()
        time.sleep(1)
        inner_html = browser.html
        inner_soup = BeautifulSoup(inner_html, 'html.parser')

        downloads = inner_soup.find_all('div', class_='downloads')

        for download in downloads:
            lis = download.find_all('li')
            for li in lis:
                print(" li.text=",  li.text)
                if 'Sample' in li.text:
                    link_dict = {}
                    link_dict["title"] = title

                    partial_link = li.find('a')['href']
                    print("-------------------------------partial_link=", partial_link)
                    link_dict["img_url"] = f'{url}{partial_link}'
                    img_link_list.append(link_dict)
                    

    # to stop automated browser to remain active and shutdown
    browser.quit()

    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': button_2,
        'facts': mars_facts,
        'hemispheres': img_link_list,
    }

    browser.quit()
    return data


if __name__ == '__main__':
    all_data = scrape_all()
    # print(f'{all_data}')
