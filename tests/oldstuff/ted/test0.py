import pgpy
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

# we can start by generating a primary key. For this example, we'll use RSA, but it could be DSA or ECDSA as well
key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)

# we now have some key material, but our new key doesn't have a user ID yet, and therefore is not yet usable!
uid = pgpy.PGPUID.new('Abraham Lincoln', comment='Honest Abe', email='abraham.lincoln@whitehouse.gov')

# now we must add the new user id to the key. We'll need to specify all of our preferences at this point
# because PGPy doesn't have any built-in key preference defaults at this time
# this example is similar to GnuPG 2.1.x defaults, with no expiration or preferred keyserver
key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
            ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
            compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed])
print(key)

# assuming we already have a primary key, we can generate a new key and add it as a subkey thusly:
subkey = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)

# preferences that are specific to the subkey can be chosen here
# any preference(s) needed for actions by this subkey that not specified here
# will seamlessly "inherit" from those specified on the selected User ID
key.add_subkey(subkey, usage={KeyFlags.Authentication})

print(subkey)

# A new, empty PGPkey object can be instantiated, but this is not very useful
# by itself.
# ASCII or binary data can be parsed into an empty PGPKey object with the .parse()
# method
empty_key = pgpy.PGPKey()
empty_key.parse(keyblob)
key, _ = pgpy.PGPKey.from_file('path/to/key.asc)

# A key can be loaded from a file, like so:
#key, _ = pgpy.PGPKey.from_file('path/to/key.asc')

# or from a text or binary string/bytes/bytearray that has already been read in:
key, _ = pgpy.PGPKey.from_blob(keyblob)
