# Python eVatR Client
A Python client for simple and qualified VAT-number validations. 

This is a Python port of the Typescript client that can be found here: https://github.com/qqilihq/evatr/tree/master

The API is provided by the German “Bundeszentralamt für Steuern”.

To use this tool, you need to be in possession of a valid German VAT number.

## Usage
```python
client = EvatrClient()

simpleParams: ISimpleParams = ISimpleParams(include_raw_xml=False,
                                                own_vat_number='<your own VAT number>', 
                                                validate_vat_number='<the VAT number to validate>')

client.check_simple(simpleParams)

qualifiedParams: IQualifiedParams = IQualifiedParams(include_raw_xml=False,
                                                own_vat_number='<your own VAT number>', 
                                                validate_vat_number='<the VAT number to validate>', 
                                                company_name='<SomeCompany Srl>', 
                                                city='Milano', 
                                                zip='20123', 
                                                street='Via Italia 22')

client.check_qualified(qualifiedParams)

```

## Installation
The source code is currently hosted on GitHub at: https://github.com/CeeDiii/evatr-client

The Python package is available at Python Package Index (PyPI)

```
pip install evatr-client
```
## Development

Install dependecies from the `requirements.txt` file:

```shell
pip install -r requirements.txt
```

## Contributing 
Feel free to open issues and pull requests in this repo.

## License




