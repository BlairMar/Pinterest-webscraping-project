from hypothesis.core import TestFunc
from selenium import webdriver     ###########
from webdriver_manager.chrome import ChromeDriverManager #########
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
import unittest
driver = webdriver.Chrome(ChromeDriverManager().install()) 
webdriver.Chrome('/Users/danielzakaiem/Downloads/chromedriver')

import unittest.mock  ######
from unittest.mock import patch########


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
        self.pinterest_scraper = pinterestScraper.PinterestScraper('https://www.pinterest.co.uk/ideas/') #creating an instance with inserting a root 
        
    def tearDown (self):
        self.pinterest_scraper._driver.close()  #after each unittest, we close the instance of the class

    def test_get_category_links_1(self): # don't use @given here since we dont want to test ALL possible strings, just the string of the categories xpath 
        '''
        This funtion is used to see if a dictionary is created
        '''
        test_dict = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a')
        self.assertIsInstance(test_dict, dict) #test if output is dictionary

    def test_get_category_links_2(self):
         '''
         This function is used to test if correct links are retreived
         '''
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


    def test_get_category_links_3 (self):
        '''
        tests if output is corrrct dictionary'''
        
        output = self.pinterest_scraper._get_category_links('//*[@id="mweb-unauth-container"]/div/div/div')
        test = test_href_links = {1: 'https://www.pinterest.co.uk/ideas/thanksgiving/949410256396/',
        2: 'https://www.pinterest.co.uk/ideas/holidays/910319220330/', 
        3: 'https://www.pinterest.co.uk/ideas/animals/925056443165/', 
        4: 'https://www.pinterest.co.uk/ideas/architecture/918105274631/', 
        5: 'https://www.pinterest.co.uk/ideas/art/961238559656/', 
        6: 'https://www.pinterest.co.uk/ideas/beauty/935541271955/', 
        7: 'https://www.pinterest.co.uk/ideas/design/902065567321/', 
        8: 'https://www.pinterest.co.uk/ideas/diy-and-crafts/934876475639/', 
        9: 'https://www.pinterest.co.uk/ideas/education/922134410098/', 
        10: 'https://www.pinterest.co.uk/ideas/electronics/960887632144/', 
        11: 'https://www.pinterest.co.uk/ideas/event-planning/941870572865/', 
        12: 'https://www.pinterest.co.uk/ideas/finance/913207199297/', 
        13: 'https://www.pinterest.co.uk/ideas/food-and-drink/918530398158/', 
        14: 'https://www.pinterest.co.uk/ideas/lawn-and-garden/909983286710/',
        15: 'https://www.pinterest.co.uk/ideas/home-decor/935249274030/', 
        16: 'https://www.pinterest.co.uk/ideas/mens-fashion/924581335376/', 
        17: 'https://www.pinterest.co.uk/ideas/quotes/948192800438/', 
        18: 'https://www.pinterest.co.uk/ideas/tattoos/922203297757/', 
        19: 'https://www.pinterest.co.uk/ideas/travel/908182459161/', 
        20: 'https://www.pinterest.co.uk/ideas/vehicles/918093243960/', 
        21: 'https://www.pinterest.co.uk/ideas/weddings/903260720461/', 
        22: 'https://www.pinterest.co.uk/ideas/womens-fashion/948967005229/'}
        self.assertEqual (output, test)

  
    def test_get_category_links_4(self):
        '''
        This function tests if the entire method is run
        '''
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

     
     #you haveto manually pick 1,4,10 for this test
    def test_get_user_input_1 (self): 
        category_link_dict =  self.pinterest_scraper._get_category_links('//*[@id="mweb-unauth-container"]/div/div/div')
        test_list = self.pinterest_scraper._get_user_input(category_link_dict) #outputs the list of the method - input categories 1,4 and 10 for the test
        list_should_be = ['thanksgiving', 'architecture', 'electronics']   
        self.assertListEqual (test_list, list_should_be)                                                            #so for out test, the output is gonna be[ 'thanksgiving', 'architecture', 'electronics']
                                                                             

# # #new 
#     def test_get_user_input (self): 
     

