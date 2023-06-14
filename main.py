
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
from urllib.parse import urlencode

import requests

class ResultType(Enum):
    MATCH = 'A',
    NO_MATCH = 'B',
    NOT_QUERIED = 'C',
    NOT_RETURNED = 'D',

@dataclass
class ISimpleParams:
    includeRawXml: bool
    ownVatNumber: str
    validateVatNumber: str


@dataclass
class IQualifiedParams(ISimpleParams):
    companyName: str
    city: str
    zip: Optional[str] = None
    street: Optional[str] = None

@dataclass
class ISimpleResult:
    # `true` if the given data was valid (i.e. error code is `200`). */
    valid: bool
    date: str
    time: str
    errorCode: int
    # Human-readable (well, German) error description.
    # The text is extracted from [here](https://evatr.bff-online.de/eVatR/xmlrpc/codes). */
    errorDescription: str
    ownVatNumber: str
    validatedVatNumber: str
    validFrom: Optional[str] = None
    validUntil: Optional[str] = None
    rawXml: Optional[str] = None

@dataclass
class IQualifiedResult(ISimpleResult):
    companyName: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    street: Optional[str] = None
    resultName: Optional[ResultType] = ResultType.NOT_RETURNED
    resultCity: Optional[ResultType] = ResultType.NOT_RETURNED
    resultZip: Optional[ResultType] = ResultType.NOT_RETURNED
    resultStreet: Optional[ResultType] = ResultType.NOT_RETURNED
    # Human-readable, German description for the name result.
    # The text is extracted from [here](https://evatr.bff-online.de/eVatR/xmlrpc/aufbau).
    resultNameDescription: Optional[str] = None
    # Human-readable, German description for the city result.
    # The text is extracted from [here](https://evatr.bff-online.de/eVatR/xmlrpc/aufbau).
    resultCityDescription: Optional[str] = None
    # Human-readable, German description for the zip result.
    # The text is extrated from [here](https://evatr.bff-online.de/eVatR/xmlrpc/aufbau). */
    resultZipDescription: Optional[str] = None
    # Human-readable, German description for the street result.
    # The text is extrated from [here](https://evatr.bff-online.de/eVatR/xmlrpc/aufbau). */
    resultStreetDescription: Optional[str] = None

def retrieveXml(params: ISimpleParams | IQualifiedParams, qualified: bool = False) -> str:
    if params is None:
        raise AttributeError()
    
    query: Tuple[str, str] = {
        'UstId_1': params.ownVatNumber,
        'UstId_2': params.validateVatNumber
    }

    if qualified:
        query['Firmenname'] = params.companyName
        query['Ort'] = params.city
        query['PLZ'] = params.zip
        query['Strasse'] = params.street

    requestUrl: str = f'https://evatr.bff-online.de/evatrRPC?{urlencode(query)}'
    res = requests.get(requestUrl)
    if res.ok:
        return res.text
    else:
        raise Exception()

def main():
    params: IQualifiedParams = IQualifiedParams(includeRawXml=False,
                                                 ownVatNumber='DE173010519', 
                                                 validateVatNumber='IT08266280968', 
                                                 companyName='I.G.M Resins Italia Srl', 
                                                 city='Milano', 
                                                 zip='20123', 
                                                 street='Corso Magenta 82')
    xmlStr = retrieveXml(params, qualified=True)
    root = ET.fromstring(xmlStr)
    params = root.findall('.//param')
    results: ISimpleResult | IQualifiedResult
    for param in params:
        values = param.findall('.//string')
        if len(values) >= 2:
            third_value = values[1].text
            print(third_value)


if __name__ == '__main__':
    main()



    






