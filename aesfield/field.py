from django.conf import settings
from django.db import models
from django.db import connection


class EncryptedField(Exception):
    pass


class AESField(models.CharField):

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(AESField, self).__init__(*args, **kwargs)

    def get_aes_key(self):
        return settings.SECRET_KEY

    def get_prep_lookup(self, type, value):
        raise EncryptedField('You cannot do lookups on an encrypted field.')

    def get_db_prep_lookup(self, *args, **kw):
        raise EncryptedField('You cannot do lookups on an encrypted field.')

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared and value:

            cursor = connection.cursor()

            cursor.execute(
                'SELECT AES_ENCRYPT(%s, %s)',
                (value, self.get_aes_key())
            )

            value = cursor.fetchone()[0]

        return value

    def to_python(self, value):
        if not value:
            return value

        cursor = connection.cursor()

        cursor.execute(
            'SELECT AES_DECRYPT(%s, %s)',
            (value, self.get_aes_key())
        )

        res = cursor.fetchone()[0]

        if res:
            value = res

        return value
