from collections import defaultdict

from .status_codes import status_codes

RESULT_TYPE = defaultdict(lambda: None, {
    'A': 'stimmt überein',
    'B': 'stimmt nicht überein',
    'C': 'nicht angefragt',
    'D': 'vom EU-Mitgliedsstaat nicht mitgeteilt'
})

def get_result_description(result_type: str) -> str:
    '''
    Get the description for a specific result type.

    Args:
        result_type (ResultType): The result type.

    Returns:
        str: The description of the result type.

    '''
    return RESULT_TYPE[result_type]
    
def get_error_description(error_code: int) -> str:
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
