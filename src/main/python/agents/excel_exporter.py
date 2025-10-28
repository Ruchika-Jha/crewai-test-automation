import openpyxl
from openpyxl import Workbook
from typing import List, Dict


def save_test_scenarios_to_excel(test_scenarios: List[Dict], filename: str = "test_cases.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"
    # Header
    ws.append(["Requirement ID", "Requirement Title", "Test Case Title", "Test Steps", "Expected Results", "Test Data"])
    for scenario in test_scenarios:
        req_id = scenario.get('requirement_id', '')
        req_title = scenario.get('requirement_title', '')
        for test_case in scenario.get('test_cases', []):
            tc_title = test_case.get('title', '')
            steps = "\n".join(test_case.get('steps', [])) if isinstance(test_case.get('steps', []), list) else test_case.get('steps', '')
            expected = "\n".join(test_case.get('expected_results', [])) if isinstance(test_case.get('expected_results', []), list) else test_case.get('expected_results', '')
            test_data = str(test_case.get('test_data', ''))
            ws.append([req_id, req_title, tc_title, steps, expected, test_data])
    wb.save(filename)
    print(f"Test scenarios saved to {filename}")
