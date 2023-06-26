import time

from bs4 import BeautifulSoup
import datetime
import DB as db
import pandas as pd


class Fundraiser:

    def __init__(self, conn, driver, FundraiserId):
        sql = "SELECT * FROM Fundraisers WHERE id = {}".format(FundraiserId)
        result = pd.read_sql_query(sql, conn)
        self.title = result["Title"][0]
        self.location = result["Location"][0]
        self.goal = result["Goal"][0]
        self.raised = result["RaisedMoney"][0]
        self.webpage = result["Webpage"][0]
        self.image = result["Image"][0]
        self.organizer = ''
        self.dateCreated = None
        self.nrDonations = 0
        self.desc = ''
        self.nrUpdates = 0
        self.nrComments = 0
        self.nrDonors = None
        self.shares = None
        self.followers = None
        self.scrapeFundraiserData(driver)
        record = (
            self.organizer, self.dateCreated, self.nrDonations, self.desc, self.nrUpdates, self.nrComments,
            self.nrDonors,
            self.shares, self.followers, datetime.datetime.now())
        print(record)
        db.update_fundraiser_record(conn, record, FundraiserId)

    def scrapeFundraiserData(self, driver):
        driver.get(self.webpage)
        # scrolls at the bottom so every element of the page will be loaded
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight,behavior: 'smooth'});")
        time.sleep(2)
        result = BeautifulSoup(driver.page_source, "html.parser")
        try:
            donations = result.find('button', {"data-element-id": "btn_donations"}).text.strip()

            if 'K' in donations:
                self.nrDonations = int(float(donations.replace('K', '')) * 1000)
                print(self.nrDonations)
            else:
                self.nrDonations = int(donations)
                print(self.nrDonations)
        except:
            print("Donations did not load")

        try:
            self.desc = result.find('div', {"class": "o-campaign-story"}).text.strip()
            print(self.desc)
        except:
            print("Description didnt load")

        try:
            self.nrComments = int(
                result.find('div', {"class": "p-campaign-comments"}).find('h2').text.strip().replace('Comments (',
                                                                                                     '').replace(')',
                                                                                                                 ''))
            print(self.nrComments)
        except:
            print("Comments Info didn't load")

        try:
            self.nrUpdates = int(
                result.find('div', {"class": "p-campaign-updates"}).find('h2').text.strip().replace('Updates (',
                                                                                                    '').replace(')',
                                                                                                                ''))
            print(self.nrUpdates)
        except:
            print("Updates didnt load")

        try:
            self.nrDonors = int(result.findAll('span', {"class": "text-stat-value"})[0].text.strip())
            self.shares = int(result.findAll('span', {"class": "text-stat-value"})[1].text.strip())
            self.followers = int(result.findAll('span', {"class": "text-stat-value"})[2].text.strip())
            print(self.nrDonors, self.shares, self.followers)
        except:
            print("Nr Donors, Shares and Followers did not load")

        try:
            organizerStr = result.find('div', {"class": "m-campaign-byline-description"}).text.strip()

            if " is organizing this fundraiser" in organizerStr:
                self.organizer = organizerStr.replace(' is organizing this fundraiser', '').replace('.', '')
                print(self.organizer)
            elif " are organizing this fundraiser" in organizerStr:
                self.organizer = organizerStr.replace(' are organizing this fundraiser', '').replace('.', '')
                print(self.organizer)
        except:
            print("Organizers Error")

        try:
            temp = result.find('span', {"class": "a-created-date"}).text.strip().replace('Created ', '')

            if " days ago" in temp:
                temp = int(temp.replace(" days ago", ""))
                self.dateCreated = (datetime.datetime.now() - datetime.timedelta(temp)).date()
                print(self.dateCreated)
            else:
                self.dateCreated = datetime.datetime.strptime(temp, '%B %d, %Y').date()
                print(self.dateCreated)
        except:
            print("Created Date Error")