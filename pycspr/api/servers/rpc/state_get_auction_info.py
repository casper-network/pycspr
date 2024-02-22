from pycspr.api import constants
from pycspr.api.servers.rpc.utils.params import get_block_id
from pycspr.api.servers.rpc.utils.proxy import Proxy
from pycspr.types import BlockID


def exec(proxy: Proxy, block_id: BlockID = None) -> dict:
    """Returns current auction system contract information.

    :returns: Current auction system contract information.

    """
    params: dict = get_block_id(block_id, False)

    return proxy.get_response(constants.RPC_STATE_GET_AUCTION_INFO, params)
