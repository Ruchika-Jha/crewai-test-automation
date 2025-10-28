from crewai import Agent
from azure.devops.connection import Connection
from azure.devops.v7_1.work_item_tracking.models import Wiql
from msrest.authentication import BasicAuthentication
from dotenv import load_dotenv
import os

class AzureDevOpsAgent:
    def __init__(self):
        load_dotenv()
        self.pat = os.getenv('AZURE_DEVOPS_PAT')
        self.organization = os.getenv('AZURE_DEVOPS_ORG')
        self.project = os.getenv('AZURE_DEVOPS_PROJECT')
        self.connection = self._create_connection()

    def _create_connection(self):
        credentials = BasicAuthentication('', self.pat)
        organization_url = f"https://dev.azure.com/{self.organization}"
        return Connection(base_url=organization_url, creds=credentials)

    def create_agent(self):
        return Agent(
            role='Azure DevOps Requirements Fetcher',
            goal='Fetch and process test requirements from Azure DevOps',
            backstory="""You are an expert in retrieving and processing requirements from 
            Azure DevOps. Your job is to fetch test requirements and prepare them for 
            test automation.""",
            # tools=[self.fetch_requirements],
            verbose=True
        )

    def fetch_requirements(self) -> list:
        """Fetch test requirements from Azure DevOps project"""
        try:
            wit_client = self.connection.clients.get_work_item_tracking_client()
            
            # Query to fetch requirement work items
            wiql = Wiql(
                query=f"""
                SELECT [System.Id], [System.Title], [System.Description]
                FROM workitems
                WHERE [System.WorkItemType] = 'Product Backlog Item'
                AND [System.TeamProject] = '{self.project}'
                AND [System.State] = 'Committed'
                ORDER BY [System.Id]
                """
            )
            
            # Execute the query
            query_results = wit_client.query_by_wiql(wiql).work_items
            
            requirements = []
            if query_results:
                # Get work items with full details
                work_items = wit_client.get_work_items(
                    ids=[result.id for result in query_results],
                    expand="All"
                )
                
                for work_item in work_items:
                    requirement = {
                        'id': work_item.id,
                        'title': work_item.fields['System.Title'],
                        'description': work_item.fields.get('System.Description', ''),
                        'acceptance_criteria': work_item.fields.get('Microsoft.VSTS.Common.AcceptanceCriteria', '')
                    }
                    requirements.append(requirement)
            
            return requirements
            
        except Exception as e:
            print(f"Error fetching requirements: {str(e)}")
            return []