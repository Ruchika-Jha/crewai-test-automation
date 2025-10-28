from crewai import Crew, Process
from dotenv import load_dotenv
from agents.azure_devops_agent import AzureDevOpsAgent
from agents.requirements_analyzer import RequirementsAnalyzer
from agents.test_automation_generator import TestAutomationGenerator
from agents.test_executor import TestExecutor

def main():
    import pprint
    azure_devops_agent = AzureDevOpsAgent()
    try:
        requirements = azure_devops_agent.fetch_requirements()
        print("DEBUG: requirements fetched:")
        pprint.pprint(requirements)
    except Exception as e:
        print(f"Error fetching requirements: {e}")
        requirements = []

    requirements_analyzer = RequirementsAnalyzer()
    try:
        test_scenarios = requirements_analyzer.analyze_requirements(requirements)
        print("DEBUG: test_scenarios generated:")
        pprint.pprint(test_scenarios)
    except Exception as e:
        print(f"Error analyzing requirements: {e}")
        test_scenarios = []
        print("DEBUG: test_scenarios generated (empty due to error):")
        pprint.pprint(test_scenarios)

    print("\nGenerated test scenarios:")
    for scenario in test_scenarios:
        print(f"- {scenario.get('requirement_title', 'N/A')} ({len(scenario.get('test_cases', []))} test cases)")

    # Export test scenarios to Excel
    from agents.excel_exporter import save_test_scenarios_to_excel
    save_test_scenarios_to_excel(test_scenarios)


    test_generator = TestAutomationGenerator()
    test_generator.generate_test_automation(test_scenarios)
    print("\nGenerated Python Selenium test files in src/test/python.")

    # Generate Java Selenium test files and page objects
    from agents.java_test_generator import generate_java_tests
    generate_java_tests(test_scenarios)
    print("Generated Java Selenium test files in src/test/java/com/crewai/tests and page objects in src/main/java/com/crewai/pages.")

    test_executor = TestExecutor()
    test_executor.execute_tests(test_scenarios)
    print("\nAutomation Process Completed!")
    print("Check the test-results directory for detailed execution results.")

if __name__ == "__main__":
    main()