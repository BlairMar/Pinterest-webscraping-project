from selenium import webdriver
import unittest
from src import pinterestScraper
from hypothesis import given
import hypothesis.strategies as st
import random

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
    @given(st.text()) #NOT TESTING ANY INPUTS - AS THERE IS NONE (self isnt an input)
    def setUp(self):   
        '''
        This function is used to set up the scenario for each test
        '''
        self.category = "Animals- animals/925056443165/"    # we will be testing the scraper with these specific attributes:
        self.root = "pinterest.co.uk/"
        self.driver = webdriver.Chrome()
        self.image_set = set()
        self.category_link_list = []
        self.save_path = None
    
    @given(st.text())       # AM I SUPOSED TO DO A FUNCTIONALITY TEST AND A 'GIVEN' TEST FOR EACH FUNCTION? (SO 2 FOR EACH?)
    def test_get_category_links(self):
        '''
        This function is used to test if correct links are retreived
        '''
        actual_links = pinterestScraper.PinterestScraper.get_category_links() 
        hand_picked_links = ['https://www.pinterest.co.uk/ideas/halloween/915794205972/',  #haveto reeneter these before the test?
                  'https://www.pinterest.co.uk/ideas/holidays/910319220330/',
                  'https://www.pinterest.co.uk/ideas/animals/925056443165/']                #ie: ' what the function should output
        for link in actual_links:
            if link == (hand_picked_links[0] or hand_picked_links[1] or hand_picked_links[2]):
                print ('we have collected the correct links')
                break
            else:
                pass 

        x = (type(random.choice(hand_picked_links)))  #im attempting tomake sure that the 'type' of the links we got are the same (ie: theyre both web-element objects)
        y = (type(random.choice(actual_links))) 
        self.assertEqual(x, y)
        #self.assertEqual(self.category_link_list, )   # do i ultimately haveto make ANY test, as long as it shows that the definite output is the same as out output from the function?- YES
    
    @given(st.text()) 
    def test_create_folders(self): # how would we test to see if it creates folders properly?
        '''
        This function is used to test if folders are created properly
        '''
        actual_folders = pinterestScraper.PinterestScraper._create_folders()  #folders made by our class
                                             # maybe the test should be if the object type is a folder
                                             #
                                             # 
        test = random.choice(actual_folders) #picks a folder at random 
        try:
            f = open(test)            #maybe use 'with' statment here - opens and closes file in 1 step 
        except:
            print ('File is not accessible!')
        finally:
            f.close()
        

    @given(st.text())
    def test_extract_links():
        '''
        This function is used to test if correct links are extracted
        '''
        actual_links = pinterestScraper.PinterestScraper.extract_links
        
        pass
    
    @given(st.text())
    def test_get_image_source():
        '''
        This function is used to test if the correct image source is retreived
        '''
        actual_image_source = pinterestScraper.PinterestScraper.get_image_source
        pass
    
    @given(st.text())
    def test_download_images():
        '''
        This funciton is used to test if the images are downloaded properly
        '''    
        pass
    
    @given(st.text())
    def test_get_category_images():
        ''''
        This fucntion is used to test if 
        '''
        pass
    
    @given(st.text())
    def new_function():
        pass



#testing possible inputs :

from hypothesis import given

