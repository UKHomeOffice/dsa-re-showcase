import os
import unittest
from unittest.mock import Mock, patch

import certifi

import opensearch_sink


class TestGetClient(unittest.TestCase):
    def setUp(self):
        opensearch_sink._client = None

    def tearDown(self):
        opensearch_sink._client = None

    @patch.dict(
        os.environ,
        {"OPENSEARCH_ENDPOINT": "search.example.com", "OPENSEARCH_REGION": "eu-west-2"},
        clear=True,
    )
    @patch("opensearch_sink.OpenSearch")
    @patch("opensearch_sink.AWSV4SignerAuth")
    @patch("opensearch_sink.boto3.Session")
    def test_builds_verified_sigv4_client(self, session, signer_auth, open_search):
        credentials = Mock()
        session.return_value.get_credentials.return_value = credentials
        client = Mock()
        open_search.return_value = client

        result = opensearch_sink._get_client()

        self.assertIs(result, client)
        signer_auth.assert_called_once_with(credentials, "eu-west-2", "es")
        open_search.assert_called_once_with(
            hosts=[{"host": "search.example.com", "port": 443}],
            http_auth=signer_auth.return_value,
            use_ssl=True,
            verify_certs=True,
            ca_certs=certifi.where(),
            connection_class=opensearch_sink.RequestsHttpConnection,
            timeout=10,
            max_retries=3,
            retry_on_timeout=True,
        )

    @patch.dict(
        os.environ,
        {"OPENSEARCH_ENDPOINT": "https://search.example.com:9443/", "OPENSEARCH_REGION": "eu-west-2"},
        clear=True,
    )
    @patch("opensearch_sink.OpenSearch")
    @patch("opensearch_sink.AWSV4SignerAuth")
    @patch("opensearch_sink.boto3.Session")
    def test_accepts_https_endpoint_with_port_and_root_path(
        self, session, signer_auth, open_search
    ):
        session.return_value.get_credentials.return_value = Mock()

        opensearch_sink._get_client()

        self.assertEqual(
            open_search.call_args.kwargs["hosts"],
            [{"host": "search.example.com", "port": 9443}],
        )

    def test_rejects_non_https_endpoint(self):
        invalid_endpoints = (
            "http://search.example.com",
            "https:///missing-host",
            "https://search.example.com/_dashboards",
            "https://search.example.com?query=value",
            "https://search.example.com#fragment",
        )
        for endpoint in invalid_endpoints:
            with self.subTest(endpoint=endpoint):
                with patch.dict(
                    os.environ,
                    {"OPENSEARCH_ENDPOINT": endpoint, "OPENSEARCH_REGION": "eu-west-2"},
                    clear=True,
                ):
                    with self.assertRaises(ValueError):
                        opensearch_sink._get_client()

    @patch.dict(
        os.environ,
        {"OPENSEARCH_ENDPOINT": "search.example.com", "OPENSEARCH_REGION": "eu-west-2"},
        clear=True,
    )
    @patch("opensearch_sink.boto3.Session")
    def test_requires_aws_credentials(self, session):
        session.return_value.get_credentials.return_value = None

        with self.assertRaisesRegex(RuntimeError, "AWS credentials are not available"):
            opensearch_sink._get_client()


class TestIndexLoginEvent(unittest.TestCase):
    def test_does_not_create_client_when_disabled(self):
        with patch.dict(os.environ, {"OPENSEARCH_ENABLED": "false"}, clear=True):
            with patch.object(opensearch_sink, "_get_client") as get_client:
                opensearch_sink.index_login_event({"event_type": "login"}, "user-login", 1, 42)

        get_client.assert_not_called()

    @patch.dict(
        os.environ,
        {"OPENSEARCH_ENABLED": "true", "OPENSEARCH_INDEX": "login-events"},
        clear=True,
    )
    def test_indexes_with_configured_index_and_kafka_document_id(self):
        client = Mock()
        document = {"event_type": "login", "timestamp": "2026-11-09T12:00:00Z"}

        with patch.object(opensearch_sink, "_get_client", return_value=client):
            opensearch_sink.index_login_event(document, "user-login", 1, 42)

        client.index.assert_called_once_with(
            index="login-events",
            id="user-login-1-42",
            body=document,
        )

    @patch.dict(os.environ, {"OPENSEARCH_ENABLED": "true"}, clear=True)
    def test_uses_default_index(self):
        client = Mock()

        with patch.object(opensearch_sink, "_get_client", return_value=client):
            opensearch_sink.index_login_event({}, "user-login", 0, 7)

        self.assertEqual(client.index.call_args.kwargs["index"], "showcase-login-events")

    @patch.dict(os.environ, {"OPENSEARCH_ENABLED": "true"}, clear=True)
    def test_propagates_indexing_errors(self):
        client = Mock()
        client.index.side_effect = RuntimeError("write failed")

        with patch.object(opensearch_sink, "_get_client", return_value=client):
            with self.assertRaisesRegex(RuntimeError, "write failed"):
                opensearch_sink.index_login_event({}, "user-login", 0, 7)


if __name__ == "__main__":
    unittest.main()