#         #I WAS WRONG - THE FUNCTION THROWS AN ERROR IF 'THERE IS NOT THE SAME VALUE FOR 'CATEGORY_NUMBER' AND NO OF KEYS IN DICTIONARY
#         # ^ this means i would have to purposelfy type in a number> than no available to see if error comes
#         test_category_link_dict = {1: 'https://www.pinterest.co.uk/ideas/thanksgiving/949410256396/', 2: 'https://www.pinterest.co.uk/ideas/holidays/910319220330/', 3: 'https://www.pinterest.co.uk/ideas/animals/925056443165/', 4: 'https://www.pinterest.co.uk/ideas/architecture/918105274631/', 5: 'https://www.pinterest.co.uk/ideas/art/961238559656/', 6: 'https://www.pinterest.co.uk/ideas/beauty/935541271955/', 7: 'https://www.pinterest.co.uk/ideas/design/902065567321/', 8: 'https://www.pinterest.co.uk/ideas/diy-and-crafts/934876475639/', 9: 'https://www.pinterest.co.uk/ideas/education/922134410098/', 10: 'https://www.pinterest.co.uk/ideas/electronics/960887632144/', 11: 'https://www.pinterest.co.uk/ideas/event-planning/941870572865/', 12: 'https://www.pinterest.co.uk/ideas/finance/913207199297/', 13: 'https://www.pinterest.co.uk/ideas/food-and-drink/918530398158/', 14: 'https://www.pinterest.co.uk/ideas/lawn-and-garden/909983286710/', 15: 'https://www.pinterest.co.uk/ideas/home-decor/935249274030/', 16: 'https://www.pinterest.co.uk/ideas/mens-fashion/924581335376/', 17: 'https://www.pinterest.co.uk/ideas/quotes/948192800438/', 18: 'https://www.pinterest.co.uk/ideas/tattoos/922203297757/', 19: 'https://www.pinterest.co.uk/ideas/travel/908182459161/', 20: 'https://www.pinterest.co.uk/ideas/vehicles/918093243960/', 21: 'https://www.pinterest.co.uk/ideas/weddings/903260720461/', 22: 'https://www.pinterest.co.uk/ideas/womens-fashion/948967005229/', 23: 'https://www.pinterest.co.uk/ideas/thanksgiving/949410256396/'}  
#         test = self.pinterest_scraper._get_user_input(test_category_link_dict) 
#         self.assertRaises(Exception, test)
            
#     # I HAVE FOUND THAT '_get_category_link_dict is (   but i repeated one and added to key 23 just for test purposes):
#    # {1: 'https://www.pinterest.co.uk/ideas/thanksgiving/949410256396/', 2: 'https://www.pinterest.co.uk/ideas/holidays/910319220330/', 3: 'https://www.pinterest.co.uk/ideas/animals/925056443165/', 4: 'https://www.pinterest.co.uk/ideas/architecture/918105274631/', 5: 'https://www.pinterest.co.uk/ideas/art/961238559656/', 6: 'https://www.pinterest.co.uk/ideas/beauty/935541271955/', 7: 'https://www.pinterest.co.uk/ideas/design/902065567321/', 8: 'https://www.pinterest.co.uk/ideas/diy-and-crafts/934876475639/', 9: 'https://www.pinterest.co.uk/ideas/education/922134410098/', 10: 'https://www.pinterest.co.uk/ideas/electronics/960887632144/', 11: 'https://www.pinterest.co.uk/ideas/event-planning/941870572865/', 12: 'https://www.pinterest.co.uk/ideas/finance/913207199297/', 13: 'https://www.pinterest.co.uk/ideas/food-and-drink/918530398158/', 14: 'https://www.pinterest.co.uk/ideas/lawn-and-garden/909983286710/', 15: 'https://www.pinterest.co.uk/ideas/home-decor/935249274030/', 16: 'https://www.pinterest.co.uk/ideas/mens-fashion/924581335376/', 17: 'https://www.pinterest.co.uk/ideas/quotes/948192800438/', 18: 'https://www.pinterest.co.uk/ideas/tattoos/922203297757/', 19: 'https://www.pinterest.co.uk/ideas/travel/908182459161/', 20: 'https://www.pinterest.co.uk/ideas/vehicles/918093243960/', 21: 'https://www.pinterest.co.uk/ideas/weddings/903260720461/', 22: 'https://www.pinterest.co.uk/ideas/womens-fashion/948967005229/', 23: 'https://www.pinterest.co.uk/ideas/thanksgiving/949410256396/'}
    
     

