from selenium import webdriver
import time
from time import sleep
import urllib.request
import os

# Let's define our class
class PinterestScraper:
    def __init__(self, category, root):
        self.category = category # Animals- animals/925056443165/
        self.root = root #pinterest.co.uk/ideas/
        self.driver = webdriver.Chrome()
        self.links = [] # Initialize links, so if the user calls for get_image_source, it doesn't throw an error
        
#     def extract_links(self) -> None:
#         self.driver.get(self.root + self.category)
#         category_list = self.driver.find_elements_by_xpath('//div[@class="jzS un8 P9E"]')
#         print(len(category_list))
#         self.links = []
# #         for i, item in enumerate(category_list):
# #             if i == len(category_list) - 2:
# # #                print(item)
# #             #    a_tag_list = item.find_elements_by_xpath('//a[@class="Wk9 xQ4 CCY czT ho- kVc"]')
# # #               self.links.append(item.find_elements_by_xpath('.//a').get_attribute('href'))
# #                 self.links = item.find_elements_by_xpath('.//a')
# #                print(a_tag_list)
#             #    for j in a_tag_list:
#             #        self.links.append(j.get_attribute('href'))
                   
#         print(self.links)
        

#     def get_image_source(self, link: str) -> None:
#         self.driver.get(link)
#         time.sleep(0.5)
#         self.src = self.driver.find_element_by_xpath('//img[@class="hCL kVc L4E MIw"]').get_attribute('src')
# #now that we have all links to the images:
#     def download_images(self, i) -> None:
#         urllib.request.urlretrieve(self.src, f"Animals/{self.category}_{i}.jpg")
    
#     def get_category_images(self):
#         self.extract_links()
#         for i, link in enumerate(self.links):
#             self.get_image_source(link)
#             self.download_images(i)
#         self.links = []

    def extract_links(self) -> None:
        self.driver.get(self.root + self.category)
        Y = 10**6

        self.driver.execute_script(f"window.scrollTo(0, {Y});")
        sleep(10)
        # if False:        
        #     self.driver.execute_script("document.body.style.zoom='25%'")
        sleep(15)
        category_list = self.driver.find_elements_by_xpath('//div[@data-test-id="grid"]//div[2]/a')
        self.links = []
        for i, item in enumerate(category_list):
            self.links.append(item.get_attribute('href'))
        print(self.links)

    def get_image_source(self, link: str) -> None:
        self.driver.get(link)
        sleep(0.5)
        self.src = self.driver.find_element_by_xpath('//div[@class="XiG zI7 iyn Hsu"]/img').get_attribute('src')

    def download_images(self, i, save_path) -> None:
        filename = self.category.split('/')[0]
        urllib.request.urlretrieve(self.src, f"{save_path}/{filename}_{i}.jpg")
    
    def get_category_images(self, save_path: str, offset: int) -> None:
        self.extract_links()
        for i, link in enumerate(self.links):
            self.get_image_source(link)
            self.download_images(i + offset, save_path)
        self.links = []
        self.driver.quit()

if __name__ == "__main__":
    # vehicles/918093243960/
    # animals/925056443165/
    explorePinterest = ['vehicles/918093243960/', 'animals/925056443165/', 'food-and-drink/918530398158/']
    explorePinterest = ['food-and-drink/918530398158/']
    for category in explorePinterest:
        pinterestScrapper = PinterestScraper(category, 'https://www.pinterest.co.uk/ideas/')
        name = category.split('/')[0]
        init_idx = len(os.listdir(r'D:/AiCore-perso/Projects/Pintrest-webscraping-project/data/{}'.format(name)))
        print(init_idx)
        pinterestScrapper.get_category_images(f'D:\AiCore-perso\Projects\Pintrest-webscraping-project\data\{name}', init_idx)
    