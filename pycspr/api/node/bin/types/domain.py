import dataclasses
import typing


BlockHash = typing.NewType(
    "Digest over a block.", bytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", int
)

BlockID = typing.Union[BlockHash, BlockHeight]

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many era precede it.", int
)

PublicKey = typing.NewType(
    "Public key associated with an account.", bytes
    )

TransactionHash = typing.NewType(
    "Digest over a transaction.", bytes
    )

@dataclasses.dataclass
class BlockHeader():
    pass


@dataclasses.dataclass
class BlockRange():
    pass


@dataclasses.dataclass
class NodeUptime():
    pass


@dataclasses.dataclass
class ProtocolVersion():
    # Major semantic version.
    major: int
    # Minor semantic version.
    minor: int
    # Patch semantic version.
    patch: int

    @staticmethod
    def from_semvar(val: str):
        major, minor, patch = val.split(".")

        return ProtocolVersion(
            int(major),
            int(minor),
            int(patch)
        )