package com.crewai.tests;

import com.crewai.pages.LoginPage;
import com.crewai.pages.ProductsPage;
import com.crewai.pages.CartPage;
import com.crewai.utils.ConfigReader;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class ShoppingCartTest extends BaseTest {
    private LoginPage loginPage;
    private ProductsPage productsPage;
    private CartPage cartPage;

    @BeforeMethod
    public void setupPages() {
        loginPage = new LoginPage(driver);
        productsPage = new ProductsPage(driver);
        cartPage = new CartPage(driver);

        driver.get(ConfigReader.getBaseUrl());
        loginPage.login("standard_user", "secret_sauce");
        Assert.assertTrue(productsPage.isOnProductsPage(), "User should be on products page");
    }

    @Test
    public void testAddProductToCart() {
        String productName = "Sauce Labs Backpack";
        productsPage.addProductToCart(productName);
        productsPage.openCart();

        Assert.assertTrue(cartPage.isProductInCart(productName), 
            "Product should be in the cart");
        Assert.assertEquals(cartPage.getProductQuantity(productName), 1,
            "Product quantity should be 1");
    }

    @Test
    public void testRemoveProductFromCart() {
        String productName = "Sauce Labs Bike Light";
        productsPage.addProductToCart(productName);
        productsPage.openCart();

        Assert.assertTrue(cartPage.isProductInCart(productName),
            "Product should be in the cart initially");

        cartPage.removeProduct(productName);
        Assert.assertFalse(cartPage.isProductInCart(productName),
            "Product should not be in the cart after removal");
    }

    @Test
    public void testProductPriceConsistency() {
        String productName = "Sauce Labs Fleece Jacket";
        String priceInProductPage = productsPage.getProductPrice(productName);
        
        productsPage.addProductToCart(productName);
        productsPage.openCart();

        String priceInCart = cartPage.getProductPrice(productName);
        Assert.assertEquals(priceInCart, priceInProductPage,
            "Product price should be consistent between product page and cart");
    }
}