import argparse
import os
import pathlib
import typing

import pycspr
from pycspr import NodeClient
from pycspr import NodeConnectionInfo
from pycspr.types import CL_URef
from pycspr.types import GlobalStateID
from pycspr.types import GlobalStateIDType
from pycspr.types import PurseID
from pycspr.types import PurseIDType


# Path to CCTL assets.
_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to execute native transfers with pycspr.")

# CLI argument: path to cp2 account key - defaults to CCTL user 2.
_ARGS.add_argument(
    "--account-key-path",
    default=_PATH_TO_CCTL_ASSETS / "users" / "user-1" / "public_key_hex",
    dest="path_to_account_key",
    help="Path to a test user's public_key_hex file.",
    type=str,
    )

# CLI argument: host address of target node - defaults to CCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API REST port - defaults to 14101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rest",
    default=14101,
    dest="node_port_rest",
    help="Node API REST port.  Typically 8888 on most nodes.",
    type=int,
    )

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )

# CLI argument: Node API SSE port - defaults to 18101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-sse",
    default=18101,
    dest="node_port_sse",
    help="Node API SSE port.  Typically 9999 on most nodes.",
    type=int,
    )


class _Context():
    def __init__(self, args: argparse.Namespace):
        self.client = NodeClient(NodeConnectionInfo(
            host=args.node_host,
            port_rest=args.node_port_rest,
            port_rpc=args.node_port_rpc,
            port_sse=args.node_port_sse
        ))
        self.user_public_key = pycspr.parse_public_key(args.path_to_account_key)


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Query A Node")
    print("-" * 74)

    ctx = _Context(args)
    for func in {
        # _get_node_rpc,
        # _get_node_ops,
        _get_chain_block,
        # _get_chain_era_info,
        # _get_chain_era_summary,
        # _get_chain_auction_info,
        # _get_chain_state_root_hash,
        # _get_chain_account_info,
    }:
        func(ctx)
        print("-" * 74)


def _get_chain_block(ctx: _Context):
    # Query: get_block_at_era_switch - polls until switch block.
    print("POLLING :: get_block_at_era_switch - may take some time")
    block: dict = ctx.client.get_block_at_era_switch()
    assert isinstance(block, dict)
    print("SUCCESS :: get_block_at_era_switch")

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        block: bytes = ctx.client.get_block(block_id)
        assert isinstance(block, dict)
        print(f"SUCCESS :: get_block :: block-id={block_id}")

    assert ctx.client.get_block(block["hash"]) == \
           ctx.client.get_block(block["header"]["height"])
    print("SUCCESS :: get_block - by equivalent height & hash")

    # Query: get_block_transfers - by hash & by height.
    block_transfers: tuple = ctx.client.get_block_transfers(block["hash"])
    assert isinstance(block_transfers, tuple)
    assert isinstance(block_transfers[0], str)      # black hash
    assert isinstance(block_transfers[1], list)     # set of transfers
    assert block_transfers == ctx.client.get_block_transfers(block["header"]["height"])
    print("SUCCESS :: get_block_transfers - by hash & by height")


def _get_node_ops(ctx: _Context):
    # get_node_metrics.
    node_metrics: typing.List[str] = ctx.client.get_node_metrics()
    assert isinstance(node_metrics, list)
    print("SUCCESS :: get_node_metrics")

    # get_node_metric.
    node_metric: typing.List[str] = ctx.client.get_node_metric("mem_deploy_gossiper")
    assert isinstance(node_metric, list)
    print("SUCCESS :: get_node_metric")

    # get_node_peers.
    node_peers: typing.List[dict] = ctx.client.get_node_peers()
    assert isinstance(node_peers, list)
    print("SUCCESS :: get_node_peers")

    # get_node_status.
    node_status: dict = ctx.client.get_node_status()
    assert isinstance(node_status, dict)
    print("SUCCESS :: get_node_status")


