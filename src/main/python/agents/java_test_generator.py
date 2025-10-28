import os
from typing import List, Dict

JAVA_PAGE_OBJECT_TEMPLATE = '''
package com.crewai.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;

public class {class_name} extends BasePage {{
    public {class_name}(WebDriver driver) {{
        super(driver);
    }}

    // Add locators and actions here
}}
'''

JAVA_TEST_CLASS_TEMPLATE = '''
package com.crewai.tests;

import com.crewai.pages.{page_class};
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.AfterMethod;

public class {test_class_name} extends BaseTest {{
    private {page_class} page;

    @BeforeMethod
    public void setUpTest() {{
        super.setUp();
        page = new {page_class}(driver);
        driver.get(System.getenv("TEST_WEBSITE_URL"));
    }}

    @AfterMethod
    public void tearDownTest() {{
        super.tearDown();
    }}

    // Add test methods here
}}
'''

import subprocess

def get_locator_for_action(action_text):
    result = subprocess.run(
        ['python', 'src/main/python/agents/locator_suggester.py', action_text, 'no-login'],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if "Suggested locator:" in line:
            # Example: By.ID, "add-to-cart"
            locator = line.split("Suggested locator: ")[1]
            return locator
    return None

def generate_java_page_object(scenario: Dict):
    class_name = scenario['requirement_title'].replace(' ', '') + "Page"
    # For demo, use first test case title as action
    action_text = scenario['test_cases'][0]['title'] if scenario['test_cases'] else "Add to Cart"
    locator = get_locator_for_action(action_text)
    locator_field = ""
    action_method = ""
    if locator:
        # Parse locator type and value
        if locator.startswith("By.ID"):
            locator_type = "By.id"
            locator_value = locator.split(',')[1].strip().strip('"')
            locator_field = f"    private By {action_text.replace(' ', '').lower()} = {locator_type}(\"{locator_value}\");\n"
            action_method = f"    public void {action_text.replace(' ', '').lower()}() {{\n        driver.findElement({action_text.replace(' ', '').lower()}).click();\n    }}\n"
        elif locator.startswith("By.XPATH"):
            locator_type = "By.xpath"
            locator_value = locator.split(',')[1].strip().strip('"')
            locator_field = f"    private By {action_text.replace(' ', '').lower()} = {locator_type}(\"{locator_value}\");\n"
            action_method = f"    public void {action_text.replace(' ', '').lower()}() {{\n        driver.findElement({action_text.replace(' ', '').lower()}).click();\n    }}\n"
    content = JAVA_PAGE_OBJECT_TEMPLATE.format(class_name=class_name)
    # Insert locator and action method
    content = content.replace("// Add locators and actions here", locator_field + action_method)
    file_path = f"src/main/java/com/crewai/pages/{class_name}.java"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)

def generate_java_test_class(scenario: Dict):
    page_class = scenario['requirement_title'].replace(' ', '') + "Page"
    test_class_name = "Test" + scenario['requirement_title'].replace(' ', '')
    content = JAVA_TEST_CLASS_TEMPLATE.format(page_class=page_class, test_class_name=test_class_name)
    file_path = f"src/test/java/com/crewai/tests/{test_class_name}.java"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)

def generate_java_tests(test_scenarios: List[Dict]):
    for scenario in test_scenarios:
        generate_java_page_object(scenario)
        generate_java_test_class(scenario)
