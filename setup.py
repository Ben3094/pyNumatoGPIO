from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = [line.strip() for line in fh.readlines()]

setup(
    name='pyNumatoGPIO',
    version='0.0.1',
    author='Benjamin SAGGIN',
    description='An abstraction library for Numato GPIO device',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Ben3094/pyNumatoGPIO',
    project_urls = {
        "Bug Tracker": "https://github.com/Ben3094/pyNumatoGPIO/issues"
    },
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
)