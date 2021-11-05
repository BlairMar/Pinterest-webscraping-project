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
import tempfile
import boto3 
from tqdm import tqdm

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
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.image_set = set()
        self.category_link_dict = []
        self.save_path = None
        self.link_set = set()
        self.current_dict = {}
        self.main_dict = {}
        self.counter_dict = {} # A counter dict to order the data we grab from each page.
        self.current_link = ''
        self._cat_imgs_to_save = {}
        self.s3_client = boto3.client('s3')
        self.to_s3 = False
        self.xpath_dict = {
            'official_user_container': '//div[@data-test-id="official-user-attribution"]',
            'official_user_element': './/div[@class="tBJ dyH iFc yTZ pBj zDA IZT mWe CKL"]',
            'non_off_user_container': '//div[@data-test-id="user-rep"]',
            'non_off_user_element': './/div[@class="tBJ dyH iFc yTZ pBj zDA IZT mWe"]',
            'tag_container': '//div[@data-test-id="CloseupDetails"]',
            'story_tag_container': '//div[@data-test-id="CloseupMainPin"]',
            'reg_title_element': '//div[@data-test-id="CloseupDetails"]//div[@data-test-id="pinTitle"]/h1/div',
            'h1_title_element': '//div[@data-test-id="CloseupMainPin"]//h1',
            'desc_container': '//div[@data-test-id="CloseupDetails"]//div[@data-test-id="CloseupDescriptionContainer"]',
            'desc_element': './/span[@class="tBJ dyH iFc yTZ pBj zDA IZT swG"]',
            'links_container': '//div[@data-test-id="grid"]//div[@class="vbI XiG"]',
            'links_element': './/div[@class="Yl- MIw Hb7"]/div/div/div/div[1]/a',
            'categories_container': '//div[@data-test-id="interestRepContainer"]//a'
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

    def _print_options(self, category_link_dict: dict):
        """Print all categories available on the homepage
        
        Args
        ---------------------
        category_link_dict: dict
        """
        print(f"\n The options (Total {len(category_link_dict)})  are:")
        for idx, category in self.category_link_dict.items(): # Print all categories available on the route page
            print(f"\t {idx}: {category.replace(self.root, '').split('/')[0]}")

    def _get_user_input(self, category_link_dict: dict):  
        """Let user decide how many and which categories to download
        
        Args
        ---------------------
        category_link_dict: dict
        """
        try:    
            categories_num = int(input(f"\nFrom how many categories do you want to download images?: \n"))
            assert categories_num <= len(category_link_dict)
        except:  
            raise Exception(f"Input cannot be greater than {len(category_link_dict)}.") 
        pass

        print(categories_num)
        self.selected_category = {}
        if categories_num == len(category_link_dict):
            self.selected_category = category_link_dict
        else:
            print("\nWhich one(s) [Pick number(s)]?: ")
            selected_category = []
            try:
                for i in range(categories_num):
                    choice = int(input(f"{categories_num - i} choices left: "))
                    assert choice < len(category_link_dict)
                    self.selected_category[i+1] = category_link_dict[choice]
                    self._catgories_to_save_imgs(category_link_dict[choice])
            except:
                raise Exception(f"Input cannot be greater than {len(self.category_link_dict)}.")
            
        print(f"Categories selected: {self.selected_category.values()}")

    def _catgories_to_save_imgs(self, category):
        to_save = input('\nDo you wish to save the images? [y/n]: ')
        cat_name = category.split('/')[4]
        if to_save == 'y':
            self._cat_imgs_to_save[cat_name] = True
        elif to_save == 'n':
            self._cat_imgs_to_save[cat_name] = False
        else:
            raise Exception("Invalid input.")

    def _save_to_cloud_or_local(self):
        for category in self.selected_category.values():
            name = category.split('/')[4]
            self.main_dict[f"{name}"] = {}
            self.counter_dict[f"{name}"] = 0
        choice = input('\nDo you wish to save the data on AWS S3 (y) or locally (n)? [y/n]: ')
        if choice == 'y':
            self.to_s3 = True
            self.s3_name = input('Name of S3 bucket: ')
            print(self.s3_name, type(self.s3_name))
        elif choice == 'n':
            self.to_s3 = False
            self._create_folders_locally('../data')
        else:
            raise Exception("Invalid input")


    def _create_folders_locally(self, directory_path: str) -> None:
        """Create corresponding folders to store images of each category
        Args
        ---------------------
        directory_path: str
        """
        self.root_save_path = directory_path

        # Create a folder named data to store a folder for each category
        if not os.path.exists(f'{self.root_save_path}'):
                os.makedirs(f'{self.root_save_path}')

        # Create the category folders if they do not already exist
        for category in self.selected_category.values():
            name = category.split('/')[4]
            # self.main_dict[f"{name}"] = {}
            # self.counter_dict[f"{name}"] = 0
            print(f"Category folder: {name}")
            if not os.path.exists(f'{self.root_save_path}/{name}'):
                os.makedirs(f'{self.root_save_path}/{name}')

    def _extract_links(self, container_xpath: str, elements_xpath: str, n_scrolls = 1) -> None:
        """Move to the page of a category and extract src attribute for the images 
            at the bottom of the page
            
        Args
        ---------------------
        container_xpath: str 
        elements_xpath: str
        """
        self.driver.get(self.root + self.category)
        Y = 10**6   # Amount to scroll down the page   
        sleep(2)

        # Keep scrolling down for a number of times
        for _ in range(n_scrolls):
            self.driver.execute_script(f"window.scrollTo(0, {Y})")  # Scroll down the page
            sleep(1)
            # Store the link of each image if the page contains the targeted images
            try:
                container = self.driver.find_element_by_xpath(container_xpath)
                link_list = container.find_elements_by_xpath(elements_xpath)
                print(f"Number of images successfully extracted: {len(link_list)}")
                self.link_set.update([(self.category, link.get_attribute('href')) for link in link_list])
                print(f"Number of uniques images: {len(self.link_set)}")
            except: 
                print('Some errors occurred, most likely due to no images present')

    def _grab_images_src(self, n_scrolls=1) -> None:
        """Get src links for all images
        
        Args
        ---------------------
        None
        """
        
        # Loop through each category
        for category in self.selected_category.values():
            self.category = category.replace(self.root, "")
            self.category_image_count[self.category] = 0
            self._extract_links(self.xpath_dict['links_container'], 
                                self.xpath_dict['links_element'],
                                n_scrolls)

    def _grab_title(self, title_element) -> None:

        ''' Defines a function that grabs the title from a Pinterest page
            and adds it to the key "title" in self.current_dict.
            
            Arguments: title_element
            
            Returns: None '''
        try:
            title_element = self.driver.find_element_by_xpath(title_element)
            self.current_dict["title"] = title_element.get_attribute('textContent')
        except:
            self.current_dict["title"] = 'No Title Data Available'
        
    def _grab_description(self, desc_container, desc_element) -> None:

        ''' Defines a function that grabs the description from a Pinterest page
            and adds it to the key "description" in self.current_dict.
            
            Arguments: desc_container, desc_element
            
            Returns: None '''

        description_container = self.driver.find_element_by_xpath(desc_container)
        try: # Need this try statement to see if the description is present. Other wise it faults if there is no description.
            description_element = WebDriverWait(description_container, 0.5).until(
                EC.presence_of_element_located((By.XPATH, desc_element))
            )
            self.current_dict["description"] = description_element.get_attribute('textContent')
        except:
            self.current_dict["description"] = 'No description available'

    def _grab_user_and_count(self, dict_container, dict_element) -> None:

        ''' Defines a function that grabs the poster name and follower count
            and appends adds them to the keys "poster_name" and "follower_count"
            respectively in self.current_dict.
            
            Arguments: dict_container, dict_element
            
            Returns: None '''
        try:
            container = self.driver.find_element_by_xpath(dict_container)
            poster_element = container.find_element_by_xpath(dict_element)          
            self.current_dict["poster_name"] = poster_element.get_attribute('textContent')
            follower_element =  container.find_elements_by_xpath('.//div[@class="tBJ dyH iFc yTZ pBj zDA IZT swG"]')
            followers = follower_element[-1].get_attribute('textContent')
            # If statement is needed as if there is no associated text I cannot use .split to grab only the value.
            # Do not want the text "followers" on the end to clean the data somewhat.
            if followers == '': # If the element has no associated text, there are no followers. Think this is redunant for official users.
                self.current_dict["follower_count"] = '0'
            else:
                self.current_dict["follower_count"] = followers.split()[0]
        except:
            self.current_dict['Error Grabbing User Info'] = 'Some unknown error ocured when trying to grab user info.'
            print('User Info Error')

    def _grab_tags(self, tag_container) -> None:

        ''' Defines a function that grabs the tags from a Pinterest page
            and adds them to the key "tag_list" in self.current_dict.
        
            Arguments: tag_container
            
            Returns: None '''

        try:
            container = WebDriverWait(self.driver, 0.5).until(
                EC.presence_of_element_located((By.XPATH, f'{tag_container}//div[@data-test-id="vase-carousel"]'))
            )
            tag_elements = container.find_elements_by_xpath('.//div[@data-test-id="vase-tag"]//a')
            self.current_dict["tag_list"] = [tag.get_attribute('textContent') for tag in tag_elements]
        except:
            self.current_dict["tag_list"] = 'No Tags Available'

    def _download_image(self, src: str) -> None:
        """Download the image
        """
        if self._cat_imgs_to_save[self.category]:
            if not self.to_s3:
                urllib.request.urlretrieve(src, 
                f"{self.root_save_path}/{self.category}/{self.category}_{self.counter_dict[self.category]}.jpg")
            else:
                with tempfile.TemporaryDirectory() as tempdir:
                    urllib.request.urlretrieve(src, 
                    f'{tempdir}/{self.category}_{self.counter_dict[self.category]}.jpg')
                    # print(f'{tempdir}/{self.category}_{self.counter_dict[self.category]}.jpg')
                    sleep(0.5)
                    self.s3_client.upload_file(
                        f'{tempdir}/{self.category}_{self.counter_dict[self.category]}.jpg', self.s3_name, 
                        f'pinterest/{self.category}/{self.category}_{self.counter_dict[self.category]}.jpg')

                    sleep(0.5)

    def _grab_image_src(self) -> None:

        ''' Defines a function that grabs the image src from a Pinterest page
            and adds it to the key "image_src" in self.current_dict.
            If there is no image and instead a video, grabs the video src
            and adds it to the key "video_src" in self.current_dict.
            
            Arguments: None
            
            Returns: None '''
        try:
            try: # Need this try statement to see if image in an image or other media type.
                image_element = WebDriverWait(self.driver, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@data-test-id="pin-closeup-image"]//img'))
                )
                self.current_dict["is_image_or_video"] = 'image'
                self.current_dict["image_src"] = image_element.get_attribute('src')
                self._download_image(self.current_dict["image_src"])
            except:
                video_element = self.driver.find_element_by_xpath('//video')
                self.current_dict["is_image_or_video"] = 'video'
                self.current_dict["img_src"] = video_element.get_attribute('poster')
                self._download_image(self.current_dict["img_src"])
                # Cannot get video src as the link doesn't load. Can instead get the video thumbnail.
        except:
            self.current_dict['Error Grabbing img SRC'] = 'Some unknown error occured when trying to grab img src.'
            print('Image grab Error. Possible embedded video (youtube).')

    # Need to look into fixing embedded youtube videos.

    def _grab_story_image_srcs(self) -> None:

        ''' Function in testing. Third page layout (story) that has different html
            tabs to target to get info I need. Should be able to integrate later on
            in to one larger function which pulls for xpath dict. '''
        try: 
            try:
                _ = WebDriverWait(self.driver, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Story Pin image"]'))
                    )
                image_container = self.driver.find_element_by_xpath('//div[@aria-label="Story Pin image"]')
                image = image_container.get_attribute('style')
                if not image:
                    self.current_dict["is_image_or_video"] = 'video(story page format)'
                    video_container = self.driver.find_element_by_xpath('//div[@data-test-id="story-pin-closeup"]//video')
                    self.current_dict["img_src"] = video_container.get_attribute('poster')
                    self._download_image(self.current_dict["img_src"])
                    # This particular case no longer seems useful. Leaving it in place in case it turns out to be useful in larger data_sets.
                else: 
                    self.current_dict["is_image_or_video"] = 'story'
                    self.current_dict["img_src"] = image
                    self._download_image(self.current_dict["img_src"])
                    
                # This will only grab the first couple (4 I believe) images in a story post.
                # Could improve.
            except:
                self.current_dict["is_image_or_video"] = 'story of videos'
                video_container = self.driver.find_element_by_xpath('//div[@data-test-id="story-pin-closeup"]//video')
                self.current_dict["img_src"] = video_container.get_attribute('poster')
                self._download_image(self.current_dict["img_src"])
        except:
            self.current_dict['Error Grabbing img SRC'] = 'Some unknown error occured when grabbing story img src'
            print('Story image grab error')

    def _grab_all_users_and_counts(self) -> None:

        ''' Defines a function that checks if a user is officially recognised or
            a story. If official, runs official-user data grab, if not, runs non-official-user
            data grab or story_grab if a story.
        
            Arguments: None
            
            Returns: None '''

        if (self.driver.find_elements_by_xpath('//div[@data-test-id="official-user-attribution"]')):
            self._grab_title(self.xpath_dict['reg_title_element'])
            self._grab_description(self.xpath_dict['desc_container'], self.xpath_dict['desc_element'])
            self._grab_user_and_count(
                self.xpath_dict['official_user_container'],
                self.xpath_dict['official_user_element']
            )
            self._grab_tags(self.xpath_dict['tag_container'])
            self._grab_image_src()
        elif (self.driver.find_elements_by_xpath('//div[@data-test-id="CloseupDetails"]')):
            self._grab_title(self.xpath_dict['reg_title_element'])
            self._grab_description(self.xpath_dict['desc_container'], self.xpath_dict['desc_element'])
            self._grab_user_and_count(
                self.xpath_dict['non_off_user_container'],
                self.xpath_dict['non_off_user_element']
            )
            self._grab_tags(self.xpath_dict['tag_container'])
            self._grab_image_src()
        else:
            self._grab_title(self.xpath_dict['h1_title_element'])
            self.current_dict["description"] = 'No description available Story format'
            self._grab_user_and_count(
                self.xpath_dict['non_off_user_container'],
                self.xpath_dict['non_off_user_element']
            )
            self._grab_tags(self.xpath_dict['story_tag_container'])
            self._grab_story_image_srcs()

    def _grab_page_data(self) -> None:

        ''' Defines a function which combines all data grabs and loops
            though all page links to grab the data from each page
            
            Arguments: None
            
            Returns: None '''

        # Need to make several sub dicts:
        # Need to append current dict to relevant sub dict.

        category_link_dict = self._get_category_links('//div[@data-test-id="interestRepContainer"]//a')


        for (cat, link) in tqdm(list(self.link_set)):
            self.category = cat.split("/")[0]
            self.counter_dict[f"{self.category}"] += 1
            self.current_dict = {}
            self.current_link = link
            self.driver.get(self.current_link)
            self._grab_all_users_and_counts()
            self.main_dict[f"{self.category}"][f"{self.category}_{self.counter_dict[self.category]}"] = self.current_dict
        
    def _data_dump(self) -> None:

        ''' Defines a function which dumps the compiled dictionary
            to a json file.
            
            Arguments: None
            
            Returns: None '''

        if not os.path.exists('../data'):
            os.mkdir('../data')
        os.chdir('..')
        os.chdir('data')
        for category in self.selected_category.values():
            name = category.split('/')[4]
            if not self.to_s3:
                with open(f'{name}/{name}.json', 'w') as loading:
                    json.dump(self.main_dict[f"{name}"], loading)
            else:
                with tempfile.TemporaryDirectory() as tempdir:
                    with open(f'{tempdir}/{name}.json', 'w') as loading:
                        json.dump(self.main_dict[f"{name}"], loading)
                        self.s3_client.upload_file(f'{tempdir}/{name}.json', self.s3_name, 
                        f'pinterest/{self.category}/{name}.json')

    def get_category_data(self) -> None:
        """Grab all image links, then download all images
        """
        category_link_dict = self._get_category_links(self.xpath_dict['categories_container'])
        sleep(0.75)
        self._print_options(category_link_dict)
        self._get_user_input(category_link_dict)
        # self._create_folders_locally('../data')
        self._save_to_cloud_or_local()
        self._grab_images_src(n_scrolls=1)
        self._grab_page_data()
        self._data_dump()
        self.driver.quit()

    # Things that need work.
    # Find a way to combine grab_image_src for story style and regular.
    # Grab embedded youtube vids.

if __name__ == "__main__":
    pinterest_scraper = PinterestScraper('https://www.pinterest.co.uk/ideas/')
    pinterest_scraper.get_category_data()