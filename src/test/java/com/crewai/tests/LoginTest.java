package com.crewai.tests;

import com.crewai.pages.LoginPage;
import com.crewai.pages.ProductsPage;
import com.crewai.utils.ConfigReader;
import org.testng.Assert;
import org.testng.annotations.Test;

public class LoginTest extends BaseTest {
    @Test
    public void testSuccessfulLogin() {
        LoginPage loginPage = new LoginPage(driver);
        ProductsPage productsPage = new ProductsPage(driver);

        driver.get(ConfigReader.getBaseUrl());
        loginPage.login("standard_user", "secret_sauce");

        Assert.assertTrue(productsPage.isOnProductsPage(), "User should be redirected to products page after successful login");
    }

    @Test
    public void testLockedOutUser() {
        LoginPage loginPage = new LoginPage(driver);

        driver.get(ConfigReader.getBaseUrl());
        loginPage.login("locked_out_user", "secret_sauce");

        Assert.assertTrue(loginPage.getErrorMessage().contains("Sorry, this user has been locked out"),
                "Should display locked out error message");
    }

    @Test
    public void testInvalidCredentials() {
        LoginPage loginPage = new LoginPage(driver);

        driver.get(ConfigReader.getBaseUrl());
        loginPage.login("invalid_user", "invalid_password");

        Assert.assertTrue(loginPage.getErrorMessage().contains("Username and password do not match"),
                "Should display invalid credentials error message");
    }
}