from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in easy_invoice/__init__.py
from easy_invoice import __version__ as version

setup(
	name="easy_invoice",
	version=version,
	description="Makes Sharing and assessing Invoices easier by generating unique QR codes",
	author="Muhammed Sinan K T",
	author_email="muhamsinankt@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
