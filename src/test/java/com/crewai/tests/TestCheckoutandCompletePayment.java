
package com.crewai.tests;

import com.crewai.pages.CheckoutandCompletePaymentPage;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.AfterMethod;

public class TestCheckoutandCompletePayment extends BaseTest {
    private CheckoutandCompletePaymentPage page;

    @BeforeMethod
    public void setUpTest() {
        super.setUp();
        page = new CheckoutandCompletePaymentPage(driver);
        driver.get(System.getenv("TEST_WEBSITE_URL"));
    }

    @AfterMethod
    public void tearDownTest() {
        super.tearDown();
    }

    // Add test methods here
}
