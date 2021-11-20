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

driver = webdriver.Chrome(ChromeDriverManager().install()) #########
webdriver.Chrome('/Users/danielzakaiem/Downloads/chromedriver')######### added so that now the new chromedriver version is running 



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
        self.pinterest_scraper.driver.close()  #after each unittest, we close the instance of the class




    # def test_get_category_links(self): # don't use @given here since we dont want to test ALL possible strings, just the string of the categories xpath 
    #     '''
    #     This funtion is used to see if a dictionary is created
    #     '''
    #     test_dict = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a')
    #     self.assertIsInstance(test_dict, dict) #test if output is dictionary


        
        
    
    # def test_get_category_links(self):
    #      '''
    #      This function is used to test if correct links are retreived
    #      '''
    #      test_href_links = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a')  # outputs an enumerated dictionary of the href links
        
    #      hand_picked_category_xpaths = ['//*[@id="mweb-unauth-container"]/div/div/div/div[3]/div/a',  #need to get 3 diff href links
    #                                    '//*[@id="mweb-unauth-container"]/div/div/div/div[6]/div/a',
    #                                    '//*[@id="mweb-unauth-container"]/div/div/div/div[9]/div/a']
                                       
    #      hand_picked_category_hrefs = []
    #      for xpath in hand_picked_category_xpaths:
    #          hand_picked_category_hrefs.append(self.pinterest_scraper.driver.find_element_by_xpath(xpath).get_attribute('href'))
    #      counter = 0
    #      for ele in hand_picked_category_hrefs:   
    #         if ele in test_href_links.values():
    #             counter +=1
    #             print(counter)
    #      self.assertEqual(counter, 3) # add self to all asserts



    # def test_print_options(self):
    #     '''
    #     This function tests if the entire method is run
    #     '''
    #     category_link_dict = self.pinterest_scraper._get_category_links('//div[@data-test-id="interestRepContainer"]//a') #using output of last func for input of this function
    #     test_available_categories = self.pinterest_scraper._print_options(category_link_dict) # prints out all options (1:hallowean 2: holiday... just as the scraper classdoes
    #     print (test_available_categories) 
    #     self.assertEqual('success', test_available_categories) # ascertains that the entire function actually ran


    



        

    
    # #new    
    # def test_catgories_to_save_imgs (self):  # ADDED THIS AS A NEW TEST FOR THIS COMMIT   
    #     pass                   

    # #new
    # def test_get_user_input (self):
    #    pass
    

    #new
    # def test_interior_cloud_save_loop (self):
    #     pass
    
    
    #new
    # def test_save_to_cloud_or_local (self):
    #     pass



    # #new
    # def test__initialise_counter_and_local_folders (self):
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
        


    
    #doesnt work
    def test_grab_images_src(self):
        '''
        This function is used to test if the entire run
        '''
        image_source = self.pinterest_scraper._grab_images_src() 
        self.assertEqual (image_source, 'success')                           
    #'//*[@id="mweb-unauth-container"]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div/div/img'
    # https://i.pinimg.com/originals/42/d3/e9/42d3e9b8104d429bfcc2653b42290d1f.jpg  
    
    
#
    
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
