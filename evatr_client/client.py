import requests

from dataclasses import asdict
from typing import Dict
from urllib.parse import urlencode
from xml.etree.ElementTree import fromstring

from .util import ISimpleParams, IQualifiedParams, ISimpleResult, IQualifiedResult, _get_error_description, _get_result_description

class EvatrClient:
    '''
    A client for making requests to the eVatR service and parsing the XML responses.

    This client provides methods to retrieve XML data from the eVatR RPC-API and parse the responses into simple or qualified result objects.
    
    A detailed definition of this API can be found here (link in German):
    https://evatr.bff-online.de/eVatR/xmlrpc/
    
    '''
    def _retrieve_xml(self, params: ISimpleParams | IQualifiedParams, qualified: bool = False) -> str:
        '''
        Retrieves XML data from the eVatR service based on the provided parameters.

        Args:
            params (ISimpleParams | IQualifiedParams): The parameters to be included in the request.
            qualified (bool, optional): Indicates whether the request should include qualified parameters. Defaults to False.

        Returns:
            str: The XML data retrieved from the eVatR service.

        Raises:
            AttributeError: If the `params` argument is None.
        
        '''
        if params is None:
            raise AttributeError()

        query = {
            'UstId_1': params.own_vat_number,
            'UstId_2': params.validate_vat_number
        }

        if qualified:
            query['Firmenname'] = params.company_name
            query['Ort'] = params.city
            query['PLZ'] = params.zip
            query['Strasse'] = params.street

        requestUrl = f'https://evatr.bff-online.de/evatrRPC?{urlencode(query)}'
        res = requests.get(requestUrl)

        if res.ok:
            return res.text
        else:
            raise Exception()
        
    def _map_xml_response_data(self, raw_xml: str) -> Dict:
        '''
        Maps the XML response data to a dictionary.

        Args:
            raw_xml (str): The raw XML response data.

        Returns:
            dict: A dictionary containing the mapped response data.

        '''
        root = fromstring(raw_xml)
        params = root.findall('.//param')
        label = []
        values = []
        for param in params:
            val_tag = param.findall('.//string')
            if len(val_tag) >= 2:
                label.append(val_tag[0].text)
                values.append(val_tag[1].text)
        response = dict(zip(label, values))
        return response

    def _parse_xml_response(self, raw_xml: str, qualified: bool = False, include_raw_xml: bool = False) -> ISimpleResult | IQualifiedResult:   
        '''
        Parses the XML response into a simple or qualified result object.

        Args:
            raw_xml (str): The raw XML response data.
            qualified (bool, optional): Indicates whether the response should be parsed as a qualified result. Defaults to False.
            include_raw_xml (bool, optional): Indicates whether to include the raw XML in the result object. Defaults to False.

        Returns:
            ISimpleResult | IQualifiedResult: The parsed result object.
        
        '''
        response = self._map_xml_response_data(raw_xml)

        error_code = int(response['ErrorCode'])
        result_name = response['Erg_Name']
        result_city = response['Erg_Ort']
        result_zip = response['Erg_PLZ']
        result_street = response['Erg_Str']

        result = ISimpleResult(
            valid=error_code == 200,
            date=response['Datum'],
            time=response['Uhrzeit'],
            error_code=response['ErrorCode'],
            error_description=_get_error_description(error_code),
            own_vat_number=response['UstId_1'],
            validated_vat_number=response['UstId_2'],
            valid_from=response['Gueltig_ab'],
            valid_until=response['Gueltig_bis'],
            raw_xml=raw_xml if include_raw_xml else None
        )

        if qualified:
            result = IQualifiedResult(
                *asdict(result).values(),
                company_name=response['Firmenname'],
                city=response['Ort'],
                zip=response['PLZ'],
                street=response['Strasse'],
                result_name=result_name,
                result_city=result_city,
                result_zip=result_zip,
                result_street=result_street,
                result_name_description=_get_result_description(result_name),
                result_city_description=_get_result_description(result_city),
                result_zip_description=_get_result_description(result_zip),
                result_street_description=_get_result_description(result_street)
            )

        return result


    def check_simple(self, params: ISimpleParams):
        '''
        Performs a simple VAT number check using the provided parameters.

        Args:
            params (ISimpleParams): The parameters for the simple VAT number check.

        Returns:
            ISimpleResult: The result of the simple VAT number check.
        
        For more information, see (link in German):
        https://evatr.bff-online.de/eVatR/xmlrpc/schnittstelle
        
        '''
        xml = self._retrieve_xml(params, qualified=False)
        return self._parse_xml_response(xml, qualified=False, include_raw_xml=params.include_raw_xml)


    def check_qualified(self, params: IQualifiedParams):
        '''
        Performs a qualified VAT number check using the provided parameters.

        Args:
            params (IQualifiedParams): The parameters for the qualified VAT number check.

        Returns:
            IQualifiedResult: The result of the qualified VAT number check.
        
        For more information, see (link in German):
        https://evatr.bff-online.de/eVatR/xmlrpc/schnittstelle
        
        '''
        xml = self._retrieve_xml(params, qualified=True)
        return self._parse_xml_response(xml, qualified=True, include_raw_xml=params.include_raw_xml)