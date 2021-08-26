import requests as rest_client

from pycspr.api import endpoints
from pycspr.client import NodeConnectionInfo



# API endpoint to be invoked.
_API_ENDPOINT = "metrics"


def execute(connection_info: NodeConnectionInfo, metric_id: str = None) -> list:
    """Returns node peers information.

    :param connection_info: Information required to connect to a node.
    :param metric_id: Identifier of node metric.

    :returns: Node metrics information.

    """
    endpoint = f"{connection_info.address_rest}/{endpoints.REST_GET_METRICS}"
    response = rest_client.get(endpoint)
    data = response.content.decode("utf-8")
    data = sorted([i.strip() for i in data.split("\n") if not i.startswith("#")])

    return data if metric_id is None else \
           [i for i in data if i.lower().startswith(metric_id.lower())]