#      #test the entire function runsL
#     def test_get_user_input (self):
#         test_category_link_dict = {1: 'https://www.pinterest.co.uk/ideas/thanksgiving/949410256396/', 2: 'https://www.pinterest.co.uk/ideas/holidays/910319220330/', 3: 'https://www.pinterest.co.uk/ideas/animals/925056443165/', 4: 'https://www.pinterest.co.uk/ideas/architecture/918105274631/', 5: 'https://www.pinterest.co.uk/ideas/art/961238559656/', 6: 'https://www.pinterest.co.uk/ideas/beauty/935541271955/', 7: 'https://www.pinterest.co.uk/ideas/design/902065567321/', 8: 'https://www.pinterest.co.uk/ideas/diy-and-crafts/934876475639/', 9: 'https://www.pinterest.co.uk/ideas/education/922134410098/', 10: 'https://www.pinterest.co.uk/ideas/electronics/960887632144/', 11: 'https://www.pinterest.co.uk/ideas/event-planning/941870572865/', 12: 'https://www.pinterest.co.uk/ideas/finance/913207199297/', 13: 'https://www.pinterest.co.uk/ideas/food-and-drink/918530398158/', 14: 'https://www.pinterest.co.uk/ideas/lawn-and-garden/909983286710/', 15: 'https://www.pinterest.co.uk/ideas/home-decor/935249274030/', 16: 'https://www.pinterest.co.uk/ideas/mens-fashion/924581335376/', 17: 'https://www.pinterest.co.uk/ideas/quotes/948192800438/', 18: 'https://www.pinterest.co.uk/ideas/tattoos/922203297757/', 19: 'https://www.pinterest.co.uk/ideas/travel/908182459161/', 20: 'https://www.pinterest.co.uk/ideas/vehicles/918093243960/', 21: 'https://www.pinterest.co.uk/ideas/weddings/903260720461/', 22: 'https://www.pinterest.co.uk/ideas/womens-fashion/948967005229/'}  
#         test = self.pinterest_scraper._get_user_input(test_category_link_dict)

    #new
    # def test_interior_cloud_save_loop (self):
    #     pass
    
    
    #new
    # def test_save_to_cloud_or_local (self):
    #     pass



   

    # def test_initialise_local_folders (self): #AttributeError: 'PinterestScraper' object has no attribute 'selected_category_names'- yet again- error as the vriable is defined only in the scraper
    #         #^well, this was an error- solution- instead of self.selected_category_names defined as attribute within 
    #         # running the class methods (NOT right at the start), i had taken away self, and placed it as an input to the method 
        
    #     test = self.pinterest_scraper._initialise_local_folders('/Users/danielzakaiem/Downloads', ['Animals']) #have i typed in a correct path?
        
    
    
    
    # def test_initialise_counter (self):
    #     pass

    # def test_delete_redundant_saves (self):
    #     pass

    


    

        
    

    # #new
    # def check_for_logs (self):
    #     pass
    
    
    
    #not needed anymore?
    # def test_create_folders_locally(self): 
    #     '''
    #     This function is used to test if the entire method is run
    #     '''
    #     self.selected_category  = {}  #i think we need selected_category to be the catgeories selcted in the previous method (get_user_input)
    #     test_folders = pinterestScraper.PinterestScraper._create_folders_locally(self, directory_path='/Users/danielzakaiem/Documents/')
    #     self.assertEqual('success', test_folders)
        

    #not needed anymore?
    #doesnt work
    # def test_create_folders(self): 
    #     '''
    #     This function is used to test if folders can be opneded after created
    #     '''
    #     selected_category  = ('https://www.pinterest.co.uk/ideas/halloween/915794205972/', 'https://www.pinterest.co.uk/ideas/holidays/910319220330/')  #lets say we selected 2 categories: 1 and 2
    #     test_folders = pinterestScraper.PinterestScraper._create_folders(self, directory_path='/Users/danielzakaiem/Documents/')
    #      #??- this should create folders?
       
    #     counter = 0      
        
    #     if os.path.isfile(test_folders):
    #         print('File exists')
    #         counter += 1
    #     else:
    #          print ('File does not exist')
    #     self.assertEqual(testing, 1) # asserts if file exists
    #       #see how long the function takes to run:
    #     start = time.time()
    #     self.pinterest_scraper._create_folders(directory_path='/Users/danielzakaiem/Documents/')
    #     end = time.time()
    #     print (f'It had taken {end - start} seconds to run this method')

        
        

    #  #doesnt work?
    # def test_extract_links(self):    
    #     '''
    #     This function is used to test if the entire method is run
    #     '''
        
                           
    #     extracted_links = self.pinterest_scraper._extract_links(container_xpath='//*[@id="mweb-unauth-container"]/div/div', elements_xpath = '//*[@id="mweb-unauth-container"]/div/div/div[8]/div') # lets say we picked category 1(hallowean). container xpath = xpath of all containers on hallowean page. elements x path = popular ideas container
    #     self.assertEqual('success', extracted_links)
        
