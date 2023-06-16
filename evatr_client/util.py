from dataclasses import dataclass
from enum import Enum
from typing import Optional

from status_codes import status_codes

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
    valid: bool
    date: str
    time: str
    error_code: int
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
    result_name_description: Optional[str] = None
    result_city_description: Optional[str] = None
    result_zip_description: Optional[str] = None
    result_street_description: Optional[str] = None

def get_result_description(result_type):
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
    
def get_error_description(error_code: int):
    if error_code in status_codes:
       return status_codes[error_code]
    return 'Description not found for the given code.'
