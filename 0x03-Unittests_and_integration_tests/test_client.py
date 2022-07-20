#!/usr/bin/env python3
""" Test module for utils module """
import client
import unittest
from parameterized import parameterized, parameterized_class
from typing import Dict, Mapping, Sequence
from unittest.mock import MagicMock, Mock, PropertyMock, patch
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ Test class for memorize org """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json', return_value="ok")
    def test_org(self, org: str, mock_object: MagicMock):
        """ Test to memoize org"""
        test_object = GithubOrgClient(org)
        self.assertEqual(test_object.org, mock_object.return_value)
        mock_object.assert_called_once_with(GithubOrgClient.ORG_URL.format(
                                            org=org))

    def test_public_repos_url(self):
        """ Test to Public repo URL"""
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock, return_value="COOL") as mm:
            tpsest_object = GithubOrgClient("org")
            self.assertEqual(test_object._public_repos_url, mm.return_value)

    payload = [{"name": "Monday"},
               {"name": "Tuesday"},
               {"name": "Wednesday"}]

    @patch('client.get_json', return_value=payload)
    def test_public_repos(self, payloads: MagicMock):
        """ Test to Public repos"""
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock, return_value="COOL") as mm:
            test_object = GithubOrgClient("org")
            self.assertEqual(test_object.public_repos(),
                             [repo['name'] for repo in payloads.return_value])
            mm.assert_called_once()
            payloads.assert_called_once()
            client.get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Dict], license_key: str,
                         expected):
        """ Test to Static: has_license"""
        test_object = GithubOrgClient("org")
        self.assertEqual(test_object.has_license(repo, license_key),
                         expected)


@parameterized_class(("org_payload", "repos_payload", "expected_repos",
                      "apache2_repos"), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration Test class to A Githib org client """
    @classmethod
    def setUpClass(cls):
        """ Setup method to integration tests """
        cls.get_patcher = patch('requests.get')
        cls.get_patcher.return_value = cls.__dict__.get('org_payload')
        cls.get_patcher.start()

    def test_public_repos(self):
        """ Integration tests to public_repos method """
        test_client = client.GithubOrgClient("org")
        self.assertEqual(test_client.public_repos(),
                         [repo['name'] for repo in TEST_PAYLOAD[0][2]])

    @classmethod
    def tearDownClass(cls):
        """ Tear down method to integration tests """
        cls.get_patcher.stop()

if __name__ == '__main__':
    unittest.main()
