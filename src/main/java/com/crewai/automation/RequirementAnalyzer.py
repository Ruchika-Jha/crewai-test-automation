from typing import List, Dict
from crewai import Agent
from langchain.tools import Tool
from .AzureDevOpsIntegration import AzureDevOpsIntegration

class RequirementAnalyzer:
    def __init__(self, agent: Agent, azure_devops: AzureDevOpsIntegration):
        self.agent = agent
        self.azure_devops = azure_devops
        self._setup_tools()

    def _setup_tools(self):
        self.tools = [
            Tool(
                name="fetch_requirements",
                func=self.azure_devops.get_requirements,
                description="Fetch requirements from Azure DevOps"
            ),
            Tool(
                name="create_test_case",
                func=self.azure_devops.create_test_case,
                description="Create a test case in Azure DevOps"
            )
        ]
        self.agent.tools = self.tools

    def analyze_requirements(self) -> List[Dict]:
        """
        Analyze requirements and create test scenarios
        """
        requirements = self.azure_devops.get_requirements()
        test_scenarios = []

        for req in requirements:
            # Use the agent to analyze the requirement and create test scenarios
            analysis_prompt = f"""
            Analyze the following requirement and create detailed test scenarios:
            Title: {req['title']}
            Description: {req['description']}
            Acceptance Criteria: {req['acceptance_criteria']}

            Create test scenarios that cover:
            1. Happy path testing
            2. Edge cases
            3. Error scenarios
            4. Business logic validation
            """

            scenarios = self.agent.execute_task(analysis_prompt)
            parsed_scenarios = self._parse_scenarios(scenarios, req['id'])
            test_scenarios.extend(parsed_scenarios)

            # Create test cases in Azure DevOps
            for scenario in parsed_scenarios:
                self.azure_devops.create_test_case(
                    title=scenario['title'],
                    description=scenario['description'],
                    steps=scenario['steps']
                )

        return test_scenarios

    def _parse_scenarios(self, agent_response: str, requirement_id: int) -> List[Dict]:
        """
        Parse the agent's response into structured test scenarios
        This is a simplified version - in reality, you'd want more robust parsing
        """
        # This is where you'd implement the logic to parse the agent's natural language
        # response into structured test scenarios. For now, we'll return a sample structure
        return [{
            'title': f'Test Scenario for Requirement {requirement_id}',
            'description': 'Sample test scenario description',
            'requirement_id': requirement_id,
            'steps': [
                {
                    'action': 'Sample test step action',
                    'expected_result': 'Sample expected result'
                }
            ]
        }]

    def validate_scenarios(self, scenarios: List[Dict]) -> List[Dict]:
        """
        Validate the created test scenarios for completeness and quality
        """
        validation_prompt = f"""
        Validate the following test scenarios for completeness and quality:
        {scenarios}

        Check for:
        1. Coverage of all acceptance criteria
        2. Clear and specific test steps
        3. Verifiable expected results
        4. Edge cases and error scenarios
        """

        validation_result = self.agent.execute_task(validation_prompt)
        # Here you would implement logic to parse the validation result
        # and update the scenarios accordingly
        return scenarios