def _get_node_rpc(ctx: _Context):
    # get_rpc_schema.
    rpc_schema: dict = ctx.client.get_rpc_schema()
    assert isinstance(rpc_schema, dict)
    print("SUCCESS :: get_rpc_schema")

    # get_rpc_endpoints.
    rpc_endpoints: typing.List[str] = ctx.client.get_rpc_endpoints()
    assert isinstance(rpc_endpoints, list)
    print("SUCCESS :: get_rpc_endpoints")

    # get_rpc_endpoint.
    for rpc_endpoint in rpc_endpoints:
        rpc_endpoint_schema: dict = ctx.client.get_rpc_endpoint("account_put_deploy")
        assert isinstance(rpc_endpoint_schema, dict)
    print("SUCCESS :: get_rpc_endpoint")


def _get_chain_auction_info(ctx: _Context):
    block: dict = ctx.client.get_block()

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        auction_info: bytes = ctx.client.get_auction_info(block_id)
        assert isinstance(auction_info, dict)
        print(f"SUCCESS :: get_auction_info :: block-id={block_id}")

    assert ctx.client.get_auction_info(block["hash"]) == \
           ctx.client.get_auction_info(block["header"]["height"])
    print("SUCCESS :: get_auction_info - by equivalent block height & hash")

    # Validator changes.
    validator_changes: typing.List[dict] = ctx.client.get_validator_changes()
    assert isinstance(validator_changes, list)
    print("SUCCESS :: get_validator_changes")


def _get_chain_era_info(ctx: _Context):
    block: dict = ctx.client.get_block()

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        era_info: bytes = ctx.client.get_era_info(block_id)
        assert isinstance(era_info, dict)
        print(f"SUCCESS :: get_era_info :: block-id={block_id}")

    assert ctx.client.get_era_info(block["hash"]) == \
           ctx.client.get_era_info(block["header"]["height"])
    print("SUCCESS :: get_era_info - by equivalent block height & hash")


def _get_chain_era_summary(ctx: _Context):
    block: dict = ctx.client.get_block()

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        era_summary: bytes = ctx.client.get_era_summary(block_id)
        assert isinstance(era_summary, dict)
        print(f"SUCCESS :: get_era_summary :: block-id={block_id}")

    assert ctx.client.get_era_summary(block["hash"]) == \
           ctx.client.get_era_summary(block["header"]["height"])
    print("SUCCESS :: get_era_summary :: by equivalent switch block height & hash")


def _get_chain_state_root_hash(ctx: _Context):
    block: dict = ctx.client.get_block()

    for block_id in {
        None,
        block["hash"],
        block["header"]["height"]
    }:
        state_root_hash: bytes = ctx.client.get_state_root_hash(block_id)
        assert isinstance(state_root_hash, bytes)
        print(f"SUCCESS :: get_state_root_hash :: block-id={block_id}")

    assert ctx.client.get_state_root_hash(block["hash"]) == \
           ctx.client.get_state_root_hash(block["header"]["height"])
    print("SUCCESS :: get_state_root_hash :: by equivalent switch block height & hash")


def _get_chain_account_info(ctx: _Context):
    state_root_hash: bytes = ctx.client.get_state_root_hash()

    # Query: get_account_info.
    account_info: dict = ctx.client.get_account_info(ctx.user_public_key.account_key)
    assert isinstance(account_info, dict)
    print("SUCCESS :: get_account_info")

    # Query: get_account_main_purse_uref.
    account_main_purse: CL_URef = \
        ctx.client.get_account_main_purse_uref(ctx.user_public_key.account_key)
    assert isinstance(account_main_purse, CL_URef)
    print("SUCCESS :: get_account_main_purse_uref")

    # Query: get_account_balance.
    global_state_id = GlobalStateID(state_root_hash, GlobalStateIDType.STATE_ROOT_HASH)
    purse_id = PurseID(account_main_purse, PurseIDType.UREF)
    account_balance: int = ctx.client.get_account_balance(purse_id, global_state_id)
    assert isinstance(account_balance, int)
    print("SUCCESS :: get_account_balance")


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
