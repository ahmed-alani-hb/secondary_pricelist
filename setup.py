from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="secondary_pricelist",
    version="1.0.0",
    description="Adds secondary pricelist functionality to Sales Order",
    author="Your Company",
    author_email="support@yourcompany.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)