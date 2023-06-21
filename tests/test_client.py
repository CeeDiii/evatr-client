import unittest
from unittest.mock import patch
from urllib.parse import urlencode
from evatr_client import EvatrClient, ISimpleParams, IQualifiedParams, ISimpleResult, IQualifiedResult

class TestClient(unittest.TestCase):

    def setUp(self) -> None:
        self.client = EvatrClient()
        self.own_vat_number = 'DE129273398'
        self.validate_vat_number = 'CZ00177041'
        return super().setUp()

    @patch('requests.get')
    def test_retrieve_xml_simple_should_return_xml(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.ok = True
        mock_response.text = '''
        <params>
            <param>
            <value><array><data>
            <value><string>UstId_1</string></value>
            <value><string>DE142301639</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>ErrorCode</string></value>
            <value><string>200</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>UstId_2</string></value>
            <value><string>NL803157228B01</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Druck</string></value>
            <value><string>nein</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_PLZ</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Ort</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Datum</string></value>
            <value><string>18.06.2023</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>PLZ</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Ort</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Uhrzeit</string></value>
            <value><string>21:25:26</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Name</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Gueltig_ab</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Gueltig_bis</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Strasse</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Firmenname</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Str</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            </params>
        '''

        expected = '''
        <params>
            <param>
            <value><array><data>
            <value><string>UstId_1</string></value>
            <value><string>DE142301639</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>ErrorCode</string></value>
            <value><string>200</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>UstId_2</string></value>
            <value><string>NL803157228B01</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Druck</string></value>
            <value><string>nein</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_PLZ</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Ort</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Datum</string></value>
            <value><string>18.06.2023</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>PLZ</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Ort</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Uhrzeit</string></value>
            <value><string>21:25:26</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Name</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Gueltig_ab</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Gueltig_bis</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Strasse</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Firmenname</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Str</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            </params>
        '''

        params = ISimpleParams(
            include_raw_xml=False, 
            own_vat_number=self.own_vat_number, 
            validate_vat_number=self.validate_vat_number
        )

        actual = self.client._retrieve_xml(params, qualified=False)

        self.assertEqual(actual, expected)
        mock_get.assert_called_once_with(f'https://evatr.bff-online.de/evatrRPC?UstId_1={self.own_vat_number}&UstId_2={self.validate_vat_number}', timeout=15)

    @patch('requests.get')
    def test_retrieve_xml_simple_should_fail(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.ok = False

        params = ISimpleParams(
            include_raw_xml=False, 
            own_vat_number=self.own_vat_number, 
            validate_vat_number=self.validate_vat_number
        )

        with self.assertRaises(Exception):
            self.client._retrieve_xml(params, qualified=False)

        mock_get.assert_called_once_with(f'https://evatr.bff-online.de/evatrRPC?UstId_1={self.own_vat_number}&UstId_2={self.validate_vat_number}', timeout=15)

    @patch('requests.get')
    def test_retrieve_xml_params_empty_should_fail(self, mock_get):
        params = None

        with self.assertRaises(AttributeError):
            self.client._retrieve_xml(params)

        mock_get.assert_not_called()

    @patch('requests.get')
    def test_retrieve_xml_qualified_should_return_xml(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.ok = True
        mock_response.text = '''
            <params>
                <param>
                <value><array><data>
                <value><string>UstId_1</string></value>
                <value><string>DE129273398</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>ErrorCode</string></value>
                <value><string>200</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>UstId_2</string></value>
                <value><string>CZ00177041</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Druck</string></value>
                <value><string>nein</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_PLZ</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Ort</string></value>
                <value><string>Mlada Boleslav</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Datum</string></value>
                <value><string>18.06.2023</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>PLZ</string></value>
                <value><string>293 01</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Ort</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Uhrzeit</string></value>
                <value><string>13:30:27</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Name</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Gueltig_ab</string></value>
                <value><string></string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Gueltig_bis</string></value>
                <value><string></string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Strasse</string></value>
                <value><string>tř. Václava Klementa 869</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Firmenname</string></value>
                <value><string>ŠKODA AUTO a.s.</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Str</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
            </params>
        '''

        expected = '''
            <params>
                <param>
                <value><array><data>
                <value><string>UstId_1</string></value>
                <value><string>DE129273398</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>ErrorCode</string></value>
                <value><string>200</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>UstId_2</string></value>
                <value><string>CZ00177041</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Druck</string></value>
                <value><string>nein</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_PLZ</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Ort</string></value>
                <value><string>Mlada Boleslav</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Datum</string></value>
                <value><string>18.06.2023</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>PLZ</string></value>
                <value><string>293 01</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Ort</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Uhrzeit</string></value>
                <value><string>13:30:27</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Name</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Gueltig_ab</string></value>
                <value><string></string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Gueltig_bis</string></value>
                <value><string></string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Strasse</string></value>
                <value><string>tř. Václava Klementa 869</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Firmenname</string></value>
                <value><string>ŠKODA AUTO a.s.</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Str</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
            </params>
        '''

        params = IQualifiedParams(
            include_raw_xml=True,
            own_vat_number= self.own_vat_number,
            validate_vat_number= self.validate_vat_number,
            company_name= 'ŠKODA AUTO a.s.',
            city= 'Mlada Boleslav',
            zip= '293 01',
            street= 'tř. Václava Klementa 869'
        )

        query = {
            'UstId_1': params.own_vat_number,
            'UstId_2': params.validate_vat_number,
            'Firmenname': params.company_name,
            'Ort': params.city,
            'PLZ': params.zip,
            'Strasse': params.street
        }

        actual = self.client._retrieve_xml(params, qualified=True)

        self.assertEqual(actual, expected)
        mock_get.assert_called_once_with(f'https://evatr.bff-online.de/evatrRPC?{urlencode(query)}', timeout=15)

    def test_map_xml_response_data_should_return_response_dict(self):
        qualifiedResponse: str = '''
            <params>
            <param>
            <value><array><data>
            <value><string>UstId_1</string></value>
            <value><string>DE129273398</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>ErrorCode</string></value>
            <value><string>200</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>UstId_2</string></value>
            <value><string>CZ00177041</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Druck</string></value>
            <value><string>nein</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_PLZ</string></value>
            <value><string>A</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Ort</string></value>
            <value><string>Mlada Boleslav</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Datum</string></value>
            <value><string>18.06.2023</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>PLZ</string></value>
            <value><string>293 01</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Ort</string></value>
            <value><string>A</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Uhrzeit</string></value>
            <value><string>13:30:27</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Name</string></value>
            <value><string>A</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Gueltig_ab</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Gueltig_bis</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Strasse</string></value>
            <value><string>tř. Václava Klementa 869</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Firmenname</string></value>
            <value><string>ŠKODA AUTO a.s.</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Str</string></value>
            <value><string>A</string></value>
            </data></array></value>
            </param>
            </params>
            '''
        
        expected = {
                'Datum': '18.06.2023',
                'Uhrzeit': '13:30:27',
                'ErrorCode': '200',
                'UstId_1': self.own_vat_number,
                'UstId_2': self.validate_vat_number,
                'Firmenname': 'ŠKODA AUTO a.s.',
                'Ort': 'Mlada Boleslav',
                'PLZ': '293 01',
                'Strasse': 'tř. Václava Klementa 869',
                'Erg_Name': 'A',
                'Erg_Ort': 'A',
                'Erg_PLZ': 'A',
                'Erg_Str': 'A',
                'Gueltig_ab': None,
                'Gueltig_bis': None,
                'Druck': 'nein'
            }
        
        actual = self.client._map_xml_response_data(qualifiedResponse)
        
        self.assertDictEqual(actual, expected)

    def test_map_xml_response_data_should_return_empty_dict(self):
        qualifiedResponse: str = '''
            <params>
            </params>
            '''
        
        expected = {}
        
        actual = self.client._map_xml_response_data(qualifiedResponse)
        
        self.assertDictEqual(actual, expected)

    def test_parse_xml_response_simple_should_return_result(self):
        xml = '''
        <params>
            <param>
            <value><array><data>
            <value><string>UstId_1</string></value>
            <value><string>DE129273398</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>ErrorCode</string></value>
            <value><string>200</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>UstId_2</string></value>
            <value><string>CZ00177041</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Druck</string></value>
            <value><string>nein</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_PLZ</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Ort</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Datum</string></value>
            <value><string>18.06.2023</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>PLZ</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Ort</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Uhrzeit</string></value>
            <value><string>21:25:26</string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Name</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Gueltig_ab</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Gueltig_bis</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Strasse</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Firmenname</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            <param>
            <value><array><data>
            <value><string>Erg_Str</string></value>
            <value><string></string></value>
            </data></array></value>
            </param>
            </params>
        '''
        expected = ISimpleResult(
            valid=True, 
            date='18.06.2023', 
            time='21:25:26', 
            error_code='200', 
            error_description='Die angefragte USt-IdNr. ist gültig.', 
            own_vat_number=self.own_vat_number, 
            validated_vat_number=self.validate_vat_number, 
            valid_from=None, 
            valid_until=None, 
            raw_xml=None)
        
        actual = self.client._parse_xml_response(xml, qualified=False, include_raw_xml=False)
        self.assertIsInstance(actual, ISimpleResult)
        self.assertEqual(actual, expected) 

    def test_parse_xml_response_qualified_should_return_result(self):
        xml = '''
            <params>
                <param>
                <value><array><data>
                <value><string>UstId_1</string></value>
                <value><string>DE129273398</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>ErrorCode</string></value>
                <value><string>200</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>UstId_2</string></value>
                <value><string>CZ00177041</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Druck</string></value>
                <value><string>nein</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_PLZ</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Ort</string></value>
                <value><string>Mlada Boleslav</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Datum</string></value>
                <value><string>18.06.2023</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>PLZ</string></value>
                <value><string>293 01</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Ort</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Uhrzeit</string></value>
                <value><string>13:30:27</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Name</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Gueltig_ab</string></value>
                <value><string></string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Gueltig_bis</string></value>
                <value><string></string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Strasse</string></value>
                <value><string>tř. Václava Klementa 869</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Firmenname</string></value>
                <value><string>ŠKODA AUTO a.s.</string></value>
                </data></array></value>
                </param>
                <param>
                <value><array><data>
                <value><string>Erg_Str</string></value>
                <value><string>A</string></value>
                </data></array></value>
                </param>
            </params>
        '''
        expected = IQualifiedResult(
            valid=True, 
            date='18.06.2023', 
            time='13:30:27', 
            error_code='200', 
            error_description='Die angefragte USt-IdNr. ist gültig.', 
            own_vat_number=self.own_vat_number, 
            validated_vat_number=self.validate_vat_number, 
            valid_from=None, 
            valid_until=None, 
            raw_xml=None, 
            company_name='ŠKODA AUTO a.s.', 
            city='Mlada Boleslav', 
            zip='293 01', 
            street='tř. Václava Klementa 869', 
            result_name='A', 
            result_city='A', 
            result_zip='A', 
            result_street='A', 
            result_name_description=None, 
            result_city_description=None, 
            result_zip_description=None, 
            result_street_description=None)
        
        actual = self.client._parse_xml_response(xml, qualified=True, include_raw_xml=False)
        self.assertIsInstance(actual, IQualifiedResult)
        self.assertEqual(actual, expected) 


if __name__ == '__main__':
    unittest.main()