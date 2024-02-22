from pycspr.api.servers.rpc.utils.params import get_block_id
from pycspr.api.servers.rpc.utils.proxy import Proxy
from pycspr.types import BlockID
from pycspr.types import StateRootHash


_ENDPOINT: str = "chain_get_state_root_hash"


def exec(proxy: Proxy, block_id: BlockID = None) -> StateRootHash:
    """Returns root hash of global state at a finalised block.

    :param block_id: Identifier of a finalised block.
    :returns: State root hash at finalised block.

    """
    params: dict = get_block_id(block_id)
    response: dict = proxy.get_response(_ENDPOINT, params)

    return bytes.fromhex(response["state_root_hash"])
