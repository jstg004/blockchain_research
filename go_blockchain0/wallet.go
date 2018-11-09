// my notes for this tutorial:
// https://jeiwan.cc/posts/building-blockchain-in-go-part-1/

// addresses are human readable representations of public keys
// one's identity is comprised of a public key and a private key
//    - these keys are created using cryptography algorithms
// the owner of the private key controlls all coins sent to that key
// keys that are generated are random sequences of bytes
//    - they are converted to human readable strings

// digital signatures - algorithms that guarantee the following:
// 1. data has not been modified in transit
// 2. data was created by a particular sender
// 3. sender cannot deny sending the data

// requirements to sign the data:
// 1. data to be signed
// 2. private key

// signing operation requirements:
// 1. data that was signed
// 2. signature
// 3. public key

// verification process:
// check the signature was obtained from this data with the private key used to
//    generate the public key

// cannot reconstruct the data from a signature - not encrypted
//    - public/private keys are prepresentations of the data not encrypted
//      versions of the data

// every transaction input is signed by the creator of that transaction
// every transaction must be verified before being inserted into a block
// to verify:
// 1. check if input has permission to use output form previous transaction
// 2. check that the transaction signature is correct

package main

import (
	"bytes"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"log"

	"golang.org/x/crypto/ripemd160"
)

const version = byte(0x00)
const addressChecksumLen = 4

// Wallet stores a key pair of private and public keys
type Wallet struct {
	PrivateKey ecdsa.PrivateKey
	PublicKey  []byte
}

// NewWallet creates and returns a Wallet
func NewWallet() *Wallet {
	private, public := newKeyPair()
	wallet := Wallet{private, public}

	return &wallet
}

// GetAddress returns wallet address
func (w Wallet) GetAddress() []byte {
	pubKeyHash := HashPubKey(w.PublicKey)
	// prepend the version of the address generation algorithm to the hash
	versionedPayload := append([]byte{version}, pubKeyHash...)
	checksum := checksum(versionedPayload)
	// appends the checksum to the versionedPayload
	fullPayload := append(versionedPayload, checksum...)
	//encodes fullPayload to Base58 to create the wallet address
	address := Base58Encode(fullPayload)

	return address
}

// HashPubKey hashes public key twice
func HashPubKey(pubKey []byte) []byte {
	publicSHA256 := sha256.Sum256(pubKey)

	RIPEMD160Hasher := ripemd160.New()
	_, err := RIPEMD160Hasher.Write(publicSHA256[:])
	if err != nil {
		log.Panic(err)
	}
	publicRIPEMD160 := RIPEMD160Hasher.Sum(nil)

	return publicRIPEMD160
}

// ValidateAddress check if address if valid
// Base58 removes the following symbols from Base64:
//    - 0 (zero), O (capital o), I (capital i), l (lowercase L)
func ValidateAddress(address string) bool {
	pubKeyHash := Base58Decode([]byte(address))
	actualChecksum := pubKeyHash[len(pubKeyHash)-addressChecksumLen:]
	version := pubKeyHash[0]
	pubKeyHash = pubKeyHash[1 : len(pubKeyHash)-addressChecksumLen]
	targetChecksum := checksum(append([]byte{version}, pubKeyHash...))

	return bytes.Compare(actualChecksum, targetChecksum) == 0
}

// Checksum generates a checksum for a public key
func checksum(payload []byte) []byte {
	firstSHA := sha256.Sum256(payload)
	secondSHA := sha256.Sum256(firstSHA[:])
	// the checksum is the 1st 4 bytes of the secondSHA hash
	return secondSHA[:addressChecksumLen]
}

func newKeyPair() (ecdsa.PrivateKey, []byte) {
	curve := elliptic.P256() //elliptic curve
	// a private key is generated using the elliptic curve:
	private, err := ecdsa.GenerateKey(curve, rand.Reader)
	if err != nil {
		log.Panic(err)
	}
	// public key is generated from the private key:
	//    - public keys are points on a curve
	//    - combination of X and Y coordinates
	//    - the X,Y coordinates are concatenated to form the public key
	pubKey := append(private.PublicKey.X.Bytes(), private.PublicKey.Y.Bytes()...)

	return *private, pubKey
}
