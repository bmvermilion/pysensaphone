from distutils.core import setup

setup(
    name='pysensaphone',
    version='0.2',
    author='Brian Vermilion',
    author_email='brian.vermilion@gmail.com',
    url='https://github.com/bmvermilion/pysensaphone',
    packages=['pysensaphone',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Interface for Sensaphone Sentinel Rest API',
    long_description=open('README.txt').read(),
    package_data={'pysensaphone': ['encrypted_controls.pem']},
    #install_requires=['requests',
    #                  'boto3'
    #                  ]
)
