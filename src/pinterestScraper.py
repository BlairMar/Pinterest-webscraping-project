from selenium import webdriver
import time
from time import sleep
import urllib.request
import os

# Let's define our class
class PinterestScraper:
    def __init__(self, root):
        self.category = None # Animals- animals/925056443165/
        self.root = root #pinterest.co.uk/
        self.driver = webdriver.Chrome()
        self.image_set = set()
        self.category_link_list = []
        self.save_path = None
        # self.image_links = [] Initialize links, so if the user calls for get_image_source, it doesn't throw an error
        
    def get_category_links(self):
        self.driver.get(self.root)
        sleep(2)
        categories = self.driver.find_elements_by_xpath('//div[@data-test-id="interestRepContainer"]//a')
        self.category_link_list = [link.get_attribute('href') for link in categories]

    def create_folders(self):
        path = '..'
        for category in self.category_link_list:
            name = category.split('/')[4]
            print(name)
            if not os.path.exists(f'../{name}'):
                os.makedirs(f'../{name}')
            


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
        # # if False:        
        sleep(2)
        # self.driver.execute_script("document.body.style.zoom='25%'")
        # sleep(2)
        for _ in range(3):
            self.driver.execute_script(f"window.scrollTo(0, {Y})")
            sleep(1)
            try:
                container = self.driver.find_element_by_xpath('//div[@data-test-id="grid"]//div[@class="vbI XiG"]')
                image_list = container.find_elements_by_xpath('//div[@class="Yl- MIw Hb7"]//img')
                # ('//div[@data-test-id="grid"]//div[2]//img')
                print(len(image_list))
                self.image_set.update([link.get_attribute('src') for link in image_list])
                print(len(self.image_set), 'image set')
            except: 
                print('Some error, likely no pics')


        # sleep(5)
        # self.driver.refresh()
        # sleep(5)ß
        # image_list = self.driver.find_elements_by_xpath('//div[@data-test-id="grid"]//div[2]/a')
        # self.links = []
        # for i, item in enumerate(category_list):
        #     self.links.append(item.get_attribute('href'))
        # print(self.links)

    def get_image_source(self, link: str) -> None:
        self.driver.get(link)
        sleep(0.5)
        # self.src = link.get_attribute('src')
        self.src = link

    def download_images(self, i) -> None:
        # filename = self.category.split('/')[0]
        urllib.request.urlretrieve(self.src, f"../{self.save_path}/{self.save_path}_{i}.jpg")

    def get_category_images(self) -> None:
        self.get_category_links()
        self.create_folders()
        for category in self.category_link_list:
            self.category = category.replace('https://www.pinterest.co.uk/ideas/', "")
            self.extract_links()
            self.save_path = f'{self.category.split("/")[0]}'
            for i, link in enumerate(self.image_set):
                if '75x75' not in link:
                    self.get_image_source(link)
                    self.download_images(i)
            self.image_set = set()
        self.driver.quit()

if __name__ == "__main__":
    # # vehicles/918093243960/
    # # animals/925056443165/
    # explorePinterest = ['vehicles/918093243960/', 'animals/925056443165/', 'food-and-drink/918530398158/']
    # explorePinterest = ['animals/925056443165/']
    # for category in explorePinterest:
    #     pinterestScrapper = PinterestScraper(category, 'https://www.pinterest.co.uk/ideas/')
    #     name = category.split('/')[0]
    #     # init_idx = len(os.listdir(r'D:/AiCore-perso/Projects/Pintrest-webscraping-project/data/{}'.format(name)))
    #     # print(init_idx)
    #     # pinterestScrapper.get_category_images(f'D:\AiCore-perso\Projects\Pintrest-webscraping-project\data\{name}', init_idx)
    
    pinterest_scraper = PinterestScraper('https://www.pinterest.co.uk/ideas/')
    # name = 'animals'
    # if not os.path.exists(f'../{name}'):
    #     os.makedirs(f'../{name}')
    # print(pinterest_scraper.src)
    pinterest_scraper.get_category_images()


print(PinterestScraper.extract_links)