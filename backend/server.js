const express = require('express');
const bodyParser = require('body-parser');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { generateAuthRequest, verifyAuthResponse } = require('@iden3/js-iden3-auth');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON requests
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Set up local storage directory for uploads
const UPLOAD_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR);
}

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});

const upload = multer({ storage });

// Example DID and Credential Schema
const issuerDID = 'did:polygonid:example-issuer-did'; // Replace with your Issuer DID
const credentialSchemaID = 'example-schema-id'; // Replace with your Credential Schema ID

// API to generate an authentication request
app.get('/auth/request', (req, res) => {
  try {
    const authRequest = generateAuthRequest({
      issuer: issuerDID,
      callbackURL: `${req.protocol}://${req.get('host')}/auth/response`,
      schema: credentialSchemaID,
    });

    return res.status(200).json(authRequest);
  } catch (error) {
    console.error('Error generating auth request:', error);
    return res.status(500).json({ message: 'Internal server error' });
  }
});

// API to handle authentication response
app.post('/auth/response', async (req, res) => {
  try {
    const { authResponse } = req.body;

    const isValid = await verifyAuthResponse({
      authResponse,
      issuer: issuerDID,
    });

    return res.status(200).json({
      message: isValid ? 'Authentication successful' : 'Authentication failed',
    });
  } catch (error) {
    console.error('Error verifying auth response:', error);
    return res.status(500).json({ message: 'Internal server error' });
  }
});

app.post('/register', upload.fields([
  { name: 'nationalID', maxCount: 1 },
  { name: 'businessCertificate', maxCount: 1 },
  { name: 'kraPin', maxCount: 1 }
]), (req, res) => {
  try {
    const { email, phone } = req.body;
    const files = req.files;

    // Basic validation
    if (!email || !phone || !files.nationalID || !files.businessCertificate || !files.kraPin) {
      return res.status(400).json({ message: 'Missing required fields' });
    }

    // Ensure files are saved correctly
    const nationalIDPath = files.nationalID[0]?.path;
    const businessCertificatePath = files.businessCertificate[0]?.path;
    const kraPinPath = files.kraPin[0]?.path;

    if (!nationalIDPath || !businessCertificatePath || !kraPinPath) {
      return res.status(400).json({ message: 'Error saving files' });
    }

    // Log file paths for debugging
    console.log('Files saved to:');
    console.log('National ID:', nationalIDPath);
    console.log('Business Certificate:', businessCertificatePath);
    console.log('KRA PIN:', kraPinPath);

    // Placeholder: Implement actual verification logic here
    const isVerified = true;

    if (isVerified) {
      // Issue a verifiable credential using the relevant schema
      const credential = {
        issuer: issuerDID,
        issuanceDate: new Date().toISOString(),
        credentialSubject: {
          id: `did:polygonid:${Date.now()}`,
          nationalID: 'ID-Placeholder',
          businessCertificate: 'Certificate-Placeholder',
          kraPin: 'Pin-Placeholder'
        }
      };

      // Check and delete documents after verification
      [nationalIDPath, businessCertificatePath, kraPinPath].forEach(filePath => {
        if (fs.existsSync(filePath)) {
          fs.unlinkSync(filePath);
        } else {
          console.error(`File not found: ${filePath}`);
        }
      });

      return res.status(200).json({
        message: 'Verification successful',
        credential
      });
    } else {
      // Handle verification failure
      return res.status(400).json({ message: 'Verification failed' });
    }
  } catch (error) {
    console.error('Error during registration:', error);
    return res.status(500).json({ message: 'Internal server error' });
  }
});


// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

