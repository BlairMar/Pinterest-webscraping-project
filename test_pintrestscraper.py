from selenium import webdriver
import unittest

from webdriver_manager import driver
from src import pinterestScraper
from hypothesis import strategies as st
from hypothesis import given       
import hypothesis.strategies as st
import random
import requests
from collections import defaultdict
import os.path
import time



#ADD TIMEIT TESTS TO SEE HOW LONG EACH METHOD TAKES - PUT IN TEST_CLASS AT START OF EACH METHOD 'IT TOOK .. TO RUN..'


class PinterestScraperTestCase(unittest.TestCase):
    '''
    This class tests each method in the WebScraper class

    Attributes:
        category (str): Category we will be scraping
        root (str): The root URL we will be starting from
        driver (): ChromeDriver
        image_set (): 
        category_link_list (list): A list of links
        save_path (): 
    '''
     
    def setUp(self):   
        '''
        This function is used to set up the scenario for each test
        '''
            # we will be testing the scraper with these specific attributes:(ie:this instance of the class will be getting tested)
        self.pinterest_scraper = pinterestScraper.PinterestScraper('https://www.pinterest.co.uk/ideas/') #creating an instance 
     
        
    def tearDown (self):
        self.pinterest_scraper.driver.close()  #after each unittest, we close the instance of the class

        
    def test_get_category_links(self): # don't use @given here since we dont want to test ALL possible strings, just the string of the categories xpath 
        '''
        This funtion is used to see if a dictionary is created
        '''
        test_dict = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a') # u must refer back to the exact instance of the class like here
        self.assertIsInstance(test_dict, dict) #test if output is dictionary
        
    
    def test_get_category_links(self):
         '''
         This function is used to test if correct links are retreived
         '''
         test_href_links = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a') # outputs an enumerated dictionary of the href links
        
         hand_picked_category_xpaths = ['//*[@id="mweb-unauth-container"]/div/div/div/div[3]/div/a',  #need to get 3 diff href links
                                       '//*[@id="mweb-unauth-container"]/div/div/div/div[6]/div/a',
                                       '//*[@id="mweb-unauth-container"]/div/div/div/div[9]/div/a']
                                       
         hand_picked_category_hrefs = []
         for xpath in hand_picked_category_xpaths:
             hand_picked_category_hrefs.append(self.pinterest_scraper.driver.find_element_by_xpath(xpath).get_attribute('href'))
         counter = 0
         for ele in hand_picked_category_hrefs:   
            if ele in test_href_links.values():
                counter +=1
                print(counter)
         self.assertEqual(counter, 3) # add self to all asserts

         #see how long the function takes to run:
         start = time.time()
         test_href_links = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a')
         end = time.time()
         print (f'It had taken {end - start} seconds to run this method')
        

            

    #     #DONT NEED:
    # def test_print_options(self):
    #       '''
    #       This function tests if the available categories are printed out
    #       '''
    #       category_link_dict = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a') # this is the dictionary we will input (this func needs a dict input)
    #       test_available_categories = self.pinterest_scraper._print_options(category_link_dict) # prints out all options (1:hallowean 2: holiday... just as the scraper classdoes
    #       print (test_available_categories) # this object is a 'Nontype'- how am i supposed to chek if the correct categories are ina  nontype?  HOW DO I MAKE THIS PRINTED OFF WORDS INTO A LIST SO I CAN CHECK IF CORRECT  WORDS ARE IN  THERE?
          
    #       actual_available_categories = ['halloween', 'animals', 'architecture', 'art', 'beauty', 'design', 'diy-and-crafts', 'education', 'electronics', 'event-planning', 'finance', 'food-and-drink', 'lawn-and-garden', 'home-decor', 'mens-fashion', 'quotes', 'tattoos', 'travel', 'vehicles', 'weddings', 'womens-fashion' ]
    #       print (dict(enumerate(actual_available_categories)))
          
                    #.items() splits the dictionary elements into tuples
        #   error_message = "Failed! did not collect all available categories"
        #   self.assertIn(enumerate(actual_available_categories), test_available_categories, error_message) 
        
    # #doesnt work 
    # @given(st.dictionaries)    # Want to solely test which inputs can be used with this function          
    # def test_get_user_input(self):
    #     '''
    #      This function tests if the user's inputs can be inputted successfully
    #     '''
    #     pass


    
    
    
    # def test_create_folders(self): 
    #     '''
    #     This function is used to test if folders can be opneded after created
    #     '''
    #     self.selected_category  = {}  #i think we need selected_category to be the catgeories selcted in the previous method (get_user_input)
    #     test_folders = pinterestScraper.PinterestScraper._create_folders(self, directory_path='/Users/danielzakaiem/Documents/')
    #      #??- this should create folders?
       
    #     testing = 0
    #     if os.path.isfile(test_folders):
    #          print('File exists')
    #          testing += 1
    #     else:
    #          print ('File does not exist')
    #     self.assertEqual(testing, 1) # asserts if file exists


        
        

#     @given(st.text())
#     def test_extract_links(self, container_xpath, elements_xpath):
#         '''
#         This function is used to test if correct src links are extracted
#         '''
#         actual_links = pinterestScraper.PinterestScraper._extract_links
#         test_links = [#grab 3 diffferent ones from the acc page]
#     pass
    
#     @given(st.text())
#     def test_get_image_source(self, link):
#         '''
#         This function is used to test if the correct image source is retreived
#         '''
#         actual_image_source = pinterestScraper.PinterestScraper._get_image_source # need to see wether 'pressing on the src link actually brings us to the root image"
#         response = requests.head(random.choice(actual_image_source))
#         print response.headers.get('content-type')
#         pass
    
#     @given(st.text())
#     def test_download_image(self, i):
#         '''
#         This funciton is used to test if the images are downloaded properly
#         '''    
#         pass
    
#     @given
#     def test_grab_image_srcs(self, container_xpath):
#         pass

#     @given
#     def test_save_all_images(self):
#         pass


#     @given(st.text())
#     def test_get_category_images(self):
#         ''''
#         This fucntion is used to test if 
#         '''
#         pass
    
if __name__ == "__main__":
    unittest.main(argv= [''],verbosity=2,exit =False)  # ' run all of the unittests we have defined
