from types import MethodDescriptorType
from urllib.request import DataHandler
from hypothesis.core import TestFunc
from selenium import webdriver     ###########
from webdriver_manager.chrome import ChromeDriverManager #########
from webdriver_manager import driver
from src import pinterestScraper
from hypothesis import strategies as st
from hypothesis import given       
import hypothesis.strategies as st
from collections import defaultdict
import unittest
driver = webdriver.Chrome(ChromeDriverManager().install()) 
webdriver.Chrome('/Users/danielzakaiem/Downloads/chromedriver')
import unittest.mock  
from unittest.mock import patch
import os
#TO DO:
#do other tests - like testing space complexity of each method 
#time each Method
#test that error is NOT thrown for certain methods
# neaten up code 
#find out how to automatically input into your unit tests - use 'os.system("type_ur_input")' a line below where you would have to manually type in the terinal!


class PinterestScraperTestCase(unittest.TestCase):
    """
    This class tests each method in the WebScraper class

    Attributes:
        category (str): Category we will be scraping
        root (str): The root URL we will be starting from
        driver (): ChromeDriver
        image_set (): 
        category_link_list (list): A list of links
        save_path (): 
    """
     
    def setUp(self):   
        """
        This function is used to set up the scenario for each test
        """
            # instance that will be getting tested:
        self.pinterest_scraper = pinterestScraper.PinterestScraper(root = 'https://www.pinterest.co.uk/ideas/', category = "thanksgiving/949410256396" )
        
    def tearDown (self):
        self.pinterest_scraper._driver.close()  

    def test_get_category_links_1 (self): 
        """
        This funtion is used to see if a dictionary is created
        """
        test_dict = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a')
        self.assertIsInstance(test_dict, dict) 

    def test_get_category_links_2 (self):
         """
         This function is used to test if correct links are retreived
         """
         test_href_links = self.pinterest_scraper._get_category_links('//*[@id="mweb-unauth-container"]/div/div/div')  # outputs an enumerated dictionary of the href links
        
         hand_picked_category_xpaths = ['//*[@id="mweb-unauth-container"]/div/div/div/div[3]/div/a',  #need to get 3 diff href links
                                       '//*[@id="mweb-unauth-container"]/div/div/div/div[6]/div/a',
                                       '//*[@id="mweb-unauth-container"]/div/div/div/div[9]/div/a']
         hand_picked_category_hrefs = []
         for xpath in hand_picked_category_xpaths:
             hand_picked_category_hrefs.append(self.pinterest_scraper._driver.find_element_by_xpath(xpath).get_attribute('href'))
         counter = 0
         for ele in hand_picked_category_hrefs:   
            if ele in test_href_links.values():
                counter +=1
                print(counter)
         self.assertEqual(counter, 3) # add self to all asserts

  
    def test_get_category_links_4(self):
        """
        This function is used to test if the correct hrefs are placed into the dictionary
        """
        dict_of_hrefs = self.pinterest_scraper._get_category_links('//*[@id="mweb-unauth-container"]/div/div/div') #gives dict output of enumerated hrefs
        handpicked_hrefs = ['https://www.pinterest.co.uk/ideas/thanksgiving/949410256396/',   #which should be in the dictionary
        'https://www.pinterest.co.uk/ideas/holidays/910319220330/',  #maybe instaed of handpicking, make selenium grab them all and make this list?
        'https://www.pinterest.co.uk/ideas/animals/925056443165/', 
        'https://www.pinterest.co.uk/ideas/architecture/918105274631/',
        'https://www.pinterest.co.uk/ideas/art/961238559656/', 
        'https://www.pinterest.co.uk/ideas/beauty/935541271955/',
        'https://www.pinterest.co.uk/ideas/design/902065567321/', 
        'https://www.pinterest.co.uk/ideas/diy-and-crafts/934876475639/', 
        'https://www.pinterest.co.uk/ideas/education/922134410098/', 
        'https://www.pinterest.co.uk/ideas/electronics/960887632144/', 
        'https://www.pinterest.co.uk/ideas/event-planning/941870572865/', 
        'https://www.pinterest.co.uk/ideas/finance/913207199297/',
        'https://www.pinterest.co.uk/ideas/food-and-drink/918530398158/',
        'https://www.pinterest.co.uk/ideas/lawn-and-garden/909983286710/',
        'https://www.pinterest.co.uk/ideas/home-decor/935249274030/', 
        'https://www.pinterest.co.uk/ideas/mens-fashion/924581335376/', 
        'https://www.pinterest.co.uk/ideas/quotes/948192800438/', 
        'https://www.pinterest.co.uk/ideas/tattoos/922203297757/',
        'https://www.pinterest.co.uk/ideas/travel/908182459161/',
        'https://www.pinterest.co.uk/ideas/vehicles/918093243960/',
        'https://www.pinterest.co.uk/ideas/weddings/903260720461/',
        'https://www.pinterest.co.uk/ideas/womens-fashion/948967005229/',
        'https://www.pinterest.co.uk/ideas/thanksgiving/949410256396/']
        list_of_hrefs = [*dict_of_hrefs.values()] #should now judst show the values (hrefs) of that dict^
        counter = 0
        i = 0
        for element in list_of_hrefs:
            category = handpicked_hrefs[i] #start off with categories[0] as category 
            counter += (element.count(category)) # elem.counts(category) should = 1    adds 1 if 'thanksgiving is included in first element in dictionary. output is 1 if it is included
            i += 1 # next time round, we move to see if 'holidays'
        self.assertEqual(counter, 22) 
    

    def test_print_options (self):
        """
        This function is used to test if the entire method is run properly
        """
        category_link_dict = self.pinterest_scraper._get_category_links('//*[@id="mweb-unauth-container"]/div/div/div')
        test = self.pinterest_scraper._print_options(category_link_dict)
        self.assertEqual(test, True)

    
    #makes sure entire mthod is run - haveto manually select all three categories offered (1,4 and 10)
    def test_categories_to_save_imgs (self):
        """
        This function is used to test if the entire method is run properly
        """
        selected_category_names = ['thanksgiving', 'architecture', 'electronics']
        test = self.pinterest_scraper._categories_to_save_imgs(selected_category_names)
        self.assertEqual (test, True)
     
     #you haveto manually pick 1,4,10 for this test
    def test_get_user_input_1 (self):
        """
        This function is used to test if the correct list of values is out-putted
        """
        category_link_dict =  self.pinterest_scraper._get_category_links('//*[@id="mweb-unauth-container"]/div/div/div')
        test_list = self.pinterest_scraper._get_user_input(category_link_dict) #outputs the list of the method - input categories 1,4 and 10 for the test
        os.system("3") ######### - doesnt work?
        os.system ("1,4,10")  ############ 
        list_should_be = ['thanksgiving', 'architecture', 'electronics']   
        self.assertListEqual (test_list, list_should_be)   
    
 
 #makes sure entire method is run - haveto type in RDS details manually
    def test_create_RDS (self):
        """
        This function is used to test if the entire method is run properly
        """
        test = self.pinterest_scraper.create_RDS()
        self.assertEqual(test, True)


