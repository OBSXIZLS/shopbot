import logging, random
from time import sleep
from bs4 import BeautifulSoup
from playsound import playsound
from selenium import webdriver as wd
#import getpass, imaplib


sound_path = "./notification.mp3" #https://www.youtube.com/watch?v=shu98iwsxek number 15
log_path = "./newegg.log"

#URL = "https://www.newegg.com/p/pl?N=100007709%208000%20601357282"
URL = "https://www.newegg.com/p/pl?N=100007709%208000%20601357282%20601330988%20601346498&PageSize=96&RandomID=142777412614425420210406220418"

CHROME_PATH = "./chromedriver"

logging.basicConfig(filename=log_path, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def setup_browser(URL):
    browser = wd.Chrome(CHROME_PATH)
    browser.maximize_window()
    browser.get(URL)
    #browser.set_window_size(1024,768)
    #browser.save_screenshot("/Users/peter/Desktop/blah.png")

    return browser


def close_popup(browser):
    popup = browser.find_element_by_id("popup-close").click()

def open_tab(browser, URL):
    browser.execute_script("window.open('%s', '_blank')" % URL)
    logging.debug(msg="Opening tab: {URL}")


if __name__ == '__main__':

    playsound(sound_path)
    browser = setup_browser(URL)
    browser.implicitly_wait(10)

    try:
        browser.find_element_by_id("popup-close")
        print("Closing popup via popup-close")
        logging.debug("Closing popup via popup-close")
        close_popup(browser)
    except:
        print("No Pop-up detected")
        logging.debug("No Pop-up detected")

    logging.debug("Driver object initialized.")
    input(
        "Please login to account and press enter.")

    browser.find_element_by_xpath("//label[@class='form-select']/select/option[@value='96']").click()
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    all_items = soup.find("div", {"class" : "items-grid-view"})
    itemQty = len(all_items.findAll("div", {"class": "item-cell"}))
    logging.debug(msg="Watching {itemQty} items")


    for item in all_items.findAll("div", {"class": "item-cell"}):
        logging.debug(msg="{item}")
        itemLink = item.find("a", {"class": "item-title"})['href']
        try:
            itemStatus = item.find("p", {"class": "item-promo"}).text
        except:
            logging.debug(msg="Did not find item-promo: itemStatus is {itemStatus} ")
        if itemStatus == "NONE":
            playsound(sound_path)
            open_tab(browser, itemLink)

    while True:
        for item in all_items.findAll("div", {"class": "item-cell"}):
            itemLink = item.find("a", {"class": "item-title"})['href']
            try:
                itemStatus = item.find("p", {"class": "item-promo"}).text
            except:
                logging.debug(msg="Did not find item-promo: itemStatus is {itemStatus} ")

            if itemStatus == None:
                print(f"{itemStatus} - {itemLink}")
                logging.debug(f"{itemStatus} - {itemLink}")
                open_tab(browser, itemLink)
                logging.debug(f"Opening tab - {itemLink}")
                playsound(sound_path)

            else:
                print(f"{itemStatus} - {itemLink}")
                logging.debug(f"{itemStatus} - {itemLink}")
        sleeptime = random.randint(0,200)
        logging.debug(f"Sleeping for {sleeptime} seconds.")
        sleep(sleeptime)
        browser.refresh()

'''
        if input("Enter q to Quit or enter to loop: ") == 'q':
            browser.close()
            break
        else:
            browser.refresh()

'''

