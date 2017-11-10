from codecs import open
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.readlines()


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='wechatpay',
    version='0.1',
    description='SDK for WeChat Pay.',
    long_description=long_description,
    url='https://github.com/MidTin/WeChatPay',

    author='midtin',
    author_email='midtin@gmail.com',

    license='GPL',

    classifiers=[
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    install_requires=requirements
)
