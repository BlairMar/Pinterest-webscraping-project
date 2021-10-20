from typing import DefaultDict
from selenium import webdriver
import time
from time import sleep
import urllib.request
import os
from collections import defaultdict



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
        """

        self.category = None
        self.category_image_count = defaultdict(int)
        self.root = root
        self.driver = webdriver.Chrome()
        self.image_set = set()
        self.category_link_dict = []
        self.save_path = None
        
        
    def _get_category_links(self) -> None:
        """Extract the href attribute of each of the categories
        """
        self.driver.get(self.root)
        sleep(2)
        # Get the a list of all the categories
        categories = self.driver.find_elements_by_xpath('//div[@data-test-id="interestRepContainer"]//a')
        # Extract the href
        self.category_link_dict = {i+1:link.get_attribute('href') for i, link in enumerate(categories)}

    def _print_options(self):
        """Print all categories available on the homepage
        """
        print(f"\n The options (Total {len(self.category_link_dict)})  are:")
        for idx, category in self.category_link_dict.items(): #prints all the categories available on the root page
            print(f"\t {idx}: {category.replace('https://www.pinterest.co.uk/ideas/', '').split('/')[0]}")

    def _get_user_input(self):  
        """Let user decide how many and which categories to download
        """
        try:    
            categories_num = int(input(f"\nFrom how many categories do you want to download images?: \n"))
            assert categories_num <= len(self.category_link_dict)
        except: #throws error if user puts in too high number of category 
            raise Exception(f"Input cannot be greater than {len(self.category_link_dict)}.") 
        pass

        print(categories_num)
        self.selected_category = {}
        if categories_num == len(self.category_link_dict):
            self.selected_category = self.category_link_dict
        else:
            print("Which one(s) [Pick number(s)]?: ")
            selected_category = []
            try:
                for i in range(categories_num):
                    choice = int(input(f"{categories_num - i} choices left: "))
                    assert choice < len(self.category_link_dict)
                    self.selected_category[i+1] = self.category_link_dict[choice]
            except:
                raise Exception(f"Input cannot be greater than {len(self.category_link_dict)}.")
            
        print(f"Categories selected: {self.selected_category.values()}")

    def _create_folders(self) -> None:
        """Create corresponding folders to store images of each category
        """
        self.root_save_path = '../data'

        # Create a folder named data to store a folder for each category
        if not os.path.exists(f'{self.root_save_path}'):
                os.makedirs(f'{self.root_save_path}')

        # Create the category folders if they do not already exist
        for category in self.selected_category.values():
            name = category.split('/')[4]
            print(f"Category folder: {name}")
            if not os.path.exists(f'{self.root_save_path}/{name}'):
                os.makedirs(f'{self.root_save_path}/{name}')

    def _extract_links(self) -> None:
        """Move to the page of a category and extract src attribute for the images 
            at the bottom of the page
        """
        self.driver.get(self.root + self.category)
        Y = 10**6   # Amount to scroll down the page   
        sleep(2)

        # Keep scrolling down for a number of times
        for _ in range(2):
            self.driver.execute_script(f"window.scrollTo(0, {Y})")  # Scroll down the page
            sleep(1)
            # Store the link of each image if the page contains the targeted images
            try:
                container = self.driver.find_element_by_xpath('//div[@data-test-id="grid"]//div[@class="vbI XiG"]')
                image_list = container.find_elements_by_xpath('//div[@class="Yl- MIw Hb7"]//img')
                print(f"Number of images successfully extracted: {len(image_list)}")
                self.image_set.update([(self.category, link.get_attribute('src')) for link in image_list])
                print(f"Number of uniques images: {len(self.image_set)}")
            except: 
                print('Some errors occurred, most likely due to no images present')

    def _get_image_source(self, link: str) -> None:
        """Move to the image source page

        Args
        ---------------------
        link: str
        """
        self.driver.get(link)
        sleep(0.5)
        self.src = link

    def _download_image(self, i: int) -> None:
        """Download the image
        Args
        ---------------------
        i: int
        """
        urllib.request.urlretrieve(self.src, 
                                f"{self.root_save_path}/{self.save_path}/{self.save_path}_{i}.jpg")

    def _grab_image_srcs(self) -> None:
        """Get src links for all images
        """
        self._get_category_links()
        self._print_options()
        self._get_user_input()
        self._create_folders()
        
        # Loop through each category
        for category in self.selected_category.values():
            self.category = category.replace('https://www.pinterest.co.uk/ideas/', "")
            self.category_image_count[self.category] = 0
            self._extract_links()

    def _save_all_images(self) -> None: 
        """Download images that are not a profile picture
        """
        for category,link in self.image_set:
            if '75x75' not in link: # Download image if it is not a profile picture
                self.save_path = f'{category.split("/")[0]}'
                self._get_image_source(link)
                self.category_image_count[category] += 1
                self._download_image(self.category_image_count[category])
        self.driver.quit()  # Terminate the webdriver and close all windows

    def get_category_images(self) -> None:
        """Grab all image links, then download all images
        """
        self._grab_image_srcs()
        self._save_all_images()

if __name__ == "__main__":
    pinterest_scraper = PinterestScraper('https://www.pinterest.co.uk/ideas/')
    pinterest_scraper.get_category_images()