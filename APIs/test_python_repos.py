"""
Pierre-Charles Dussault
April 21, 2021

Test suite for the file 'python_repos.py'
"""
import unittest
import python_repos


class TestPythonRepos(unittest.TestCase):

    def setUp(self):
        self.url = 'https://api.github.com/search/repositories?q=language:' \
                   'python&sort=stars'
        self.headers = {'Accept': 'application/vnd.github.com.v3+json'}
        self.my_request = python_repos.get_api_response(self.url,
                                                        headers=self.headers)

    def test_main_request(self):
        """ Verify that the status code indicates a successful API request."""
        self.assertEqual(self.my_request.status_code, 200)  # 200 -> success

    def test_returned_repos(self):
        """Verify that there were 30 repositories that were returned."""
        response_dict = self.my_request.json()
        returned_repos = python_repos.get_dicts_of_repos(response_dict)
        self.assertEqual(len(returned_repos), 30)

    def test_total_repos(self):
        """Verify that the total available repos for the selected language are
        greater than 30, the amount to be returned for the most-starred ones.
        """
        response_dict = self.my_request.json()
        self.assertTrue(response_dict['total_count'] > 30, "API response is "
                                                           "inadequate")


if __name__ == '__main__':
    unittest.main()
