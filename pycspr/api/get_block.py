import typing

import jsonrpcclient as rpc_client

from pycspr.api import endpoints
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns on-chain block information.

    :param connection_info: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: On-chain block information.

    """
    # Get latest.
    if isinstance(block_id, type(None)):
        response = rpc_client.request(
            connection_info.address_rpc,
            endpoints.RPC_CHAIN_GET_BLOCK
            )

    # Get by hash - bytes | hex.
    elif isinstance(block_id, (bytes, str)):
        response = rpc_client.request(
            connection_info.address_rpc,
            endpoints.RPC_CHAIN_GET_BLOCK, 
            block_identifier={
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }
        )

    # Get by height.
    elif isinstance(block_id, int):
        response = rpc_client.request(
            connection_info.address_rpc,
            endpoints.RPC_CHAIN_GET_BLOCK, 
            block_identifier={
                "Height": block_id
            }
        )

    return response.data.result["block"]