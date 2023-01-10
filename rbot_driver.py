# === Pre-Requisites ===
# pip3 install -U selenium
# pip3 install webdriver-manager
# pip3 install pandas
# pip install pywin32

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

def rhood_driver():
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument("start-maximized");
    OPTIONS.add_argument('--profile-directory=Default')
    OPTIONS.add_argument('--user-data-dir=E:\\robinhood_bot\\chrome_profile');
    # OPTIONS.add_argument('--user-data-dir=C:\\Users\\shaur\\AppData\\Local\\Google\\Chrome\\User Data'); # to use default chrome profile
    # OPTIONS.add_experimental_option("debuggerAddress", "127.0.0.1:8989") # to access already open chrome window
    # OPTIONS.add_argument('headless') # start browser in headless mode
    OPTIONS.add_experimental_option("excludeSwitches", ["enable-logging"])

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=OPTIONS)

def gvoice_driver():
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument("start-maximized");
    OPTIONS.add_argument('--profile-directory=Default')
    OPTIONS.add_argument('--user-data-dir=E:\\robinhood_bot\\gvoice_chrome_profile');
    OPTIONS.add_experimental_option("excludeSwitches", ["enable-logging"])

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=OPTIONS)

rdriver = rhood_driver()
gdriver = gvoice_driver()

def rhood_open(url):
    rdriver.get(url)
    time.sleep(3)

def gvoice_open(url):
    gdriver.get(url)
    time.sleep(5)

def rhood_close():
    rdriver.close()

def gvoice_close():
    gdriver.close()

def driver_close():
    rhood_close()
    gvoice_close()

def get_title(driver):
    return driver.title

def find_element(driver, path):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.presence_of_element_located((By.XPATH,path)))

def get_text(driver, path):
    return find_element(driver, path).text

def click(driver, path):
    find_element(driver, path).click()
    time.sleep(0.25)

def input(driver, path, val):
    ele = find_element(driver, path)
    ele.click()
    ActionChains(driver).move_to_element(ele).send_keys(str(val)).perform()

def take_snapshot(driver, filename):
    driver.save_screenshot(filename)