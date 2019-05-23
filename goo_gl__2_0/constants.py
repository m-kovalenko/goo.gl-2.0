from re import compile


class BlankConstants:
    JSON_STATUS_OK = 0
    JSON_STATUS_INVALID_INPUT = 1
    JSON_STATUS_INTERNAL_ERROR = 2
    JSON_STATUS_DATA_NOT_FOUND = 3
    JSON_STATUSES = {
        0: {
            'code': 0,
            'text': 'ok'
        },
        1: {
            'code': 1,
            'text': 'invalid input'
        },
        2: {
            'code': 2,
            'text': 'internal error'
        },
        3: {
            'code': 4,
            'text': 'data not found'
        }
    }

    NUMB_SYSTEM_MAP = (
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
        'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    )

    URL_VALIDATE_REGEX = compile(
        r"^(?:(?:https?|ftp)://)(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)"
        r"(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2"
        r"[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]"
        r"\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:"
        r"[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))"
        r"(?::\d{2,5})?(?:/\S*)?$")
    PARTIAL_HTTP_REGEX = compile(r'^[htps:f]*?/+')
