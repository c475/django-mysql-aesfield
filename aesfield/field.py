from django.conf import settings
from django.db import models
from django.db import connection


class EncryptedField(Exception):
    pass


class AESField(models.TextField):

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

            with connection.cursor() as c:

                c.execute(
                    'SELECT AES_ENCRYPT(%s, %s)',
                    (value, self.get_aes_key())
                )
    
                value = c.fetchone()[0]

        return value
        
    def from_db_value(self, value, exp, conn, context):
        if value is None:
            return value

        conn.cursor.execute(
            'SELECT AES_DECRYPT(%s, %s)',
            (value, self.get_aes_key())
        )

        try:
            res = conn.cursor.fetchone()[0]
        except:
            res = None
            
        return res

    def to_python(self, value):
        if not value:
            return value

        with connection.cursor() as c:

            c.execute(
                'SELECT AES_DECRYPT(%s, %s)',
                (value, self.get_aes_key())
            )
    
            res = c.fetchone()[0]
    
            if res:
                value = res

        return value
