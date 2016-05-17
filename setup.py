from setuptools import setup

setup(
    name='django-mysql-aesfield',
    version='0.2.1',
    description='Django Model Field that supports AES encryption in MySQL',
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    url='https://github.com/c475/django-mysql-aesfield',
    include_package_data=True,
    zip_safe=False,
    packages=['aesfield']
)
