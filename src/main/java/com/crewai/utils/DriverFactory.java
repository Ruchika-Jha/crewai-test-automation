package com.crewai.utils;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.MutableCapabilities;
import java.net.URL;
import java.net.MalformedURLException;
import io.github.bonigarcia.wdm.WebDriverManager;

public class DriverFactory {
    private static ThreadLocal<WebDriver> driver = new ThreadLocal<>();

    public static WebDriver getDriver() {
        if (driver.get() == null) {
            initializeDriver();
        }
        return driver.get();
    }

    public static void initializeDriver() {
        String browser = System.getProperty("browser", "chrome");
        switch (browser.toLowerCase()) {
            case "firefox": {
                WebDriverManager.firefoxdriver().setup();
                driver.set(new FirefoxDriver());
                break;
            }
            case "browserstack": {
                // BrowserStack credentials from environment variables or system properties
                String username = System.getenv("BROWSERSTACK_USERNAME");
                String accessKey = System.getenv("BROWSERSTACK_ACCESS_KEY");
                String browserstackUrl = "https://" + username + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub";

                MutableCapabilities caps = new MutableCapabilities();
                caps.setCapability("browserName", "chrome");
                caps.setCapability("browserVersion", "latest");

                // Set ChromeOptions for BrowserStack
                ChromeOptions options = new ChromeOptions();
                final java.util.Map<String, Object> chromePrefs = new java.util.HashMap<>();
                chromePrefs.put("credentials_enable_service", false);
                chromePrefs.put("profile.password_manager_enabled", false);
                chromePrefs.put("profile.password_manager_leak_detection", false);
                options.setExperimentalOption("prefs", chromePrefs);

                // Do NOT set headless mode for BrowserStack
                options.addArguments("--disable-gpu");
                options.addArguments("--window-size=1920,1080");

                caps.setCapability(ChromeOptions.CAPABILITY, options);

                // BrowserStack specific options
                java.util.Map<String, Object> bstackOptions = new java.util.HashMap<>();
                bstackOptions.put("os", "Windows");
                bstackOptions.put("osVersion", "10");
                bstackOptions.put("sessionName", "CrewAI Selenium Test");
                caps.setCapability("bstack:options", bstackOptions);

                try {
                    driver.set(new RemoteWebDriver(new URL(browserstackUrl), caps));
                } catch (MalformedURLException e) {
                    throw new RuntimeException("Invalid BrowserStack URL", e);
                }
            
                break;
            }
            default: {
                WebDriverManager.chromedriver().setup();
                ChromeOptions options = new ChromeOptions();
                final java.util.Map<String, Object> chromePrefs = new java.util.HashMap<>();
                chromePrefs.put("credentials_enable_service", false);
                chromePrefs.put("profile.password_manager_enabled", false);
                chromePrefs.put("profile.password_manager_leak_detection", false);
                options.setExperimentalOption("prefs", chromePrefs);

                // Example: add headless mode if specified
                String headless = System.getProperty("headless", "false");
                if (headless.equalsIgnoreCase("true")) {
                    options.addArguments("--headless=new");
                }
                // Example: add custom arguments
                options.addArguments("--disable-gpu");
                options.addArguments("--window-size=1920,1080");
                driver.set(new ChromeDriver(options));
                break;
            }
        }
        driver.get().manage().window().maximize();
    }

    public static void quitDriver() {
        if (driver.get() != null) {
            driver.get().quit();
            driver.remove();
        }
    }
}