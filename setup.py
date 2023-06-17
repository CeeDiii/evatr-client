from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'A client for: https://evatr.bff-online.de/eVatR/'
LONG_DESCRIPTION = 'A client to validate EU-VAT numbers with the official German tool that can be found here: https://evatr.bff-online.de/eVatR/'

# Setting up
setup(
    name="evatr-client",
    version=VERSION,
    author="CeeDiii",
    description=DESCRIPTION,
    license='MIT',
    url='https://github.com/CeeDiii/evatr-client',
    download_url='https://github.com/CeeDiii/evatr-client/archive/refs/tags/v0.1.0.tar.gz',
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'uid', 'vat', 'uid prüfung', 'vat validation', 'evatr', 'evatr client', 'evatr python client'],
    python_requires=">=3.10",
    install_requires=[
          'requests',
          'urllib3',
          'beautifulsoup4',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
