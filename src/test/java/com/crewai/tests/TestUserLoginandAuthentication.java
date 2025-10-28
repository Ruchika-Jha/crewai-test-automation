
package com.crewai.tests;

import com.crewai.pages.UserLoginandAuthenticationPage;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.AfterMethod;

public class TestUserLoginandAuthentication extends BaseTest {
    private UserLoginandAuthenticationPage page;

    @BeforeMethod
    public void setUpTest() {
        super.setUp();
        page = new UserLoginandAuthenticationPage(driver);
        driver.get(System.getenv("TEST_WEBSITE_URL"));
    }

    @AfterMethod
    public void tearDownTest() {
        super.tearDown();
    }

    // Add test methods here
}
