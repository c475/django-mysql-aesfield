from django.conf import settings
from django.db import models
from django.db import connection as django_connection


class EncryptionError(Exception):
    pass


class AESField(models.Field):

    def __init__(self, *args, **kwargs):
        super(AESField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'blob'

    def get_aes_key(self):
        return settings.SECRET_KEY

    def get_prep_lookup(self, *args, **kwargs):
        raise EncryptionError('You cannot do lookups on an encrypted field.')

    def get_db_prep_lookup(self, *args, **kwargs):
        raise EncryptionError('You cannot do lookups on an encrypted field.')

    def from_db_value(self, value, exp, conn, context):
        if value is None:
            return value

        with conn.cursor() as c:
            c.execute(
                'SELECT AES_DECRYPT(%s, %s)',
                (value, self.get_aes_key())
            )

            try:
                value = c.fetchone()[0]
            except:
                value = None

        return value

    def to_python(self, value):
        if value is None:
            return value

        with django_connection.cursor() as c:
            c.execute(
                'SELECT AES_DECRYPT(%s, %s)',
                (value, self.get_aes_key())
            )

            try:
                value = c.fetchone()[0]
            except:
                value = None

        return value

    def get_prep_value(self, value):
        if value is None:
            return value

        with django_connection.cursor() as c:
            c.execute(
                'SELECT AES_ENCRYPT(%s, %s)',
                (value, self.get_aes_key())
            )

            try:
                value = django_connection.Database.Binary(c.fetchone()[0])
            except:
                value = None

        return value

    def get_db_prep_value(self, value, conn, prepared=False):
        if value is None:
            EncryptionError('Cannot serialize "None" value')

        with conn.cursor() as c:

            c.execute(
                'SELECT AES_ENCRYPT(%s, %s)',
                (value, self.get_aes_key())
            )

            value = c.fetchone()[0]

        return value

    def get_db_prep_save(self, value, connection):
        if value is None:
            EncryptionError('Cannot serialize "None" value')

        with connection.cursor() as c:

            c.execute(
                'SELECT AES_ENCRYPT(%s, %s)',
                (value, self.get_aes_key())
            )

            value = c.fetchone()[0]

        return value