#     #not sure what inut should be????
#     # def test_interior_cloud_save_loop (self):
#     #     pass
    
    
    #  # ERROR- LONG TO SEXPLAIN, BUT _interior_cloud_save_loop FUNCTION NEEDS AN INPUT TO BE  self.selected_category_names
    # def test_save_to_cloud_or_local (self):
    #     test = self.pinterest_scraper._save_to_cloud_or_local()
    #     self.assertEqual(test, True)



    def test_initialise_local_folders (self): 
        """
        This function is used to test if the correct folders are created
        """                                                              
        #first we call the command to make the 3 folders:
        self.pinterest_scraper._initialise_local_folders('/Users/danielzakaiem/Downloads', [ 'thanksgiving', 'architecture', 'electronics']) 
        folders_created = ['/Users/danielzakaiem/Downloads/thanksgiving/',  # these are the file paths athat should be created after calling the method
         '/Users/danielzakaiem/Downloads/architecture/',
          '/Users/danielzakaiem/Downloads/electronics/']
        counter = 0
        for folder in folders_created:
          if os.path.isdir(folder):
            print('Folder exists')
            counter += 1
        else:
             print ('Folder does not exist')
        self.assertEqual(counter, 3) 
    
    
    def test_initialise_counter_1 (self):
        """
        This function is used to test if the output is a dictionary
        """
        selected_category_names = [ 'thanksgiving', 'architecture', 'electronics']
        test = self.pinterest_scraper._initialise_counter(selected_category_names)
        self.assertIsInstance(test, dict)

    
     #makes sure that dictionary has the specific keys {'thanksgiving': 0, 'architecture': 0, 'electronics': 0}
    def test_initialise_counter_2 (self):
         """
         This function is used to test if the correct keys are in the out-putted dictionary
         """
         selected_category_names = ['thanksgiving', 'architecture', 'electronics']
         test = self.pinterest_scraper._initialise_counter(selected_category_names) #output should be this dict: {'thanksgiving': 0, 'architecture': 0, 'electronics': 0}
         selected_categories = [ 'thanksgiving', 'architecture', 'electronics']
         counter = 0
         for category in selected_categories:
            if category in test:
                print ("Correct category added")
                counter += 1
            else:
                print ("This is not the category that should have been added!")

         self.assertEqual (counter, 3)
         
            
       
