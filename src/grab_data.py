from numpy import empty
from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
import urllib.request
import os
import json
from pinterestScraper import PinterestScraper

class PinterestScraperExtra(PinterestScraper):

    def __init__(self):
        self.category = 'animals/925056443165/'
        self.root =  'https://www.pinterest.co.uk/ideas/'
        self.driver = webdriver.Chrome()
        self.link_set = set()
        # self.category_link_list = []
        # self.save_path = None
        self.current_dict = {}
        self.main_dict = {}
        self.current_link = ''
        self.xpath_dict = {
            'official_user_container': '//div[@data-test-id="official-user-attribution"]',
            'official_user_element': './/div[@class="tBJ dyH iFc yTZ pBj zDA IZT mWe CKL"]',
            'non_off_user_container': '//div[@data-test-id="CloseupUserRep"]//div[@data-test-id="user-rep"]',
            'non_off_user_element': './/div[@class="tBJ dyH iFc yTZ pBj zDA IZT mWe"]'
        }
        # self.image_links = [] Initialize links, so if the user calls for get_image_source, it doesn't throw an error
        

    # Need to make a function that goes to the pages and grabs all info from them
    # This includes tags, poster, number of followers, etc and puts them in a json file
    # Json file of the same name as the image that is being saved like animal_1 etc...
    # In order to do this I need to be able to go only to the page that we need to go to
    # Currently it grabs images, including profile pics. Need to change this to go to page
    # Then grab the images.

    # Start by modifying current function that grabs the image source and only grab the https:
    # Done

    def extract_links(self) -> None:
        self.driver.get(self.root + self.category)
        Y = 10**6
        # # if False:        
        sleep(2)
        # self.driver.execute_script("document.body.style.zoom='25%'")
        # sleep(2)
        for _ in range(1):
            self.driver.execute_script(f"window.scrollTo(0, {Y})")
            sleep(1)
            try:
                container = self.driver.find_element_by_xpath('//div[@data-test-id="grid"]//div[@class="vbI XiG"]')
                link_list = container.find_elements_by_xpath('//div[@class="Yl- MIw Hb7"]/div/div/div/div[1]/a')
                print(len(link_list))
                self.link_set.update([link.get_attribute('href') for link in link_list])
                print(len(self.link_set), 'link set')
            except: 
                print('Some error, likely no <a> tag')

    def _grab_tags(self) -> None:

        ''' Defines a function that grabs the tags from a Pinterest page
            and adds them to the key "tag_list" in self.current_dict.
        
            Arguments: None
            
            Returns: None '''

        tag_container = self.driver.find_element_by_xpath('//div[@data-test-id="CloseupDetails"]//div[@data-test-id="vase-carousel"]')
        tag_elements = tag_container.find_elements_by_xpath('.//div[@data-test-id="vase-tag"]//a')
        tag_text_list = [tag.get_attribute('textContent') for tag in tag_elements]
        self.current_dict["tag_list"] = tag_text_list

    def _grab_title(self) -> None:

        ''' Defines a function that grabs the title from a Pinterest page
            and adds it to the key "title" in self.current_dict.
            
            Arguments: None
            
            Returns: None '''

        title_container = self.driver.find_element_by_xpath('//div[@data-test-id="CloseupDetails"]//div[@data-test-id="pinTitle"]')
        title_element = title_container.find_element_by_xpath('./h1/div')
        title_text = title_element.get_attribute('textContent')
        self.current_dict["title"] = title_text

    def _grab_all_users_and_counts(self) -> None:

        ''' Defines a function that checks if a user is officially recognised
            If official, runs official-user data grab, if not, runs non-official-user
            data grab .
        
            Arguments: None
            
            Returns: None '''

        if not (self.driver.find_elements_by_xpath('//div[@data-test-id="official-user-attribution"]')):
            self._grab_user_and_count(
                self.xpath_dict['non_off_user_container'],
                self.xpath_dict['non_off_user_element']
            )
        else:
            self._grab_user_and_count(
                self.xpath_dict['official_user_container'],
                self.xpath_dict['official_user_element']
            )

    def _grab_user_and_count(self, dict_container, dict_element) -> None:

        ''' Defines a function that grabs the poster name and follower count
            and appends adds them to the keys "poster_name" and "follower_count"
            respectively in self.current_dict.
            
            Arguments: dict_container, dict_element
            
            Returns: None '''

        container = self.driver.find_element_by_xpath(dict_container)
        poster_element = container.find_element_by_xpath(dict_element)          
        poster_name = poster_element.get_attribute('textContent')
        self.current_dict["poster_name"] = poster_name
        follower_element =  container.find_elements_by_xpath('.//div[@class="tBJ dyH iFc yTZ pBj zDA IZT swG"]')
        followers = follower_element[-1].get_attribute('textContent')
        # If statement is needed as if there is no associated text I cannot use .split to grab only the value.
        # Do not want the text "followers" on the end to clean the data somewhat.
        if followers == '': # If the element has no associated text, there are no followers. Think this is redunant for official users.
            self.current_dict["follower_count"] = '0'
        else:
            follower_count = followers.split()[0]
            self.current_dict["follower_count"] = follower_count
    
    def _grab_description(self) -> None:

        ''' Defines a function that grabs the description from a Pinterest page
            and adds it to the key "description" in self.current_dict.
            
            Arguments: None
            
            Returns: None '''

        description_container = self.driver.find_element_by_xpath('//div[@data-test-id="CloseupDetails"]//div[@data-test-id="CloseupDescriptionContainer"]')
        try: # Need this try statement to see if the description is present. Other wise it faults if there is no description.
            description_element = WebDriverWait(description_container, 0.5).until(
                EC.presence_of_element_located((By.XPATH, './/span[@class="tBJ dyH iFc yTZ pBj zDA IZT swG"]'))
            )
            description_text = description_element.get_attribute('textContent')
            self.current_dict["description"] = description_text
        except:
            self.current_dict["description"] = 'No description available'

    def _grab_image_src(self) -> None:

        ''' Defines a function that grabs the image src from a Pinterest page
            and adds it to the key "image_src" in self.current_dict.
            If there is no image and instead a video, grabs the video src
            and adds it to the key "video_src" in self.current_dict.
            
            Arguments: None
            
            Returns: None '''

        try: # Need this try statement to see if image in an image or other media type.
            image_element = WebDriverWait(self.driver, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-test-id="pin-closeup-image"]//img'))
            )
            image_src = image_element.get_attribute('src')
            self.current_dict["is_image_or_video"] = 'image'
            self.current_dict["image_src"] = image_src
        except:
            video_element = self.driver.find_element_by_xpath('//video')
            video_thumbnail = video_element.get_attribute('poster')
            # Cannot get video src as the link doesn't load. Can instead get the video thumbnail.
            self.current_dict["is_image_or_video"] = 'video'
            self.current_dict["video_thumbnail_src"] = video_thumbnail


    def grab_page_data(self) -> None:

        ''' Defines a function which combines all data grabs and loops
            though all page links to grab the data from each page
            
            Arguments: None
            
            Returns: None '''

        for i, link in enumerate(list(self.link_set)):
            self.current_dict = {}
            self.current_link = link
            self.driver.get(self.current_link)
            self._grab_title()
            self._grab_description()
            self._grab_all_users_and_counts()
            self._grab_tags()
            self._grab_image_src()
            self.main_dict[f"animal_pic_{i+1}"] = self.current_dict
        
    def data_dump(self) -> None:

        ''' Defines a function which dumps the compiled dictionary
            to a json file.
            
            Arguments: None
            
            Returns: None '''

        if not os.path.exists('../data'):
            os.mkdir('../data')
        os.chdir('..')
        os.chdir('data')
        with open('json_data_dict.json', 'w') as loading:
            json.dump(self.main_dict, loading)

    # TO DO
    # See how to grab the wanted image from each page.
    # Link to external source is a button, cannot grab href unless I visit each page. Sort out later if needed.

if __name__ == "__main__":

    test = PinterestScraperExtra()

    test.extract_links()
    test.grab_page_data()
    test.data_dump()