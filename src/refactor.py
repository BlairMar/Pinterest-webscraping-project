from selenium import webdriver
from time import sleep
import urllib.request
import os
from collections import defaultdict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
import json
# from webdriver_manager.chrome import ChromeDriverManager

"""
Class to perform webscraping on the Pinterest website.
"""
class PinterestScraper:

    def __init__(self, root):
        """
        Initialise the attributes of the class

        Args
        ----------------------------------------------------------------
        root: str \n
                The main page which contains a list of all the
             available categories

        Attributes
        ---------------------------
        category: str \n
        root: str \n
        driver: webdriver object \n
        image_set: list \n
        category_link_list: list \n
        save_path: str \n
        link_set: set \n
        current_dict: dict \n
        main_dict: dict \n
        current_link: str \n
        xpath_dict: dict \n
        """

        self.category = None
        self.category_image_count = defaultdict(int)
        self.root = root
#        self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.image_set = set()
        self.category_link_dict = []
        self.save_path = None
        self.link_set = set()
        self.current_dict = {}
        self.main_dict = {}
        self.counter_dict = {} # A counter dict to order the data we grab from each page.
        self.current_link = ''
        self.xpath_dict = {
            'official_user_container': '//div[@data-test-id="official-user-attribution"]',
            'official_user_element': './/div[@class="tBJ dyH iFc yTZ pBj zDA IZT mWe CKL"]',
            'non_off_user_container': '//div[@data-test-id="user-rep"]',
            'non_off_user_element': './/div[@class="tBJ dyH iFc yTZ pBj zDA IZT mWe"]',
            'tag_container': '//div[@data-test-id="CloseupDetails"]',
            'story_tag_container': '//div[@data-test-id="CloseupMainPin"]'
        }

    def _get_category_links(self, categories_xpath: str) -> dict:
        """Extract the href attribute of each of the categories
        
        Args
        ---------------------
        categories_xpath: str
        
        Return
        ---------------------
        dict: dictionary containing the href of each category
        """
        self.driver.get(self.root)
        sleep(2)
        # Get the a list of all the categories
        categories = self.driver.find_elements_by_xpath(categories_xpath)
        # Extract the href
        self.category_link_dict = {i+1:link.get_attribute('href') for i, link in enumerate(categories)}

        return self.category_link_dict