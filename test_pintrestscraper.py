from selenium import webdriver
import unittest
from src import pinterestScraper
from hypothesis import strategies as st
from hypothesis import given       
import hypothesis.strategies as st
import random
import requests
from collections import defaultdict



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
            # we will be testing the scraper with these specific attributes:
        self.pinterest_scraper = pinterestScraper.PinterestScraper('https://www.pinterest.co.uk/ideas/') #creating an instance 


        

    def tearDown (self):
        self.pinterest_scraper.driver.close()  #after each unittest, we close the instance of the class

    
    def test_get_category_links(self): # don't use @given here since we dont want to test ALL possible strings, just the string of the categories xpath 
        '''
        This funtion is used to see if a dictionary is created
        '''
        test_dict = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a')
        self.assertIsInstance(test_dict, dict) #test if output is dictionary
    
    # CAN HAVE MULTIPLE TESTS FOR SAME FUNCTION (AS SEPERATE TESTS OVS)
    
    def test_get_category_links(self):
        '''
        This function is used to test if correct links are retreived
        '''
        test_links = pinterestScraper.PinterestScraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a') 
        hand_picked_links = ['https://www.pinterest.co.uk/ideas/halloween/915794205972/',  #haveto reeneter these before the test?
                   'https://www.pinterest.co.uk/ideas/holidays/910319220330/',
                   'https://www.pinterest.co.uk/ideas/animals/925056443165/']                
        
        self.assertTrue(hand_picked_links in test_links)

     #    assert ((test_links.count(hand_picked_links[0])) > 0) and ((test_links.count(hand_picked_links[1])) > 0) and ((test_links.count(hand_picked_links[2])) > 0)
        
        
        # for link in test_links:
        #      if link == (hand_picked_links[0] or hand_picked_links[1] or hand_picked_links[2]):
        #          print ("correct links retreived!")
        #          break
        #      else:
        #         pass 
            

     
    def test_print_options(self):
        '''
        This function tests if the available categories are printed out
        '''
    
        test_available_categories = pinterestScraper.PinterestScraper._print_options('//div[@data-test-id="interestRepContainer"]//a')
        available_categories = ['halloween', 'animals', 'architecture', 'art', 'beauty', 'design', 'diy-and-crafts', 'education', 'electronics', 'event-planning', 'finance', 'food-and-drink', 'lawn-and-garden', 'home-decor', 'mens-fashion', 'quotes', 'tattoos', 'travel', 'vehicles', 'weddings', 'womens-fashion' ]
        error_message = "Failed! did not collect all available categories"
        self.assertIn(enumerate(available_categories), test_available_categories, error_message) 
    

    @given(st.integers().filter(lambda x: x in range(1,23)))                  #should only be able to input 1-22
    def test_get_user_inputs(self):
         '''
         This function tests if the user's inputs can be inputted successfully
         '''
         pass


#      #@given(st.text()) 
#     def test_create_folders(self,directory_path): 
#         '''
#         This function is used to test if folders are created properly
#         '''
#         actual_folders = pinterestScraper.PinterestScraper._create_folders()  
#         test = random.choice(actual_folders) #picks a random folder
#         try:
#             f = open(test)            #maybe use 'with' statment here - opens and closes file in 1 step 
#         except:
#             print ('File is not accessible!')
#         finally:
#             f.close()
        

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
    unittest.main(argv= [''],verbosity=2,exit =False)  # ' run all of the unittests we have defined'
