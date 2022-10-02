from typing import List, Dict, Sequence, Optional, Mapping, Tuple, Set

from .umbral import SecretKey, PublicKey, Signer, Capsule, VerifiedKeyFrag, VerifiedCapsuleFrag


class Address:

    def __init__(self, address_bytes: bytes):
        ...

    def __bytes__(self) -> bytes:
        ...

    def __hash__(self) -> int:
        ...

    def __eq__(self, other) -> bool:
        ...


class Conditions:

    def __init__(self, conditions: str):
        ...

    @classmethod
    def from_string(cls, conditions: str) -> Conditions:
        ...

    def __str__(self) -> str:
        ...


class Context:

    def __init__(self, context: str):
        ...

    @classmethod
    def from_string(cls, context: str) -> Context:
        ...

    def __str__(self) -> str:
        ...


class MessageKit:

    @staticmethod
    def from_bytes(data: bytes) -> MessageKit:
        ...

    def __init__(
        self,
        policy_encrypting_key: PublicKey,
        plaintext: bytes,
        conditions: Optional[Conditions]
    ):
        ...

    def decrypt(self, sk: SecretKey) -> bytes:
        ...

    def decrypt_reencrypted(
        self,
        sk: SecretKey,
        policy_encrypting_key: PublicKey,
        vcfrags: Sequence[VerifiedCapsuleFrag]
    ) -> bytes:
        ...

    capsule: Capsule

    conditions: Optional[Conditions]


class HRAC:

    def __init__(
        self,
        publisher_verifying_key: PublicKey,
        bob_verifying_key: PublicKey,
        label: bytes,
    ):
        ...

    @staticmethod
    def from_bytes(data: bytes) -> HRAC:
        ...

    def __bytes__(self) -> bytes:
        ...


class EncryptedKeyFrag:

    def __init__(
        self,
        signer: Signer,
        recipient_key: PublicKey,
        hrac: HRAC,
        verified_kfrag: VerifiedKeyFrag,
    ):
        ...

    def decrypt(
        self,
        sk: SecretKey,
        hrac: HRAC,
        publisher_verifying_key: PublicKey,
    ) -> VerifiedKeyFrag:
        ...

    @staticmethod
    def from_bytes(data: bytes) -> EncryptedKeyFrag:
        ...

    def __bytes__(self) -> bytes:
        ...


class TreasureMap:

    def __init__(
        self,
        signer: Signer,
        hrac: HRAC,
        policy_encrypting_key: PublicKey,
        assigned_kfrags: Mapping[Address, Tuple[PublicKey, VerifiedKeyFrag]],
        threshold: int,
    ):
        ...

    def encrypt(self, signer: Signer, recipient_key: PublicKey) -> EncryptedTreasureMap:
        ...

    def make_revocation_orders(self, signer: Signer) -> List[RevocationOrder]:
        ...

    destinations: Dict[Address, EncryptedKeyFrag]

    hrac: HRAC

    threshold: int

    policy_encrypting_key: PublicKey

    publisher_verifying_key: PublicKey

    @staticmethod
    def from_bytes(data: bytes) -> TreasureMap:
        ...

    def __bytes__(self) -> bytes:
        ...


class EncryptedTreasureMap:

    def decrypt(
        self,
        sk: SecretKey,
        publisher_verifying_key: PublicKey,
    ) -> TreasureMap:
        ...

    @staticmethod
    def from_bytes(data: bytes) -> EncryptedTreasureMap:
        ...

    def __bytes__(self) -> bytes:
        ...


class ReencryptionRequest:

    def __init__(
        self,
        capsules: Sequence[Capsule],
        hrac: HRAC,
        encrypted_kfrag: EncryptedKeyFrag,
        publisher_verifying_key: PublicKey,
        bob_verifying_key: PublicKey,
        conditions: Optional[Conditions],
        context: Optional[Context],
    ):
        ...

    hrac: HRAC

    publisher_verifying_key: PublicKey

    bob_verifying_key: PublicKey

    encrypted_kfrag: EncryptedKeyFrag

    capsules: List[Capsule]

    conditions: Optional[Conditions]

    context: Optional[Context]

    @staticmethod
    def from_bytes(data: bytes) -> ReencryptionRequest:
        ...

    def __bytes__(self) -> bytes:
        ...