#doesnt work
    # def test_extract_links(self, container_xpath, elements_xpath):    #when importing this class, does it 'import' variables defined within the class? i dont think so no
    #     '''
    #     This function is used to test if correct src links are extracted
    #     '''
    #     extracted_links = self.pinterest_scraper._extract_links(container_xpath='//*[@id="mweb-unauth-container"]/div/div', elements_xpath = '//*[@id="mweb-unauth-container"]/div/div/div[8]/div')
        
    #     #handpicked for halloween
    #     handpicked_src_1 = self.driver.find_element_by_xpath('//*[@id="mweb-unauth-container"]/div/div/div[8]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[7]/div/div/div/div[1]/a/div/div/div/div/div[1]/img'.get_attribute('src')
    #     handpicked_src_2 = self.driver.find_element_by_xpath('//*[@id="mweb-unauth-container"]/div/div/div[8]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[10]/div/div/div/div[1]/a/div/div/div/div/div[1]/img').get_attribute('src')
        


    
    # #doesnt work
    # def test_grab_images_src(self):
    #     '''
    #     This function is used to test if the entire run
    #     '''
    #     image_source = self.pinterest_scraper._grab_images_src()  # im thinking that the 'select_category" used is only defined locally in the scraper, so cannot be accessed here, unless made into an attribute pf the scraper- since importing the scraper only takes in methods and attributes
    #     self.assertEqual (image_source, 'success')               # 'selected_category' is a varibale defined in the scope of pnly the scraper class? 
    # #'//*[@id="mweb-unauth-container"]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div/div/img'
    # # https://i.pinimg.com/originals/42/d3/e9/42d3e9b8104d429bfcc2653b42290d1f.jpg  
    
    
#

    # def test_grab_title (self):
    #     pass


    
#    #doesnt work
#     def test_download_image(self):
#         '''
#         This funciton is used to test if the entire method is run 
#         '''    
        
#         src = 'https://i.pinimg.com/originals/42/d3/e9/42d3e9b8104d429bfcc2653b42290d1f.jpg' # the func needed an src to run
#         downloaded_images =self.pinterest_scraper._download_image(2)
#         self.assertEqual(downloaded_images, 'success')
    
    #doesnt work
    # @given(st.text())
    # def test_download_image(self, i):
    #     '''
    #     This funciton is used to test if the images are downloaded properly
    #     '''    
    #     pass
    
    #doesnt work
#     @given
#     def test_grab_image_srcs(self, container_xpath):
#         pass


#doesnt work
#     @given
#     def test_save_all_images(self):
#         pass

#doesnt work
#     @given(st.text())
#     def test_get_category_images(self):
#         ''''
#         This fucntion is used to test if 
#         '''
#         pass
    
if __name__ == "__main__":
    unittest.main(argv= [''],verbosity=2,exit =False)   #"run all of the unittests we have defined"
