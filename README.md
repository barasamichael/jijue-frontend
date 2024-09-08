# Jijue: A Centralized Digital Identity Platform for Businesses in Kenya

## Verifiable Credential Schema Design
### National ID Credential
__@context__: https://www.w3.org/2018/credentials/v1
__type__: VerifiableCredential, NationalIDCredential
__issuer__: DID of the entity issuing the credential (e.g., Government DID)
__credentialSubject__:
__id__: DID of the holder (individual being identified)
__name__: Full legal name of the individual
__dateOfBirth__: Date of birth of the individual
__nationalIDNumber__: Unique National ID number
__dateOfIssue__: Date when the National ID was issued
__expiryDate__: Date when the National ID expires (if applicable)
__photo__: Base64-encoded string of the individual's photo
__issuanceDate__: Date when the credential was issued
__proof__: Cryptographic proof that binds the credential to the issuer

### Business Certificate Credential
__@context__: https://www.w3.org/2018/credentials/v1
__type__: VerifiableCredential, BusinessCertificateCredential
__issuer__: DID of the entity issuing the certificate (e.g., Government or Registration Authority DID)
__credentialSubject__:
__id__: DID of the holder (company being identified)
__businessName__: Registered name of the business
__businessRegistrationNumber__: Unique business registration number
__businessType__: Type of business (e.g., LLC, Corporation, Sole Proprietorship)
__dateOfIncorporation__: Date when the business was incorporated
__businessAddress__: Physical address of the business
__ownerName__: Name of the business owner or primary contact
__expiryDate__: Expiry date of the business certificate (if applicable)
__issuanceDate__: Date when the credential was issued
__proof__: Cryptographic proof that binds the credential to the issuer

### KRA PIN Credential
__@context__: https://www.w3.org/2018/credentials/v1
__type__: VerifiableCredential, KRAPinCredential
__issuer__: DID of the entity issuing the KRA PIN (e.g., Tax Authority DID)
__credentialSubject__:
__id__: DID of the holder (individual or company being identified)
__name__: Full legal name of the individual or business
__kraPinNumber__: Unique KRA PIN number
__dateOfIssue__: Date when the KRA PIN was issued
__issuanceDate__: Date when the credential was issued
__proof__: Cryptographic proof that binds the credential to the issuer

## Schema Example (JSON-LD)
Here’s how the schema might look in JSON-LD format for a National ID Credential
```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://schema.org"
  ],
  "type": ["VerifiableCredential", "NationalIDCredential"],
  "issuer": "did:polygonid:example-issuer-did",
  "issuanceDate": "2024-09-08T19:37:14Z",
  "credentialSubject": {
    "id": "did:polygonid:example-holder-did",
    "name": "John Doe",
    "dateOfBirth": "1985-01-01",
    "nationalIDNumber": "123456789",
    "dateOfIssue": "2020-05-15",
    "expiryDate": "2030-05-15",
    "photo": "data:image/jpeg;base64,..."
  },
  "proof": {
    "type": "Ed25519Signature2018",
    "created": "2024-09-08T19:37:14Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:polygonid:example-issuer-did#keys-1",
    "jws": "..."
  }
}
```

## Common Elements Across All Credentials
__@context__: Defines the contexts (in this case, W3C Verifiable Credentials context) that give meaning to the terms used in the credential.
__type__: Specifies the type(s) of the credential. This is important for interoperability.
__issuer__: The DID of the entity that issued the credential.
__credentialSubject__: Contains the claims about the subject (e.g., individual, business).
__issuanceDate__: The date when the credential was issued.
__proof__: A cryptographic proof (e.g., a digital signature) that binds the credential to the issuer.

## Credential Proof
The proof section of a Verifiable Credential is a crucial component that ensures the integrity and authenticity of the credential. It includes:
__type__: The type of proof (e.g., Ed25519Signature2018).
__created__: The date and time when the proof was created.
__proofPurpose__: The intended purpose of the proof, typically assertionMethod for Verifiable Credentials.
__verificationMethod__: A reference to the cryptographic key used to generate the proof.
__jws__: The actual signature or proof, typically in JWS (JSON Web Signature) format.

## Schema Registration and Use
Schema ID: Each schema should have a unique identifier (e.g., did:polygonid:schema:12345), which allows for consistent referencing in the ecosystem.
Publishing the Schema: The schema should be published in a decentralized registry or schema repository (e.g., a blockchain or DLT), making it discoverable and reusable by others.

## Verification Process:
When verifying a credential, the verifier will check the schema ID to understand the structure and attributes expected in the credential.
The verifier will also validate the cryptographic proof to ensure the credential hasn't been tampered with and was issued by a legitimate issuer.
