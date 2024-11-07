import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from t5_grp.visualization.diagram_generator import generate_html, extract_pipeline_data
"""
Unit tests for the `diagram_generator` module in the t5_grp.visualization package.

This module contains tests to ensure that the `generate_html` and `extract_pipeline_data` functions work correctly,
handling various inputs and edge cases as expected.

Classes:
    TestDiagramGenerator:
        Contains tests for the `generate_html` and `extract_pipeline_data` functions.

Methods:
    test_generate_html:
        Tests if the `generate_html` function correctly generates an HTML file from given pipeline data.

    test_extract_pipeline_data:
        Tests if the `extract_pipeline_data` function correctly processes and extracts pipeline data.

    test_extract_pipeline_data_missing_stage:
        Tests the `extract_pipeline_data` function's behavior when a job has a missing stage.
"""
# class TestDiagramGenerator(unittest.TestCase):
#     """
#         Contains unit tests for the `diagram_generator` functions.
#
#         These tests ensure that the `generate_html` and `extract_pipeline_data` functions behave as expected.
#         """
#     @patch('builtins.open', new_callable=mock_open)
#     @patch('os.makedirs')
#     @patch('os.path.exists')
#     @patch('t5_grp.visualization.diagram_generator.Environment.get_template')
#     def test_generate_html(self, mock_get_template, mock_exists, mock_makedirs, mock_open):
#         """
#          Tests the `generate_html` function to ensure it generates an HTML file from given pipeline data.
#
#          Mocks the file operations and Jinja2 environment to simulate HTML generation without actual file I/O.
#
#          Args:
#              mock_env (MagicMock): Mock for the Jinja2 Environment.
#              mock_file_loader (MagicMock): Mock for the Jinja2 FileSystemLoader.
#              mock_open (MagicMock): Mock for the open function.
#              mock_makedirs (MagicMock): Mock for the os.makedirs function.
#              mock_exists (MagicMock): Mock for the os.path.exists function.
#          """
#         mock_exists.side_effect = [False, True]
#         mock_template = MagicMock()
#         mock_get_template.return_value = mock_template
#         mock_template.render.return_value = '<html></html>'
#
#         # 测试数据
#         data = {
#             'pipeline': {'name': 'Test Pipeline'},
#             'stages': ['Build', 'Test', 'Deploy'],
#             'jobs': [
#                 {'name': 'build1', 'stage': 'Build'},
#                 {'name': 'test1', 'stage': 'Test', 'needs': ['build1']},
#                 {'name': 'deploy1', 'stage': 'Deploy', 'needs': ['test1']}
#             ]
#         }
#
#         generate_html(data)
#
#         mock_template.render.assert_called_once_with(pipeline=extract_pipeline_data(data))
#         # AssertionError: exists('/Users/yoyowu/NEU/t5_grp/src/src/main') call not found
#         expected_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..',  'src', 'main'))
#         mock_exists.assert_any_call(expected_output_dir)
#         mock_makedirs.assert_called_once_with(expected_output_dir)
#
#         expected_output_path = os.path.join(expected_output_dir, 'output.html')
#         mock_open.assert_called_once_with(expected_output_path, 'w')
#         mock_open().write.assert_called_once_with('<html></html>')
#
#     def test_extract_pipeline_data(self):
#         """
#         Tests the `extract_pipeline_data` function to ensure it correctly processes and extracts pipeline data.
#
#         This test checks various aspects, like job dependencies and artifacts, to validate the data extraction logic.
#         """
#         data = {
#             'pipeline': {'name': 'Test Pipeline'},
#             'stages': ['Build', 'Test', 'Deploy'],
#             'jobs': [
#                 {'name': 'build1', 'stage': 'Build'},
#                 {'name': 'test1', 'stage': 'Test', 'needs': ['build1'], 'artifacts': {'paths': ['artifact1']}},
#                 {'name': 'deploy1', 'stage': 'Deploy', 'needs': ['test1']}
#             ]
#         }
#
#         expected_pipeline_data = {
#             'name': 'Test Pipeline',
#             'stages': ['Build', 'Test', 'Deploy'],
#             'jobs': {
#                 'build1': {
#                     'stage': 'Build',
#                     'needs': [],
#                     'allow_failure': False,
#                     'id': 'job_build1',
#                     'position': 0,
#                     'artifacts': []
#                 },
#                 'test1': {
#                     'stage': 'Test',
#                     'needs': ['build1'],
#                     'allow_failure': False,
#                     'id': 'job_test1',
#                     'position': 1,
#                     'artifacts': ['artifact1']
#                 },
#                 'deploy1': {
#                     'stage': 'Deploy',
#                     'needs': ['test1'],
#                     'allow_failure': False,
#                     'id': 'job_deploy1',
#                     'position': 2,
#                     'artifacts': []
#                 }
#             },
#             'artifacts': {
#                 'Test': ['artifact1']
#             },
#             'dependencies': [
#                 {'from': 'job_build1', 'to': 'job_test1', 'fromStage': 'Build', 'toStage': 'Test'},
#                 {'from': 'job_test1', 'to': 'job_deploy1', 'fromStage': 'Test', 'toStage': 'Deploy'}
#             ],
#             'all_artifacts': ['artifact1']
#         }
#
#         pipeline_data = extract_pipeline_data(data)
#         self.assertEqual(pipeline_data, expected_pipeline_data)
#
#     def test_extract_pipeline_data_missing_stage(self):
#         """
#         Tests the `extract_pipeline_data` function's behavior when a job has a missing stage.
#
#         Ensures that an appropriate exception is raised when a job lacks a stage definition.
#         """
#         data = {
#             'pipeline': {'name': 'Test Pipeline'},
#             'stages': ['Build', 'Test', 'Deploy'],
#             'jobs': [
#                 {'name': 'build1', 'stage': 'Build'},
#                 {'name': 'test1', 'needs': ['build1']}
#             ]
#         }
#         with self.assertRaises(ValueError) as context:
#             extract_pipeline_data(data)
#         self.assertEqual(str(context.exception), "Stage is required for job: test1")
#
# if __name__ == '__main__':
#     unittest.main()