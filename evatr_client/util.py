from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .status_codes import status_codes

class ResultType(Enum):
    MATCH = 'A',
    NO_MATCH = 'B',
    NOT_QUERIED = 'C',
    NOT_RETURNED = 'D',

@dataclass
class ISimpleParams:
    '''
    Parameters for a simple VAT number check.

    Args:
        include_raw_xml (bool): Whether to include the raw XML response in the result.
        own_vat_number (str): The VAT number used for validation.
        validate_vat_number (str): The VAT number to validate.

    '''
    include_raw_xml: bool
    own_vat_number: str
    validate_vat_number: str


@dataclass
class IQualifiedParams(ISimpleParams):
    '''
    Parameters for a qualified VAT number check.

    Args:
        include_raw_xml (bool): Whether to include the raw XML response in the result.
        own_vat_number (str): The VAT number used for validation.
        validate_vat_number (str): The VAT number to validate.
        company_name (str): The name of the company to validate.
        city (str): The city of the company to validate.
        zip (Optional[str]): The zip code of the company to validate (optional).
        street (Optional[str]): The street of the company to validate (optional).
    
    '''
    company_name: str
    city: str
    zip: Optional[str] = None
    street: Optional[str] = None


@dataclass
class ISimpleResult:
    '''
    Result of a simple VAT number check.

    Args:
        valid (bool): Indicates whether the VAT number is valid.
        date (str): The date of the check.
        time (str): The time of the check.
        error_code (int): The error code of the check.
        error_description (str): The description of the error.
        own_vat_number (str): The VAT number that was used for validation.
        validated_vat_number (str): The VAT number that was validated.
        valid_from (Optional[str]): The start date of the VAT number validity (optional).
        valid_until (Optional[str]): The end date of the VAT number validity (optional).
        raw_xml (Optional[str]): The raw XML response (optional).

    '''
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
    '''
    Result of a qualified VAT number check.

    Args:
    Result of a simple VAT number check.

    Args:
        valid (bool): Indicates whether the VAT number is valid.
        date (str): The date of the check.
        time (str): The time of the check.
        error_code (int): The error code of the check.
        error_description (str): The description of the error.
        own_vat_number (str): The VAT number that was used for validation.
        validated_vat_number (str): The VAT number that was validated.
        valid_from (Optional[str]): The start date of the VAT number validity (optional).
        valid_until (Optional[str]): The end date of the VAT number validity (optional).
        raw_xml (Optional[str]): The raw XML response (optional).
        company_name (Optional[str]): The name of the company (optional).
        city (Optional[str]): The city where the company is located (optional).
        zip (Optional[str]): The postal code of the company (optional).
        street (Optional[str]): The street address of the company (optional).
        result_name (Optional[ResultType]): The result of the name validation (optional).
        result_city (Optional[ResultType]): The result of the city validation (optional).
        result_zip (Optional[ResultType]): The result of the postal code validation (optional).
        result_street (Optional[ResultType]): The result of the street address validation (optional).
        result_name_description (Optional[str]): The description of the name validation result (optional).
        result_city_description (Optional[str]): The description of the city validation result (optional).
        result_zip_description (Optional[str]): The description of the zip code validation result (optional).
        result_street_description (Optional[str]): The description of the street address validation result (optional).

    '''
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

def _get_result_description(result_type):
    '''
    Get the description for a specific result type.

    Args:
        result_type (ResultType): The result type.

    Returns:
        str: The description of the result type.

    '''
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
    
def _get_error_description(error_code: int):
    '''
    Get the description for a specific error code.

    Args:
        error_code (int): The error code.

    Returns:
        str: The description of the error code.

    '''
    if error_code in status_codes:
       return status_codes[error_code]
    return 'Description not found for the given code.'
