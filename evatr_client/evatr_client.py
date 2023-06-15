import requests

from dataclasses import asdict
from urllib.parse import urlencode
from xml.etree.ElementTree import fromstring

from util import ISimpleParams, IQualifiedParams, ISimpleResult, IQualifiedResult, get_error_description, get_result_description

class EvatrClient:
    def retrieve_xml(self, params: ISimpleParams | IQualifiedParams, qualified: bool = False) -> str:
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
        
    def map_xml_response_data(self, raw_xml: str):
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

    def parse_xml_response(self, raw_xml: str, qualified: bool = False, include_raw_xml: bool = False) -> ISimpleResult | IQualifiedResult:   
        response = self.map_xml_response_data(raw_xml)

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
            error_description=get_error_description(error_code),
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
                result_name_description=get_result_description(result_name),
                result_city_description=get_result_description(result_city),
                result_zip_description=get_result_description(result_zip),
                result_street_description=get_result_description(result_street)
            )

        return result


    def check_simple(self, params: ISimpleParams):
        xml = self.retrieve_xml(params, qualified=False)
        return self.parse_xml_response(xml, qualified=False, include_raw_xml=params.include_raw_xml)


    def check_qualified(self, params: IQualifiedParams):
        xml = self.retrieve_xml(params, qualified=True)
        return self.parse_xml_response(xml, qualified=True, include_raw_xml=params.include_raw_xml)