AES Field
=============

Provides an AES field for Django that works with MySQL to do the AES encryption
and decryption in the database.

See: https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_aes-decrypt


Usage
-----

Like any other field:

    from aesfield.field import AESField

    class SomeModel(...):
        key = AESField()

Info
-------------

Uses the SECRET_KEY variable in settings.py as the AES key. To change this, override AESField().get_aes_key().

MySQL shell example:

SELECT AES_DECRYPT(field, SECRET_KEY) FROM some_table;
