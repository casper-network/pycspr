import typing

import jsonrpcclient as rpc_client

from pycspr.types import NodeConnectionInfo



# RPC method to be invoked.
_API_ENDPOINT = "state_get_item"


def execute(
    connection_info: NodeConnectionInfo,
    account_hash: bytes,
    state_root_hash: typing.Union[bytes, None]=None,
    parse_response: bool = True,
    ) -> dict:
    """api account information at a certain state root hash.

    :param connection_info: Information required to connect to a node.
    :param account_hash: An on-chain account identifier derived from it's associated public key.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: Account information in JSON format.

    """    
    root_hash = state_root_hash.hex() if state_root_hash else None
    key=f"account-hash-{account_hash.hex()}"
    path = []

    response = rpc_client.request(
        connection_info.address_rpc,
        _API_ENDPOINT,
        key=key,
        state_root_hash=root_hash,
        path=path
        )

    if parse_response:
        response = response.data.result["stored_value"]["Account"]
    
    return response