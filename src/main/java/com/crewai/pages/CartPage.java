package com.crewai.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.util.List;

public class CartPage extends BasePage {
    @FindBy(className = "cart_item")
    private List<WebElement> cartItems;

    @FindBy(css = ".cart_item .inventory_item_name")
    private List<WebElement> itemNames;

    @FindBy(css = ".cart_item .inventory_item_price")
    private List<WebElement> itemPrices;

    @FindBy(id = "checkout")
    private WebElement checkoutButton;

    @FindBy(id = "continue-shopping")
    private WebElement continueShoppingButton;

    @FindBy(css = ".cart_item .cart_quantity")
    private List<WebElement> itemQuantities;

    @FindBy(css = "[data-test^='remove']")
    private List<WebElement> removeButtons;

    public CartPage(WebDriver driver) {
        super(driver);
    }

    public boolean isProductInCart(String productName) {
        return itemNames.stream()
                       .anyMatch(item -> item.getText().equals(productName));
    }

    public void removeProduct(String productName) {
        for (int i = 0; i < itemNames.size(); i++) {
            if (itemNames.get(i).getText().equals(productName)) {
                wait.until(ExpectedConditions.elementToBeClickable(removeButtons.get(i))).click();
                break;
            }
        }
    }

    public void clickCheckout() {
        wait.until(ExpectedConditions.elementToBeClickable(checkoutButton)).click();
    }

    public void continueShopping() {
        wait.until(ExpectedConditions.elementToBeClickable(continueShoppingButton)).click();
    }

    public int getCartItemCount() {
        return cartItems.size();
    }

    public String getProductPrice(String productName) {
        for (int i = 0; i < itemNames.size(); i++) {
            if (itemNames.get(i).getText().equals(productName)) {
                return itemPrices.get(i).getText();
            }
        }
        return null;
    }

    public int getProductQuantity(String productName) {
        for (int i = 0; i < itemNames.size(); i++) {
            if (itemNames.get(i).getText().equals(productName)) {
                return Integer.parseInt(itemQuantities.get(i).getText());
            }
        }
        return 0;
    }
}