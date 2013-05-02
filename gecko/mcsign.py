from gecko import app, logger
from M2Crypto import SMIME, BIO, Rand, X509

# Seed the PRNG.
# Rand.load_file('randpool.dat', -1)

# init signer
signer = SMIME.SMIME()
signer.load_key(app.config["PRIVATE_KEY"], app.config["SIGNER"])
cert = X509.load_cert(app.config["CERTIFICATE"])
sk = X509.X509_Stack()
sk.push(cert)
signer.set_x509_stack(sk)

def makebuf(text):
    return BIO.MemoryBuffer(text)

def sign(indata):
    # Make a MemoryBuffer of the message.
    inbuf = makebuf(indata)
    pkcs7 = signer.sign(inbuf, SMIME.PKCS7_BINARY)
    
    outbuf = BIO.MemoryBuffer()
    pkcs7.write_der(outbuf)
    return outbuf.read()