#     # #not sure what inputs are needed
#     # def test_delete_redundant_saves (self):
#     #    test = pinterestScraper._delete_redundant_saves()
#     #    pass 

    

    def check_for_logs (self):
         """
         This function is used to make sure that the entire method is run
         """
         test = self.pinterest_scraper._check_for_logs()
         self.assertEqual(test, True)

    #must manually pick category 1 for this test
    def test_extract_links(self):    
         '''          
         This function is used to test if the entire method is run
         '''
         test = self.pinterest_scraper._extract_links(container_xpath='//*[@id="mweb-unauth-container"]/div/div/div', elements_xpath = '//*[@id="mweb-unauth-container"]/div/div[2]/div[8]/div/div[2]/div/div/div[2]/div/div/div/div[1]',  n_scrolls = 1 ) # lets say we picked category 1( 'thanksgiving'). container xpath = xpath of all containers on 'thanksgiving' page. elements x path = popular ideas container
         self.assertEqual(True, test)
        

#   #doesnt work- attribute error for 'selected_category'
    # def test_grab_images_src(self):
    #      '''
    #      This function is used to test if the entire run
    #      '''
    #      test = self.pinterest_scraper._grab_images_src() 
    #      self.assertEqual (test, True)


#    #doesnt work- try and test if image is downloaded remotely/locally
#     def test_download_image(self):
#         '''
#         This funciton is used to test if the entire method is run 
#         '''    
        
#         src = 'https://i.pinimg.com/originals/42/d3/e9/42d3e9b8104d429bfcc2653b42290d1f.jpg' # the func needed an src to run
#         downloaded_images =self.pinterest_scraper._download_image(2)
#         self.assertEqual(downloaded_images, 'success')
    


    
if __name__ == "__main__":
    unittest.main(argv= [''],verbosity=2,exit =False)   #"run all of the unittests we have defined"


# TO DO:
#test RDS function when user inputs locally 



scraper collects Data
and stores on files made in computer or s3 bucket based on user input 

#categories to saves images : ask if they wanna download any of the images - offers depedning on how many categories they have selected in earlier functions ovs- then dictionary is empty - thereis a dictionary called self.catimages_to_save - which is for all images we will download - the image names will have true or false next to all of them - ones with true will be downloaded 
#savetocloud or loacal : asks if wanna download to s3 bucket- if they say bno- gets saved to local machine- if they say yes- have to type in s3 bucket credentials to it is then saved to the s3 bucket (only works with a public bucket)- then makes a list of categories taht we want to save to the bucket for s_3_list - the vlaues on this will be saved on s3 buckt, the rest which arent on list will be stored locally 
#initialise counter : countes how which pages we have been to in a certain category (in a counter_dict) so that we wont repeat a page in the future- for now, we set all keys to 0 - the dictionary with keys-categories and values- a number wich goes up as u go over more pages in a specific category- this method gives them all values of 0 to start with- these temp files are 
#initialise_local_folders: creating a folder called 'data' (to put all scraped images) unless its being saved to s3 bucket - then  creates temp folder within the data folder based on categories selected (eg: tmp_animals and a temp_hallowean WITHIN THE data folder)
#check_for_logs:
#grab_image_srcs:  same shit that extract_links does - it extracts the src links for the categories selcted - it will scroll down each categoru selected - collecting all hrefs- placing in python set 
#extract_links : so we basically have hrefs for each category saved in a set in python
#grab_page_data: also puts loads of functions together - basically form each href link (in our href set), we grab different data points like 'title', 'description' from each href page AND collects other info like if the - by the end of this method AND data_dump function  - essentially, u end up with all diffferent data points collected in a seperate temprary older per gategory with images downloaded (if you have slected to do so)- note: all the data collected per each href link is given in a json format
# #create_log: creates a new files called 'log.json' - this is used incase people want to run the scraper twice- it'll basically save the hrefs that u already used to u dont revisit (the href page)if run scraper again  and a 'recent-save-log.json: which tells you that if u wanna rerun, itll continue where it left off in scraping the data points - by looking at the temp files for each category and c
#check for logs: makes sure these files exist^
#at end got json files for each category  saved in bucket or locally (whichever u choose)
#then we go to create_RDS: asks if u wanna create a database locally on pgadmin, but u can also choose to do it with an aws database 
#now next steps would be to: run this entire scraper (script) in a docker container (with cron jobs every few weeks) on an EC2 instance 
#w ewill the set up prometheus to monitor the EC2 instance basiclly 'does something'
# so we need to:
# set up prometheus to track EC2 instance:
#pascals is currently running the scraper docker image on his EC2 instance on a cron job 
#so basically set up prometheus to track EC2 on pascals ECS instance - acc do it all urself- connect to ur ec2 insance- by connecting cloudwatch to it, then connecting cloud watch with prometheus 
#basically find a way of makign ec2 instance -make it obuntu 20.04 version when making the instance!- run the docker file on it (with crontab - which makes it run the docker container (our scraper) every 10 minutes- connect prometheus and grafana 
#NOTE: this docker container we have already has all the preset values 
#securecopy image created from gthub (EC2-Ubuntu-20.04) (SO NOT A CONTAINER IN DOCKER, INSTEAD, ITS AN IMAGE AS A FILE) which is in our webscraping folderinto ec2 instance 
