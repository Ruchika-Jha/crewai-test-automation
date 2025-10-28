import os
from typing import List, Dict
from crewai import Agent
from jinja2 import Template

class TestAutomationGenerator:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.page_object_template = self._load_template('page_object.java.j2')
        self.test_class_template = self._load_template('test_class.java.j2')

    def _load_template(self, template_name: str) -> Template:
        """
        Load a Jinja2 template for code generation
        """
        template_path = os.path.join(os.path.dirname(__file__), 'templates', template_name)
        with open(template_path, 'r') as f:
            return Template(f.read())

    def generate_page_objects(self, scenarios: List[Dict]) -> Dict[str, str]:
        """
        Generate page objects based on test scenarios
        """
        page_objects = {}
        
        for scenario in scenarios:
            analysis_prompt = f"""
            Analyze the following test scenario and identify required page objects:
            {scenario}

            For each page object, identify:
            1. Web elements and their locators
            2. Required actions and methods
            3. Validations and verifications
            """

            analysis_result = self.agent.execute_task(analysis_prompt)
            page_objects.update(self._create_page_objects(analysis_result))

        return page_objects

    def generate_test_classes(self, scenarios: List[Dict], page_objects: Dict[str, str]) -> Dict[str, str]:
        """
        Generate test classes based on scenarios and page objects
        """
        test_classes = {}
        
        for scenario in scenarios:
            generation_prompt = f"""
            Create a TestNG test class for the following scenario:
            {scenario}

            Available page objects:
            {list(page_objects.keys())}

            Include:
            1. Test method implementation
            2. Required setup and teardown
            3. Assertions and verifications
            4. Error handling
            """

            test_code = self.agent.execute_task(generation_prompt)
            test_classes[f"{scenario['title']}Test"] = test_code

        return test_classes

    def _create_page_objects(self, analysis_result: str) -> Dict[str, str]:
        """
        Create page object classes from analysis result
        """
        # This would parse the agent's response and use templates to generate code
        # For now, returning a simplified structure
        return {
            'SamplePage': self.page_object_template.render(
                class_name='SamplePage',
                elements=[{'name': 'sampleElement', 'locator': 'id="sample"'}],
                methods=[{'name': 'sampleMethod', 'code': 'System.out.println("sample");'}]
            )
        }

    def save_generated_code(self, base_path: str, page_objects: Dict[str, str], test_classes: Dict[str, str]):
        """
        Save generated code to files
        """
        # Save page objects
        page_objects_path = os.path.join(base_path, 'src', 'main', 'java', 'com', 'crewai', 'pages')
        os.makedirs(page_objects_path, exist_ok=True)
        for name, code in page_objects.items():
            with open(os.path.join(page_objects_path, f'{name}.java'), 'w') as f:
                f.write(code)

        # Save test classes
        tests_path = os.path.join(base_path, 'src', 'test', 'java', 'com', 'crewai', 'tests')
        os.makedirs(tests_path, exist_ok=True)
        for name, code in test_classes.items():
            with open(os.path.join(tests_path, f'{name}.java'), 'w') as f:
                f.write(code)