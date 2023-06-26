"""
GoFundMe Scraping Project
    @author: Fatjon Tushe
    January 2021
    Project For Personal Portfolio
"""

from bs4 import BeautifulSoup
import time
from selenium import webdriver
import DB as db
from Fundraiser import Fundraiser
import pandas as pd


# Scraping Overall Data About The Fundraiser For Reference
def scrapeFirstHandData(conn, driver):
    driver.get("https://www.gofundme.com/discover/medical-fundraiser")
    # scrolls at the bottom so every element of the page will be loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    # for loop to load as many data to fetch
    start_index = 0
    end_index = 11
    for j in range(50):
        elem = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div[2]/a")
        # driver.execute_script("arguments[0].scrollIntoView(true);", elem)
        driver.execute_script("window.scrollTo(0, {});".format(1900))
        time.sleep(2)
        elem.click()
        # work with BS4
        result = BeautifulSoup(driver.page_source, "html.parser")
        # scrape total number of results in the webpage
        fundraisers = result.find_all("div", {"class": "grid-item"})
        for i in range(start_index, end_index):

            try:
                fundraiser_title = ''.join(fundraisers[i].find("div", {"class": "fund-title"}).text.strip().split("'"))
                fundraiser_location = ''.join(
                    fundraisers[i].find("div", {"class": "fund-location"}).text.strip().split("'"))
                fundraiser_webpage = fundraisers[i].find("a", {"class": "fund_tile_card_link"})['href']
                fundraiser_img = fundraisers[i].find("div", {"class": "campaign-tile-img--contain"})["data-original"]
                # collects both goal and raised, change the currency depending on the country!!!
                fundraisers_stats = \
                    fundraisers[i].findAll("div", {"class": "show-for-medium"})[1].text.strip().split("'")[
                        0].replace(" raised of ", '').replace(",", "").split('€')

                if 'M' in fundraisers_stats[2]:
                    fundraiser_goal = int(float(fundraisers_stats[2].replace('M', '')) * 1000000)
                else:
                    fundraiser_goal = int(fundraisers_stats[2])

                if 'M' in fundraisers_stats[1]:
                    fundraiser_raised = int(float(fundraisers_stats[1].replace('M', '')) * 1000000)
                else:
                    fundraiser_raised = int(fundraisers_stats[1])

                record = (
                    fundraiser_title, fundraiser_location, fundraiser_goal, fundraiser_raised, fundraiser_webpage,
                    fundraiser_img)
                print(record)
                try:
                    db.insert_fundraiser_data(conn, record)
                except:
                    print("Database Insertion Error or the item already exist in the database")
            except:
                print("First Hand Data Scraping Error")
        start_index += 12
        end_index += 12


def scrapeSecondHandData(conn, driver):
    df = pd.read_sql_query("SELECT * FROM Fundraisers WHERE Organizer IS NULL OR DateCreated IS NULL OR Timestamp IS "
                           "NULL", conn)
    print(df.head())
    for i in range(0, len(df)):
        f1 = Fundraiser(conn, driver, df["id"][i])


def main():
    conn = db.create_connection()

    chrome_options = webdriver.ChromeOptions()
    # comment out Configs you don't want
    # Chrome doesnt show
    chrome_options.add_argument("--headless")
    # Incognito mode
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        scrapeFirstHandData(conn, driver)
        # scrapeSecondHandData(conn, driver)
    finally:
        if conn:
            conn.close()
            driver.close()


if __name__ == '__main__':
    main()
