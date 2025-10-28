import os
from dotenv import load_dotenv
from crewai import Crew
from .TestAutomationCrew import TestAutomationCrew
from .RequirementAnalyzer import RequirementAnalyzer
from .TestAutomationGenerator import TestAutomationGenerator
from .TestExecutor import TestExecutor

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize CrewAI setup
    crew = TestAutomationCrew(
        azure_pat=os.getenv('AZURE_PAT'),
        azure_org_url=os.getenv('AZURE_ORG_URL'),
        project_name=os.getenv('AZURE_PROJECT_NAME')
    )
    
    # Create the automation workflow
    try:
        # Step 1: Analyze requirements and create test scenarios
        print("Analyzing requirements and creating test scenarios...")
        requirement_analyzer = RequirementAnalyzer(crew.test_analyst, crew.azure_connection)
        test_scenarios = requirement_analyzer.analyze_requirements()
        
        # Step 2: Generate test automation code
        print("Generating test automation code...")
        automation_generator = TestAutomationGenerator(crew.automation_engineer)
        page_objects = automation_generator.generate_page_objects(test_scenarios)
        test_classes = automation_generator.generate_test_classes(test_scenarios, page_objects)
        
        # Save generated code
        automation_generator.save_generated_code(
            base_path='.',
            page_objects=page_objects,
            test_classes=test_classes
        )
        
        # Step 3: Execute tests and report results
        print("Executing tests and analyzing results...")
        test_executor = TestExecutor(crew.qa_lead, crew.azure_connection)
        test_results = test_executor.execute_tests(test_scenarios)
        
        # Generate final report
        report = test_executor.generate_report(test_results)
        print("\nTest Automation Complete!")
        print("Final Report:")
        print(report)
        
    except Exception as e:
        print(f"Error in automation workflow: {e}")
        raise

if __name__ == "__main__":
    main()