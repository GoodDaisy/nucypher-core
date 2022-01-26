use alloc::boxed::Box;
use alloc::string::String;

use serde::{Deserialize, Serialize};
use umbral_pre::{PublicKey, Signature, Signer};

use crate::address::Address;
use crate::key_frag::EncryptedKeyFrag;
use crate::versioning::{
    messagepack_deserialize, messagepack_serialize, ProtocolObject, ProtocolObjectInner,
};

/// Represents a string used by characters to perform a revocation on a specific Ursula.
#[derive(PartialEq, Debug, Serialize, Deserialize)]
pub struct RevocationOrder {
    staker_address: Address,
    encrypted_kfrag: EncryptedKeyFrag,
    signature: Signature,
}

impl RevocationOrder {
    /// Create and sign a new revocation order.
    pub fn new(
        signer: &Signer,
        staker_address: &Address,
        encrypted_kfrag: &EncryptedKeyFrag,
    ) -> Self {
        Self {
            staker_address: *staker_address,
            encrypted_kfrag: encrypted_kfrag.clone(),
            signature: signer
                .sign(&[staker_address.as_ref(), &encrypted_kfrag.to_bytes()].concat()),
        }
    }

    /// Verifies the revocation order against Alice's key.
    pub fn verify_signature(&self, alice_verifying_key: &PublicKey) -> bool {
        // TODO: return an Option of something instead of returning `bool`?
        let message = [
            self.staker_address.as_ref(),
            &self.encrypted_kfrag.to_bytes(),
        ]
        .concat();
        self.signature.verify(alice_verifying_key, &message)
    }
}

impl<'a> ProtocolObjectInner<'a> for RevocationOrder {
    fn brand() -> [u8; 4] {
        *b"Revo"
    }

    fn version() -> (u16, u16) {
        (1, 0)
    }

    fn unversioned_to_bytes(&self) -> Box<[u8]> {
        messagepack_serialize(&self)
    }

    fn unversioned_from_bytes(minor_version: u16, bytes: &[u8]) -> Option<Result<Self, String>> {
        if minor_version == 0 {
            Some(messagepack_deserialize(bytes))
        } else {
            None
        }
    }
}

impl<'a> ProtocolObject<'a> for RevocationOrder {}
