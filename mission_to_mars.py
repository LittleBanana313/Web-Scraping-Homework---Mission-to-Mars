# Import statements and setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def Mars():
    # Chrome driver config
    executable_path = {"executable_path": "/Users/connn/Downloads/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # visit NASA site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Parse HTML resuslts with bsoup
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")

    # inspect
    slide_element.find("div", class_="content_title")

    # find newest news title
    news_title = slide_element.find("div", class_="content_title").get_text()

    # Find the newest paragraph text
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    step_1 = {"Newest title": news_title, "Newest paragraph": news_paragraph}

    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    browser = Browser("chrome", **executable_path)
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    button = img_soup.find_all('button')[1].find_parent()['href']
    button_2 = f'{url}{button}'

    browser = Browser("chrome", **executable_path, headless=False)
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)

    # open Mars Facts site
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[0]

    # render index, set dataframe cols, display
    mars_facts.reset_index(inplace=True)
    mars_facts.columns = ["ID", "Properties", "Mars", "Earth"]
    mars_facts.to_html(classes="table table-striped")

    # visit Mars Hemisphere info site
    browser = Browser("chrome", **executable_path, headless=False)
    url = "https://marshemispheres.com/"
    browser.visit(url)


    img_link_dict = {}
    # Parse the resulting html with soup
    html = browser.html
    img_soup2 = BeautifulSoup(html, 'html.parser')
    # img_soup2
    links = browser.links.find_by_partial_text("Hemisphere Enhanced")
    for index, link in enumerate(links):
        if index > 0:
            browser.back()
            time.sleep(2)
            links = browser.links.find_by_partial_text("Hemisphere Enhanced")
        link = links[index]
        title = link.text
        link.click()
        time.sleep(1)
        inner_html = browser.html
        inner_soup = BeautifulSoup(inner_html, 'html.parser')

        downloads = inner_soup.find_all('div', class_ = 'downloads')

        for download in downloads:
            lis = download.find_all("li")
            for li in lis:
                if "Original" in li.text:
                    partial_link = li.find('a')['href']
                    img_link_dict[title] = f'{url}{partial_link}'

    # to stop automated browser to remain active and shutdown
    browser.quit()


    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": button_2,
        "facts": mars_facts,
        "hemispheres": img_link_dict,
    }
    browser.quit()
    return data

if __name__ == "__main__":
    all_data = Mars()
    print(f'{all_data}')