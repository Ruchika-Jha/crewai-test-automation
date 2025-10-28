package com.crewai.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.util.List;

public class ProductsPage extends BasePage {
    @FindBy(className = "title")
    private WebElement pageTitle;

    @FindBy(className = "inventory_item")
    private List<WebElement> inventoryItems;

    @FindBy(className = "shopping_cart_link")
    private WebElement cartLink;

    @FindBy(css = "[data-test^='add-to-cart']")
    private List<WebElement> addToCartButtons;

    @FindBy(css = ".inventory_item_name")
    private List<WebElement> productNames;

    @FindBy(css = ".inventory_item_price")
    private List<WebElement> productPrices;

    public ProductsPage(WebDriver driver) {
        super(driver);
    }

    public boolean isOnProductsPage() {
        return wait.until(ExpectedConditions.visibilityOf(pageTitle))
                   .getText().equals("Products");
    }

    public void addProductToCart(String productName) {
        for (int i = 0; i < productNames.size(); i++) {
            if (productNames.get(i).getText().equals(productName)) {
                wait.until(ExpectedConditions.elementToBeClickable(addToCartButtons.get(i))).click();
                break;
            }
        }
    }

    public void openCart() {
        wait.until(ExpectedConditions.elementToBeClickable(cartLink)).click();
    }

    public int getNumberOfProducts() {
        return inventoryItems.size();
    }

    public String getProductPrice(String productName) {
        for (int i = 0; i < productNames.size(); i++) {
            if (productNames.get(i).getText().equals(productName)) {
                return productPrices.get(i).getText();
            }
        }
        return null;
    }
}