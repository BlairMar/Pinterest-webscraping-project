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
        self.log = set()
        self.fresh_set = set()
        self.s3_list = []
        # self.current_run_categories = [] made redundant by self.selected_category_names
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
            'categories_container': '//div[@data-test-id="interestRepContainer"]'
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
        # Get the a list of all the categories
        container = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, categories_xpath))
            )
        categories = container.find_elements_by_xpath('.//a')
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

    def _catgories_to_save_imgs(self) -> None:

        get_all = ''
        while get_all != 'N' and get_all != 'Y':
            get_all = input('\nWould you like to download images for all selected categories? Y or N: ').upper()
            if get_all == 'Y':
                for cat_name in self.selected_category_names:
                    self._cat_imgs_to_save[cat_name] = True
            elif get_all == 'N':
                get_some = ''
                while get_some != 'N' and get_some != 'Y':
                    get_some = input('\nWould you like to download images for some of the selected categories? Y or N: ').upper()
                    if get_some == 'Y': 
                        for cat_name in self.selected_category_names:
                            to_save = ''
                            while to_save != 'Y' and to_save != 'N':
                                to_save = input(f'\nDo you wish to save the images for {cat_name}? [Y/N]: ').upper()
                                if to_save == 'Y':
                                    self._cat_imgs_to_save[cat_name] = True
                                elif to_save == 'N':
                                    self._cat_imgs_to_save[cat_name] = False
                                else:
                                    print('\nPlease retry your input. ')
                    elif get_some == 'N':
                        print('\nNo images will be downloaded. ')
                        for cat_name in self.selected_category_names:
                            self._cat_imgs_to_save[cat_name] = False
                    else:
                        print('\nUnrecognised input, please retry.')
            else:
                print('\nPlease re-enter your answer. ')


    def _get_user_input(self, category_link_dict: dict):  
        """Let user decide how many and which categories to download
        
        Args
        ---------------------
        category_link_dict: dict
        """
        try:    
            categories_num = int(input(f"\nHow many categories of images do you wish to grab? 1 to {len(category_link_dict)}: \n"))
            assert categories_num <= len(category_link_dict)
        except:  
            raise Exception(f"\nInput cannot be greater than {len(category_link_dict)}.") 
        pass

        self.selected_category = {}

        if categories_num == len(category_link_dict):
            self.selected_category = category_link_dict
        else:
            try:
                choices = []
                check_list = [str(x+1) for x in range(len(category_link_dict))]
                while len(choices) != categories_num:
                    choices = input(f"\nPlease select your desired categories. Separate your choices by commas: You have {categories_num} choice(s) to make. ")
                    choices = (choices.replace(' ', '')).split(',')
                    print(choices)
                    for choice in choices:
                        if choice not in check_list:
                            choices = []
                            print(f'\nPlease only enter integers in a comma separated list. Values between 1 and {len(category_link_dict)}. ') 
                            break
                    if len(choices) == 0:
                        continue
                    elif len(choices) != categories_num:
                        print('\nPlease only select the predetermined number of choices. ')
                    elif len(set(choices)) != len(choices):
                        print('\nOnly unique categories accepted. ')
                        choices = []
                    elif len(set(choices)) == len(choices) == categories_num:
                        for i, choice in enumerate(choices):
                            choice = int(choice)
                            self.selected_category[i+1] = category_link_dict[choice]
                    else: 
                        print('\nUnknown choice error')            
            except:
                raise Exception(f"\nChoice error 2")

        self.selected_category_names = [category.split('/')[4] for category in self.selected_category.values()]
        print(f"Categories selected: {self.selected_category_names}")

    def _interior_cloud_save_loop(self, remote) -> None or str:

        ''' Defines the interior loop of the cloud save function. Would all have been in one function but I needed to repeat
            this section of code if the user made an error entering their bucket name. 
            
            Arguments: remote 
            
            Returns: "retry" if user made a mistake when entering their bucket name
                      None at all other times '''

        if remote == 'Y':
            # self.to_s3 = True
            self.s3_name = input('\nPlease enter the name of your desired S3 bucket. ')
            go_on = ''
            while go_on != 'Y' and go_on != 'N':
                go_on = input(f'\nYou have enetered {self.s3_name} as your s3 bucket. Is this correct? Y or N: ').upper()
                if go_on == 'Y':
                    all_or_some = ''
                    while all_or_some != 'N' and all_or_some != 'Y':
                        all_or_some = input('\nWould you like to download everything to this bucket? Y or N: ').upper()
                        if all_or_some == 'Y':
                            print('\nAll data will be stored on your s3 bucket. ')
                            self.s3_list = self.selected_category_names
                        elif all_or_some == 'N':
                            print('\nPlease select which of the categories you wish to download to your bucket. ')
                            for cat_name in self.selected_category_names:
                                choice = ''
                                while choice != 'N' and choice != 'Y':
                                    choice = input(f'\nWould you like to download {cat_name} to your bucket? Y or N: ').upper()
                                    if choice == 'Y':
                                        self.s3_list.append(cat_name)
                                        print(f'\n{cat_name} will be downloaded remotely. ')
                                    elif choice == 'N':
                                        print(f'\n{cat_name} will be stored locally. ')
                                    else:
                                        print('\nUnsupported selection, please choose again. ')
                        else:
                           print('\nUnrecognized input, please select again. ')
                elif go_on == 'N':
                    print('\nPlease re-enter the name of your bucket. ')
                    return 'retry'
        elif remote == 'N':
            # self.to_s3 == False
            print('\nAll data will be stored on your local machine. ')
        else:
            print('\nYour selection was not valid, please choose again. ')

    def _save_to_cloud_or_local(self) -> None:

        remote = ''
        while remote != 'N' and remote != 'Y':
            if remote == '':
                remote = input('\nWould you like to save any of your data/images to a remote bucket? Y or N: ').upper()
                remote = self._interior_cloud_save_loop(remote)
                if remote == None:
                    break
            elif remote == 'retry':
                remote = 'Y'
                remote = self._interior_cloud_save_loop(remote)
                if remote == None:
                    break
            else:
                print('\nLoop structure error. Luke you stupid...')

    def _initialise_counter_and_local_folders(self, directory_path) -> None:

        ''' Defines a function which initialises the counter dict with the categories selected for the current run and folders for
            local saves. 
            
            Arguments: directory_path: str 
            
            Returns: None '''

        self.root_save_path = directory_path

        for category in self.selected_category_names:
            self.counter_dict[f'{category}'] = 0
            # Create a folder named data to store a folder for each category
            if not os.path.exists(f'{self.root_save_path}'):
                os.makedirs(f'{self.root_save_path}')
            self.main_dict[f"{category}"] = {}
            if category not in self.s3_list:
                if not os.path.exists(f'{self.root_save_path}/{category}'):
                    print(f"\nCreating local folder : {category}")
                    os.makedirs(f'{self.root_save_path}/{category}')

    def _check_for_logs(self) -> None:

        ''' Defines a function which checks to see where/if there is previous data from which to 
            continue. This would need to read from log.json and recent_saves.json '''

        ''' Something about current list of categories selected
            if any of the categories already have a save point in save log file.
        
            Something about how the save log is appeneded to '''

        if os.path.exists('../data/recent-save-log.json'):
            #[if x in current_cat_list? for x in recent_save.values()]
            # if recent_save.values()
            # current_cat_list 
            with open('../data/recent-save-log.json', 'r') as load:
                recent_saves = json.load(load)
            saves = [key for key in recent_saves if key in self.selected_category_names]
            with open('../data/log.json', 'r') as load:
                contents = json.load(load)
                tuples_content = [(item[0], item[1]) for item in contents]
            if saves:
                print(f'\nWe have detected saved data for the follow categories: {saves}. ')
                # data_loc = [recent_saves[key] for key in saves]
                fresh = ''
                while fresh != 'Y' and fresh != 'N':
                    fresh = input('\nWould you like to add to your existing data? Y or N: ').upper()
                    if fresh == 'Y':
                        self.link_set = set(tuples_content)
                        self.log = set(tuples_content)
                        for cat, href in tuples_content:
                            category = cat.split('/')[0]
                            if category in self.selected_category_names:
                                self.counter_dict[category] += 1
                        for save in saves:
                            if recent_saves[save] == 'local':
                                with open(f'../data/{save}/{save}.json', 'r') as load:
                                    self.main_dict[f'{save}'] = json.load(load)
                            elif recent_saves[save][0] == 'remote':
                                s3_save = recent_saves[save][1]
                                obj = self.s3_client.get_object(
                                    Bucket = s3_save,
                                    Key = (f'pinterest/{save}/{save}.json')
                                ) 
                                self.main_dict[f'{save}'] = json.loads(obj['Body'].read())
                            else: 
                                print('\nSomething fishy going on with the save_log. ')
                    elif fresh == 'N':
                        tuples_content = [item for item in tuples_content if item[0].split('/')[0] not in saves]
                        self.link_set = set(tuples_content)
                        self.log = set(tuples_content)
                        print('\nExisting data will be overwritten if you are saving in the same directory as your last save. ')
                    else:
                        self.link_set = set(tuples_content)
                        print('\nPlease re-enter your input. ')
            else:
                self.link_set = set(tuples_content)
                self.log = set(tuples_content)
                print("Previous saves detected: None relate to this data collection run. ")

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
                print(f"\nNumber of images successfully extracted: {len(link_list)}")
                self.link_set.update([(self.category, link.get_attribute('href')) for link in link_list])
                print(f"\nNumber of uniques images: {len(self.link_set)}")
            except: 
                print('\nSome errors occurred, most likely due to no images present')

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
            if self.category not in self.s3_list:
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
            print('\nImage grab Error. Possible embedded video (youtube).')

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
            print('\nStory image grab error')

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

        # category_link_dict = self._get_category_links('//div[@data-test-id="interestRepContainer"]//a')

        self.fresh_set = self.link_set.difference(self.log)

        for (cat, link) in tqdm(list(self.fresh_set)):
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
        for name in self.selected_category_names:
            if name not in self.s3_list:
                with open(f'{name}/{name}.json', 'w') as loading:
                    json.dump(self.main_dict[f"{name}"], loading)
            else:
                # Changed the upload to s3 as the json file was acting strange, this makes it readable.
                self.s3_client.put_object(
                    Body = json.dumps(self.main_dict[f'{name}']), 
                    Bucket = self.s3_name,
                    Key = f'pinterest/{name}/{name}.json'
                )

    def _create_log(self) -> None:

        ''' Defines a function which creates two logs. One of which logs pages visited as to not repeat
            the other a log of where the most recent save for each category is in order to update the
            most recent save. 
            
            Arguments: None
            
            Returns: None '''
        
        # if dict exists json.load
        if os.path.exists('../data/recent-save-log.json'):
            with open('../data/recent-save-log.json', 'r') as load:
                self.recent_save_dict = json.load(load)
        else:
            self.recent_save_dict = {}

        for category in self.selected_category_names:
            if category in self.s3_list:
                update = ['remote', self.s3_name]
            else:
                update = 'local'
            self.recent_save_dict[category] = update

        with open('../data/log.json', 'w') as log, open('../data/recent-save-log.json', 'w') as save:
            json.dump(list(self.link_set), log)
            json.dump(self.recent_save_dict, save)

    def get_category_data(self) -> None:
        """Grab all image links, then download all images
        """
        category_link_dict = self._get_category_links(self.xpath_dict['categories_container'])
        sleep(0.75)
        self._print_options(category_link_dict)
        self._get_user_input(category_link_dict)
        self._catgories_to_save_imgs()
        self._save_to_cloud_or_local()
        self._initialise_counter_and_local_folders('../data')
        self._check_for_logs()
        self._grab_images_src(n_scrolls=1)
        self._grab_page_data()
        self._data_dump()
        self._create_log()
        print('Done and done!')

if __name__ == "__main__": 

    pinterest_scraper = PinterestScraper('https://www.pinterest.co.uk/ideas/')
    pinterest_scraper.get_category_data()