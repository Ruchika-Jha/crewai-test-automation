import subprocess
from typing import List, Dict
from crewai import Agent
from .AzureDevOpsIntegration import AzureDevOpsIntegration

class TestExecutor:
    def __init__(self, agent: Agent, azure_devops: AzureDevOpsIntegration):
        self.agent = agent
        self.azure_devops = azure_devops

    def execute_tests(self, test_cases: List[Dict]) -> List[Dict]:
        """
        Execute the generated test cases and analyze results
        """
        results = []
        
        # Run tests using Maven
        try:
            subprocess.run(['mvn', 'clean', 'test'], check=True)
            test_output = self._parse_test_results('target/surefire-reports')
            
            analysis_prompt = f"""
            Analyze the following test execution results:
            {test_output}

            Provide:
            1. Summary of test execution
            2. Failed test analysis
            3. Recommendations for fixes
            4. Overall quality assessment
            """
            
            analysis = self.agent.execute_task(analysis_prompt)
            results = self._process_analysis(analysis, test_cases)
            
        except subprocess.CalledProcessError as e:
            print(f"Error executing tests: {e}")
            results = [{'status': 'Failed', 'error': str(e)}]
        
        return results

    def _parse_test_results(self, reports_dir: str) -> Dict:
        """
        Parse test execution reports from surefire-reports directory
        """
        # Implementation would parse XML test reports
        # For now, returning a sample structure
        return {
            'total_tests': 10,
            'passed': 8,
            'failed': 1,
            'skipped': 1,
            'execution_time': '2m 30s'
        }

    def _process_analysis(self, analysis: str, test_cases: List[Dict]) -> List[Dict]:
        """
        Process the agent's analysis and update Azure DevOps
        """
        results = []
        
        # Here you would parse the agent's analysis and create structured results
        # For now, using a sample structure
        for test_case in test_cases:
            result = {
                'test_case_id': test_case['id'],
                'status': 'Passed',  # This would come from actual test results
                'comment': 'Test executed successfully'  # This would come from analysis
            }
            
            # Update test result in Azure DevOps
            self.azure_devops.update_test_results(
                test_case_id=test_case['id'],
                test_result=result
            )
            
            results.append(result)
        
        return results

    def generate_report(self, results: List[Dict]) -> str:
        """
        Generate a detailed test execution report
        """
        report_prompt = f"""
        Create a detailed test execution report from these results:
        {results}

        Include:
        1. Executive summary
        2. Test execution metrics
        3. Failed test analysis
        4. Recommendations
        5. Next steps
        """
        
        return self.agent.execute_task(report_prompt)