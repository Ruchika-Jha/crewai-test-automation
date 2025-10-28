from crewai import Agent
import unittest
import os
import sys
import importlib
from typing import List, Dict
import json
from datetime import datetime

class TestExecutor:
    def __init__(self):
        self.test_results = []

    def create_agent(self):
        return Agent(
            role='Test Executor',
            goal='Execute automated tests and report results',
            backstory="""You are responsible for running automated tests and 
            collecting test results. You ensure proper test execution and provide 
            detailed test reports.""",
            tools=[self.execute_tests],
            verbose=True
        )

    def execute_tests(self, test_scenarios: List[Dict]) -> Dict:
        """
        Execute the generated test cases and collect results
        
        Args:
            test_scenarios (List[Dict]): List of test scenarios to execute
            
        Returns:
            Dict: Test execution results
        """
        results = {
            'execution_time': datetime.now().isoformat(),
            'total_scenarios': len(test_scenarios),
            'passed_tests': 0,
            'failed_tests': 0,
            'scenario_results': []
        }

        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        for scenario in test_scenarios:
            scenario_result = self._execute_scenario_tests(scenario)
            results['scenario_results'].append(scenario_result)
            # Update summary counts
            results['passed_tests'] += scenario_result['passed_tests']
            results['failed_tests'] += scenario_result['failed_tests']
        # Save results to a file
        self._save_test_results(results)
        return results

    def _execute_scenario_tests(self, scenario: Dict) -> Dict:
        """
        Execute tests for a single scenario
        
        Args:
            scenario (Dict): Test scenario to execute
            
        Returns:
            Dict: Results for this scenario
        """
        scenario_result = {
            'requirement_id': scenario['requirement_id'],
            'requirement_title': scenario['requirement_title'],
            'passed_tests': 0,
            'failed_tests': 0,
            'test_cases': []
        }

        # Import and run the test module
        test_module_name = f"test_{scenario['requirement_title'].lower().replace(' ', '_')}"
        test_module_path = f"src.test.python.{test_module_name}"

        try:
            # Add the src/test/python directory to Python path
            test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../test/python'))
            if test_dir not in sys.path:
                sys.path.append(test_dir)

            # Import the test module
            test_module = importlib.import_module(test_module_name)

            # Create a test suite
            suite = unittest.TestLoader().loadTestsFromModule(test_module)

            if not suite or not hasattr(suite, '_tests') or not suite._tests:
                print(f"No valid tests found in module {test_module_name} for scenario {scenario['requirement_title']}")
                scenario_result['failed_tests'] += 1
                scenario_result['test_cases'].append({
                    'name': 'no_tests_found',
                    'status': 'FAILED',
                    'error': 'No valid tests found in module.'
                })
            else:
                # Run the tests
                result = unittest.TestResult()
                suite.run(result)

                # Process results
                for test in result.failures + result.errors:
                    test_case = {
                        'name': test[0].id().split('.')[-1],
                        'status': 'FAILED',
                        'error': str(test[1])
                    }
                    scenario_result['test_cases'].append(test_case)
                    scenario_result['failed_tests'] += 1

                # Add successful tests
                successful_tests = result.testsRun - len(result.failures) - len(result.errors)
                scenario_result['passed_tests'] = successful_tests
                
                # Add successful tests
                all_test_names = set()
                for test in suite:
                    try:
                        all_test_names.add(test.id().split('.')[-1])
                    except Exception:
                        pass
                failed_test_names = set(t['name'] for t in scenario_result['test_cases'])
                for test_name in all_test_names - failed_test_names:
                    test_case = {
                        'name': test_name,
                        'status': 'PASSED',
                        'error': None
                    }
                    scenario_result['test_cases'].append(test_case)

        except Exception as e:
            print(f"Error executing tests for scenario {scenario['requirement_title']}: {str(e)}")
            scenario_result['failed_tests'] += 1
            scenario_result['test_cases'].append({
                'name': 'module_import',
                'status': 'FAILED',
                'error': str(e)
            })

        return scenario_result

    def _save_test_results(self, results: Dict):
        """
        Save test results to a file
        
        Args:
            results (Dict): Test execution results
        """
        # Create results directory if it doesn't exist
        os.makedirs('test-results', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'test-results/test_execution_{timestamp}.json'
        
        # Save results as JSON
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)