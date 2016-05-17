AES Field
=============

Provides an AES field for Django that works with MySQL to do the AES encryption
and decryption in the database.

See: https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-decrypt

Credit:

* Kumar McMillan did a lot of this work.

Usage
-----

Like any other field::

    from aesfield.field import AESField

    class SomeModel(...):
        key = AESField()

Configuration
-------------

This AESField takes no additional parameters beyond a normal CharField. The SECRET_KEY is used in encryption and decryption.

Settings:

* `SECRET_KEY`: Used for encryption and decryption.
