const crypto = require('crypto');

const key = crypto.randomBytes(16);

function encryptToken(state) {
  const token = JSON.stringify(state);
  const cipher = crypto.createCipheriv('aes-128-ecb', key, null);
  cipher.setAutoPadding(true);
  const encryptedToken = Buffer.concat([
    cipher.update(token),
    cipher.final()
  ]);
  return encryptedToken.toString('hex');
}

function decryptToken(encryptedTokenHex) {
  const encryptedToken = Buffer.from(encryptedTokenHex, 'hex');
  const decipher = crypto.createDecipheriv('aes-128-ecb', key, null);
  decipher.setAutoPadding(true);
  const token = Buffer.concat([
    decipher.update(encryptedToken),
    decipher.final()
  ]).toString();
  const state = JSON.parse(token);
  return { token, state };
}

module.exports = {
  encryptToken,
  decryptToken
};
