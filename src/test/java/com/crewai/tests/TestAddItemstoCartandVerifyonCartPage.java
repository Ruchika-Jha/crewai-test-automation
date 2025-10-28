
package com.crewai.tests;

import com.crewai.pages.AddItemstoCartandVerifyonCartPagePage;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.AfterMethod;

public class TestAddItemstoCartandVerifyonCartPage extends BaseTest {
    private AddItemstoCartandVerifyonCartPagePage page;

    @BeforeMethod
    public void setUpTest() {
        super.setUp();
        page = new AddItemstoCartandVerifyonCartPagePage(driver);
        driver.get(System.getenv("TEST_WEBSITE_URL"));
    }

    @AfterMethod
    public void tearDownTest() {
        super.tearDown();
    }

    // Add test methods here
}
