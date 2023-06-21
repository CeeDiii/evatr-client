from enum import Enum

from .status_codes import status_codes

class ResultType(Enum):
    MATCH = 'A',
    NO_MATCH = 'B',
    NOT_QUERIED = 'C',
    NOT_RETURNED = 'D',

def get_result_description(result_type):
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
    
def get_error_description(error_code: int):
    '''
    Get the description for a specific error code.

    Args:
        error_code (int): The error code.

    Returns:
        str: The description of the error code.

    '''
    if str(error_code) in status_codes:
       return status_codes[str(error_code)]
    return 'Beschreibung für diesen Code wurde nicht gefunden.'
