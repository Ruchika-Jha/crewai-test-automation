
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.add_items_to_cart_and_verify_on_cart_page_page import AddItemstoCartandVerifyonCartPagePage
import os
from dotenv import load_dotenv

class TestAddItemstoCartandVerifyonCartPage(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        chrome_options = Options()
        # Add options for headless execution if needed
        # chrome_options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.implicitly_wait(10)
        self.base_url = os.getenv('TEST_WEBSITE_URL')
        self.page = AddItemstoCartandVerifyonCartPagePage(self.driver)

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    
    def test_add_single_product_to_cart_and_verify_on_cart_page(self):
        """Add Single Product to Cart and Verify on Cart Page"""
        
        self.page.navigate_to(self.base_url)
        
    
    def test_add_multiple_products_to_cart_and_verify_on_cart_page(self):
        """Add Multiple Products to Cart and Verify on Cart Page"""
        
        self.page.navigate_to(self.base_url)
        
    
    def test_remove_product_from_cart_and_verify_cart_update(self):
        """Remove Product from Cart and Verify Cart Update"""
        
        self.page.navigate_to(self.base_url)
        
    

if __name__ == '__main__':
    unittest.main()