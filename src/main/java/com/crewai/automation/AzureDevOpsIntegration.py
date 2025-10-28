from azure.devops.connection import Connection
from azure.devops.v6_0.work_item_tracking.models import Wiql
from typing import List, Dict

class AzureDevOpsIntegration:
    def __init__(self, connection: Connection, project_name: str):
        self.connection = connection
        self.project_name = project_name
        self.wit_client = connection.clients.get_work_item_tracking_client()

    def get_requirements(self) -> List[Dict]:
        """
        Fetch requirements from Azure DevOps
        """
        wiql = Wiql(
            query=f"""
            SELECT [System.Id], [System.Title], [System.Description]
            FROM WorkItems
            WHERE [System.WorkItemType] = 'Requirement'
            AND [System.TeamProject] = '{self.project_name}'
            AND [System.State] != 'Closed'
            ORDER BY [System.CreatedDate] DESC
            """
        )
        
        wiql_results = self.wit_client.query_by_wiql(wiql).work_items
        requirements = []
        
        if wiql_results:
            for item in wiql_results:
                work_item = self.wit_client.get_work_item(item.id)
                requirements.append({
                    'id': work_item.id,
                    'title': work_item.fields['System.Title'],
                    'description': work_item.fields.get('System.Description', ''),
                    'acceptance_criteria': work_item.fields.get('Microsoft.VSTS.Common.AcceptanceCriteria', '')
                })
        
        return requirements

    def create_test_case(self, title: str, description: str, steps: List[Dict]) -> int:
        """
        Create a test case in Azure DevOps
        """
        test_case = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": title
            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": description
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.Steps",
                "value": self._format_test_steps(steps)
            }
        ]
        
        created_test_case = self.wit_client.create_work_item(
            document=test_case,
            project=self.project_name,
            type="Test Case"
        )
        
        return created_test_case.id

    def update_test_results(self, test_case_id: int, test_result: Dict):
        """
        Update test results in Azure DevOps
        """
        test_results = [
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.TestResult",
                "value": test_result['status']
            },
            {
                "op": "add",
                "path": "/fields/System.History",
                "value": test_result['comment']
            }
        ]
        
        self.wit_client.update_work_item(
            document=test_results,
            id=test_case_id
        )

    def _format_test_steps(self, steps: List[Dict]) -> str:
        """
        Format test steps into Azure DevOps compatible format
        """
        formatted_steps = []
        for step in steps:
            formatted_steps.append({
                "id": len(formatted_steps) + 1,
                "action": step['action'],
                "expectedResult": step['expected_result']
            })
        return formatted_steps