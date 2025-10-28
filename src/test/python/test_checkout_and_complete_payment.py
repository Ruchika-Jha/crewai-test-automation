
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.checkout_and_complete_payment_page import CheckoutandCompletePaymentPage
import os
from dotenv import load_dotenv

class TestCheckoutandCompletePayment(unittest.TestCase):
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
        self.page = CheckoutandCompletePaymentPage(self.driver)

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    
    def test_**_proceed_to_checkout_from_cart(self):
        """** Proceed to Checkout from Cart"""
        
        self.page.navigate_to(self.base_url)
        
    
    def test_**_enter_shipping_and_payment_details(self):
        """** Enter Shipping and Payment Details"""
        
        self.page.navigate_to(self.base_url)
        
    
    def test_**_process_payment_and_display_confirmation(self):
        """** Process Payment and Display Confirmation"""
        
        self.page.navigate_to(self.base_url)
        
    
    def test_**_display_order_summary_after_payment(self):
        """** Display Order Summary After Payment"""
        
        self.page.navigate_to(self.base_url)
        
    

if __name__ == '__main__':
    unittest.main()