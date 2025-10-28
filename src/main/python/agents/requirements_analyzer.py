from crewai import Agent
from typing import List, Dict
import openai
import os
from dotenv import load_dotenv

class RequirementsAnalyzer:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        print(f"Loaded OpenAI API key: {openai.api_key}")

    def create_agent(self):
        return Agent(
            role='Requirements Analyzer',
            goal='Analyze requirements and generate detailed test scenarios',
            backstory="""You are an expert in analyzing software requirements and 
            breaking them down into detailed test scenarios. You understand both 
            functional and technical aspects of testing.""",
            verbose=True
        )

    def analyze_requirements(self, requirements: List[Dict]) -> List[Dict]:
        """
        Analyze requirements and generate test scenarios
        
        Args:
            requirements (List[Dict]): List of requirements from Azure DevOps
            
        Returns:
            List[Dict]: List of test scenarios
        """
        test_scenarios = []
        
        for req in requirements:
            # Generate test scenarios using OpenAI
            test_cases = self._generate_test_scenarios(req)
            
            scenario = {
                'requirement_id': req['id'],
                'requirement_title': req['title'],
                'test_cases': test_cases
            }
            test_scenarios.append(scenario)
        
        return test_scenarios

    def _generate_test_scenarios(self, requirement: Dict) -> List[Dict]:
        """
        Generate test scenarios for a requirement using OpenAI
        
        Args:
            requirement (Dict): Single requirement details
            
        Returns:
            List[Dict]: List of test cases for the requirement
        """
        prompt = f"""
        Based on the following requirement, generate detailed test scenarios:
        
        Title: {requirement['title']}
        Description: {requirement['description']}
        Acceptance Criteria: {requirement['acceptance_criteria']}
        
        For each test case, provide:
        1. Test case title
        2. Test steps
        3. Expected results
        4. Test data requirements
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a test automation expert. Generate detailed, practical test scenarios that can be automated using Selenium."},
                    {"role": "user", "content": prompt}
                ]
            )
            print(f"\n--- RAW OPENAI RESPONSE FOR REQUIREMENT '{requirement['title']}' ---\n{response.choices[0].message.content}\n--- END RESPONSE ---\n")
            # Process and structure the response
            test_cases = self._parse_test_scenarios(response.choices[0].message.content)
            if not test_cases:
                # Fallback: generate a default test case
                test_cases = [{
                    'title': f"Default test for: {requirement['title']}",
                    'steps': [
                        f"Review requirement: {requirement['description']}",
                        "Design a basic test flow based on acceptance criteria."
                    ],
                    'expected_results': ["Requirement is covered by at least one test."],
                    'test_data': {}
                }]
            return test_cases
        except Exception as e:
            print(f"Error generating test scenarios: {str(e)}")
            # Fallback: generate a default test case
            return [
                {
                    'title': f"Default test for: {requirement['title']}",
                    'steps': [
                        f"Review requirement: {requirement['description']}",
                        "Design a basic test flow based on acceptance criteria."
                    ],
                    'expected_results': ["Requirement is covered by at least one test."],
                    'test_data': {}
                }
            ]

    def _parse_test_scenarios(self, content: str) -> List[Dict]:
        """
        Improved parser for OpenAI response to extract all test cases, steps, expected results, and test data.
        """
        import re
        test_cases = []
        try:
            # Split on both 'Test Case' and 'Test Scenario' headers
            raw_cases = re.split(r"Test Case \d+:|Test Scenario \d+:", content)
            for raw_case in raw_cases[1:]:
                lines = [l.strip() for l in raw_case.strip().split("\n") if l.strip()]
                test_case = {
                    'title': '',
                    'steps': [],
                    'expected_results': [],
                    'test_data': {}
                }
                current_section = None
                for line in lines:
                    # Section headers can be numbered, e.g., '2. Test Steps:'
                    if "Test Case Title:" in line:
                        test_case['title'] = line.split("Test Case Title:",1)[1].strip()
                        current_section = None
                    elif re.match(r"\d+\.\s*Test Steps:?", line):
                        current_section = "steps"
                        continue
                    elif re.match(r"\d+\.\s*Expected Results:?", line):
                        current_section = "expected"
                        continue
                    elif re.match(r"\d+\.\s*Test Data Requirements:?", line):
                        current_section = "test_data"
                        continue
                    # Collect lines starting with a dash under the current section
                    if current_section == "steps" and line.startswith("-"):
                        step = line.lstrip("- ").strip()
                        if step:
                            test_case['steps'].append(step)
                    elif current_section == "expected" and line.startswith("-"):
                        expected = line.lstrip("- ").strip()
                        if expected:
                            test_case['expected_results'].append(expected)
                    elif current_section == "test_data" and line.startswith("-"):
                        td = line.lstrip("- ").strip()
                        if td:
                            test_case['test_data'][f"data_{len(test_case['test_data'])+1}"] = td
                if test_case['title']:
                    test_cases.append(test_case)
            return test_cases
        except Exception as e:
            print(f"Error parsing test scenarios: {str(e)}")
            return []