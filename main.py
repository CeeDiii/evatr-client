import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, Tuple, List, Dict
from urllib.parse import urlencode

import requests

class ResultType(Enum):
    MATCH = 'A',
    NO_MATCH = 'B',
    NOT_QUERIED = 'C',
    NOT_RETURNED = 'D',

@dataclass
class ISimpleParams:
    include_raw_xml: bool
    own_vat_number: str
    validate_vat_number: str


@dataclass
class IQualifiedParams(ISimpleParams):
    company_name: str
    city: str
    zip: Optional[str] = None
    street: Optional[str] = None

@dataclass
class ISimpleResult:
    # `true` if the given data was valid (i.e. error code is `200`). */
    valid: bool
    date: str
    time: str
    error_code: int
    # Human-readable (well, German) error description.
    # The text is extracted from [here](https://evatr.bff-online.de/eVatR/xmlrpc/codes). */
    error_description: str
    own_vat_number: str
    validated_vat_number: str
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    raw_xml: Optional[str] = None

@dataclass
class IQualifiedResult(ISimpleResult):
    company_name: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    street: Optional[str] = None
    result_name: Optional[ResultType] = ResultType.NOT_QUERIED
    result_city: Optional[ResultType] = ResultType.NOT_QUERIED
    result_zip: Optional[ResultType] = ResultType.NOT_QUERIED
    result_street: Optional[ResultType] = ResultType.NOT_QUERIED
    # Human-readable, German description for the name result.
    # The text is extracted from [here](https://evatr.bff-online.de/eVatR/xmlrpc/aufbau).
    result_name_description: Optional[str] = None
    # Human-readable, German description for the city result.
    # The text is extracted from [here](https://evatr.bff-online.de/eVatR/xmlrpc/aufbau).
    result_city_description: Optional[str] = None
    # Human-readable, German description for the zip result.
    # The text is extrated from [here](https://evatr.bff-online.de/eVatR/xmlrpc/aufbau). */
    result_zip_description: Optional[str] = None
    # Human-readable, German description for the street result.
    # The text is extrated from [here](https://evatr.bff-online.de/eVatR/xmlrpc/aufbau). */
    result_street_description: Optional[str] = None

def retrieve_xml(params: ISimpleParams | IQualifiedParams, qualified: bool = False) -> str:
    if params is None:
        raise AttributeError()
    
    query: Tuple[str, str] = {
        'UstId_1': params.own_vat_number,
        'UstId_2': params.validate_vat_number
    }

    if qualified:
        query['Firmenname'] = params.company_name
        query['Ort'] = params.city
        query['PLZ'] = params.zip
        query['Strasse'] = params.street

    requestUrl: str = f'https://evatr.bff-online.de/evatrRPC?{urlencode(query)}'
    res = requests.get(requestUrl)
    if res.ok:
        return res.text
    else:
        raise Exception()
    
def map_xml_response_data(raw_xml: str) -> Dict:
    root = ET.fromstring(raw_xml)
    params = root.findall('.//param')
    label: List[str] = []
    values: List[str] = []
    for param in params:
        val_tag = param.findall('.//string')
        if len(val_tag) >= 2:
            label.append(val_tag[0].text)
            values.append(val_tag[1].text)
    response = dict(zip(label, values))
    return response
    
def get_error_description(error_code: int):
    f = open('res/error-codes.json')
    error_codes = json.load(f)
    for item in error_codes:
        if 'code' in item and item['code'] == error_code:
            return item['description']
    return 'Description not found for the given code.'

def get_result_description(result_type: ResultType) -> Optional[str]:
    if result_type == ResultType.MATCH:
        return 'stimmt überein'
    elif result_type == ResultType.NO_MATCH:
        return 'stimmt nicht überein'
    elif result_type == ResultType.NOT_QUERIED:
        return 'nicht angefragt'
    elif result_type == ResultType.NOT_RETURNED:
        return 'vom EU-Mitgliedsstaat nicht mitgeteilt'
    else:
        return None

def parse_xml_response(raw_xml: str, qualified: bool = False, include_raw_xml: bool = False) -> ISimpleResult | IQualifiedResult:
    response = map_xml_response_data(raw_xml)

    error_code = int(response['ErrorCode'])
    result_name = response['Erg_Name']
    result_city = response['Erg_Ort']
    result_zip = response['Erg_PLZ']
    result_street = response['Erg_Str']

    result: ISimpleResult = ISimpleResult(
        valid=error_code == 200,
        date=response['Datum'],
        time=response['Uhrzeit'],
        error_code=response['ErrorCode'],
        error_description=get_error_description(error_code),
        own_vat_number=response['UstId_1'],
        validated_vat_number=response['UstId_2'],
        valid_from=response['Gueltig_ab'],
        valid_until=response['Gueltig_bis'],
        raw_xml= raw_xml if include_raw_xml else None
    )

    if qualified:
        result: IQualifiedResult = IQualifiedResult(
            *asdict(result).values(),
            company_name=response['Firmenname'],
            city=response['Ort'],
            zip=response['PLZ'],
            street=response['Strasse'],
            result_name=result_name,
            result_city=result_city,
            result_zip=result_zip,
            result_street=result_street,
            result_name_description=get_result_description(result_name),
            result_city_description=get_result_description(result_city),
            result_zip_description=get_result_description(result_zip),
            result_street_description=get_result_description(result_street)
        )

    return result
    
def check_simple(params: ISimpleParams):
    xml: str = retrieve_xml(params, qualified=False)
    return parse_xml_response(xml, qualified=False, include_raw_xml=params.include_raw_xml)

def check_qualified(params: IQualifiedParams):
    xml: str = retrieve_xml(params, qualified=True)
    return parse_xml_response(xml, qualified=True, include_raw_xml=params.include_raw_xml)

def main():
    params: IQualifiedParams = IQualifiedParams(include_raw_xml=False,
                                                 own_vat_number='DE173010519', 
                                                 validate_vat_number='IT08266280968', 
                                                 company_name='I.G.M Resins Italia Srl', 
                                                 city='Milano', 
                                                 zip='20123', 
                                                 street='Corso Magenta 82')
    print(check_qualified(params))


            

if __name__ == '__main__':
    main()



    