class ReencryptionResponse:

    def __init__(self, signer: Signer, capsules_and_vcfrags: Sequence[Tuple[Capsule, VerifiedCapsuleFrag]]):
        ...

    def verify(
        self,
        capsules: Sequence[Capsule],
        alice_verifying_key: PublicKey,
        ursula_verifying_key: PublicKey,
        policy_encrypting_key: PublicKey,
        bob_encrypting_key: PublicKey,
    ) -> List[VerifiedCapsuleFrag]:
        ...

    @staticmethod
    def from_bytes(data: bytes) -> ReencryptionResponse:
        ...

    def __bytes__(self) -> bytes:
        ...


class RetrievalKit:

    @staticmethod
    def from_message_kit(message_kit: MessageKit) -> RetrievalKit:
        ...

    def __init__(
        self,
        capsule: Capsule,
        queried_addresses: Set[Address],
        conditions: Optional[Conditions],
    ):
        ...

    capsule: Capsule

    queried_addresses: Set[Address]

    conditions: Optional[Conditions]

    @staticmethod
    def from_bytes(data: bytes) -> RetrievalKit:
        ...

    def __bytes__(self) -> bytes:
        ...


class RevocationOrder:

    def __init__(
        self,
        signer: Signer,
        staking_provider_address: Address,
        encrypted_kfrag: EncryptedKeyFrag,
    ):
        ...

    def verify(
        self,
        alice_verifying_key: PublicKey,
    ) -> Tuple[Address, EncryptedKeyFrag]:
        ...

    @staticmethod
    def from_bytes(data: bytes) -> RevocationOrder:
        ...

    def __bytes__(self) -> bytes:
        ...


class NodeMetadataPayload:

    def __init__(
        self,
        staking_provider_address: Address,
        domain: str,
        timestamp_epoch: int,
        verifying_key: PublicKey,
        encrypting_key: PublicKey,
        certificate_der: bytes,
        host: str,
        port: int,
        operator_signature: Optional[bytes],
    ):
        ...

    staking_provider_address: Address

    verifying_key: PublicKey

    encrypting_key: PublicKey

    operator_signature: Optional[bytes]

    domain: str

    host: str

    port: int

    timestamp_epoch: int

    certificate_der: bytes

    def derive_operator_address(self) -> Address:
        ...


class NodeMetadata:

    def __init__(self, signer: Signer, payload: NodeMetadataPayload):
        ...

    def verify(self) -> bool:
        ...

    payload: NodeMetadataPayload

    @staticmethod
    def from_bytes(data: bytes) -> NodeMetadata:
        ...

    def __bytes__(self) -> bytes:
        ...


class FleetStateChecksum:

    def __init__(self, this_node: Optional[NodeMetadata], other_nodes: Sequence[NodeMetadata]):
        ...


class MetadataRequest:

    def __init__(
        self,
        fleet_state_checksum: FleetStateChecksum,
        announce_nodes: Sequence[NodeMetadata],
    ):
        ...

    fleet_state_checksum: FleetStateChecksum

    announce_nodes: List[NodeMetadata]

    @staticmethod
    def from_bytes(data: bytes) -> MetadataRequest:
        ...

    def __bytes__(self) -> bytes:
        ...


class MetadataResponsePayload:

    def __init__(self, timestamp_epoch: int, announce_nodes: Sequence[NodeMetadata]):
        ...

    timestamp_epoch: int

    announce_nodes: List[NodeMetadata]


class MetadataResponse:

    def __init__(self, signer: Signer, payload: MetadataResponsePayload):
        ...

    def verify(self, verifying_pk: PublicKey) -> MetadataResponsePayload:
        ...

    @staticmethod
    def from_bytes(data: bytes) -> MetadataResponse:
        ...

    def __bytes__(self) -> bytes:
        ...