import logging
import os
from urllib.parse import urlsplit

import boto3
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection

logger = logging.getLogger(__name__)
_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client

    endpoint = os.environ["OPENSEARCH_ENDPOINT"].strip()
    if "://" not in endpoint:
        endpoint = f"https://{endpoint}"
    parsed_endpoint = urlsplit(endpoint)
    if parsed_endpoint.scheme != "https" or not parsed_endpoint.hostname:
        raise ValueError("OPENSEARCH_ENDPOINT must be an HTTPS host or URL")
    if parsed_endpoint.path not in ("", "/") or parsed_endpoint.query or parsed_endpoint.fragment:
        raise ValueError("OPENSEARCH_ENDPOINT must not include a path, query, or fragment")

    region = os.environ["OPENSEARCH_REGION"]
    credentials = boto3.Session().get_credentials()
    if credentials is None:
        raise RuntimeError("AWS credentials are not available to the OpenSearch client")

    auth = AWSV4SignerAuth(credentials, region, "es")
    _client = OpenSearch(
        hosts=[{"host": parsed_endpoint.hostname, "port": parsed_endpoint.port or 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=10,
        max_retries=3,
        retry_on_timeout=True,
    )
    logger.info("Configured OpenSearch client for host %s in %s", parsed_endpoint.hostname, region)
    return _client


def index_login_event(document, topic, partition, offset):
    if os.getenv("OPENSEARCH_ENABLED", "false").lower() != "true":
        return

    index_name = os.getenv("OPENSEARCH_INDEX", "showcase-login-events")
    document_id = f"{topic}-{partition}-{offset}"
    result = _get_client().index(index=index_name, id=document_id, body=document)
    logger.info(
        "Indexed login event in OpenSearch: index=%s id=%s result=%s",
        index_name,
        document_id,
        result.get("result", "unknown"),
    )