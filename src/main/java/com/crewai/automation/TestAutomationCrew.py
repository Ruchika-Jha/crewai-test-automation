from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class TestAutomationCrew:
    def __init__(self, azure_pat, azure_org_url, project_name):
        self.openai_model = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key="your_openai_api_key"
        )
        self.azure_connection = self._setup_azure_connection(azure_pat, azure_org_url)
        self.project_name = project_name

    def _setup_azure_connection(self, pat, org_url):
        credentials = BasicAuthentication('', pat)
        return Connection(base_url=org_url, creds=credentials)

    def create_agents(self):
        # Test Analyst Agent - Responsible for understanding requirements and creating test scenarios
        self.test_analyst = Agent(
            role='Test Analyst',
            goal='Analyze requirements and create comprehensive test scenarios',
            backstory="""You are an experienced Test Analyst with expertise in 
            understanding business requirements and creating detailed test scenarios.
            You excel at identifying edge cases and critical test paths.""",
            verbose=True,
            allow_delegation=True,
            llm=self.openai_model
        )

        # Automation Engineer Agent - Responsible for creating test automation code
        self.automation_engineer = Agent(
            role='Automation Engineer',
            goal='Create efficient and maintainable test automation scripts',
            backstory="""You are a skilled Automation Engineer with deep knowledge of 
            Selenium WebDriver, Java, and TestNG. You create reliable and maintainable 
            test automation scripts following best practices.""",
            verbose=True,
            allow_delegation=True,
            llm=self.openai_model
        )

        # QA Lead Agent - Responsible for overseeing test execution and reporting
        self.qa_lead = Agent(
            role='QA Lead',
            goal='Ensure quality of test execution and accurate reporting',
            backstory="""You are a detail-oriented QA Lead who ensures proper test 
            execution and maintains high quality standards. You excel at analyzing 
            test results and providing actionable insights.""",
            verbose=True,
            allow_delegation=True,
            llm=self.openai_model
        )

    def create_tasks(self):
        # Task 1: Analyze Requirements
        analyze_requirements = Task(
            description="""Analyze the requirements from Azure DevOps and create 
            detailed test scenarios. Focus on critical paths and edge cases.""",
            agent=self.test_analyst
        )

        # Task 2: Create Test Scripts
        create_test_scripts = Task(
            description="""Create Selenium test scripts based on the test scenarios. 
            Implement proper page objects and maintain code quality.""",
            agent=self.automation_engineer
        )

        # Task 3: Execute Tests
        execute_tests = Task(
            description="""Execute the test scripts, analyze results, and prepare 
            detailed test execution report.""",
            agent=self.qa_lead
        )

        return [analyze_requirements, create_test_scripts, execute_tests]

    def run_automation_process(self):
        # Create agents
        self.create_agents()

        # Create tasks
        tasks = self.create_tasks()

        # Create crew
        crew = Crew(
            agents=[self.test_analyst, self.automation_engineer, self.qa_lead],
            tasks=tasks,
            process=Process.sequential  # Tasks will be executed in sequence
        )

        # Start the crew's work
        result = crew.kickoff()
        return result