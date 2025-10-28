from crewai import Agent
from typing import List, Dict
import os
from dotenv import load_dotenv
from jinja2 import Template

class TestAutomationGenerator:
    def __init__(self):
        load_dotenv()
        self.test_url = os.getenv('TEST_WEBSITE_URL')

    def create_agent(self):
        return Agent(
            role='Test Automation Generator',
            goal='Generate Selenium test automation scripts from test scenarios',
            backstory="""You are an expert in creating automated test scripts using 
            Selenium WebDriver. You convert test scenarios into executable test cases 
            following best practices and page object model pattern.""",
            tools=[self.generate_test_automation],
            verbose=True
        )

    def generate_test_automation(self, test_scenarios: List[Dict]) -> bool:
        """
        Generate Selenium test automation scripts from test scenarios
        
        Args:
            test_scenarios (List[Dict]): List of test scenarios to automate
            
        Returns:
            bool: True if generation was successful, False otherwise
        """
        try:
            for scenario in test_scenarios:
                self._generate_page_objects(scenario)
                self._generate_test_class(scenario)
            return True
        except Exception as e:
            print(f"Error generating test automation: {str(e)}")
            return False

    def _generate_page_objects(self, scenario: Dict):
        """
        Generate page object classes for the test scenario
        
        Args:
            scenario (Dict): Test scenario details
        """
        # Template for page object class
        page_object_template = Template('''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class {{ class_name }}:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    {% for element in elements %}
    # {{ element.description }}
    {{ element.name }}_locator = (By.{{ element.by }}, "{{ element.value }}")
    
    def {{ element.name }}(self):
        return self.wait.until(
            EC.presence_of_element_located(self.{{ element.name }}_locator)
        )
    {% endfor %}
    
    {% for action in actions %}
    def {{ action.name }}(self{% if action.params %}, {{ action.params }}{% endif %}):
        """{{ action.description }}"""
        {{ action.implementation }}
    {% endfor %}
''')

        # Extract page elements and actions from test cases
        elements = []
        actions = []
        
        # Add common actions
        actions.append({
            'name': 'navigate_to',
            'description': 'Navigate to the page',
            'params': 'url',
            'implementation': 'self.driver.get(url)'
        })

        # Generate page object content
        page_object_content = page_object_template.render(
            class_name=f"{scenario['requirement_title'].replace(' ', '')}Page",
            elements=elements,
            actions=actions
        )

        # Save the page object file
        file_path = f"src/main/python/pages/{scenario['requirement_title'].lower().replace(' ', '_')}_page.py"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(page_object_content)

    def _generate_test_class(self, scenario: Dict):
        """
        Generate test class for the test scenario
        
        Args:
            scenario (Dict): Test scenario details
        """
        # Template for test class
        test_class_template = Template('''
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.{{ page_class_file }} import {{ page_class }}
import os
from dotenv import load_dotenv

class {{ test_class_name }}(unittest.TestCase):
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
        self.page = {{ page_class }}(self.driver)

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    {% for test_case in test_cases %}
    def test_{{ test_case.name }}(self):
        """{{ test_case.description }}"""
        {% for step in test_case.steps %}
        {{ step }}
        {% endfor %}
    {% endfor %}

if __name__ == '__main__':
    unittest.main()
''')

        # Generate test class content
        test_cases = []
        for test_case in scenario['test_cases']:
            # Always create at least one valid test method
            steps = [f"self.page.navigate_to(self.base_url)"]
            # If there are additional steps, add them here
            if 'steps' in test_case and isinstance(test_case['steps'], list):
                steps.extend(test_case['steps'])
            case = {
                'name': test_case['title'].lower().replace(' ', '_'),
                'description': test_case['title'],
                'steps': steps
            }
            test_cases.append(case)
        # If no test cases, add a dummy test to avoid empty class
        if not test_cases:
            test_cases.append({
                'name': 'dummy',
                'description': 'Dummy test to ensure at least one test method exists.',
                'steps': ['self.page.navigate_to(self.base_url)']
            })

        page_class_name = f"{scenario['requirement_title'].replace(' ', '')}Page"
        page_class_file = f"{scenario['requirement_title'].lower().replace(' ', '_')}_page"
        
        test_class_content = test_class_template.render(
            test_class_name=f"Test{scenario['requirement_title'].replace(' ', '')}",
            page_class=page_class_name,
            page_class_file=page_class_file,
            test_cases=test_cases
        )

        # Save the test class file
        file_path = f"src/test/python/test_{scenario['requirement_title'].lower().replace(' ', '_')}.py"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(test_class_content)