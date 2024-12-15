import sys

sys.path.append("./")

from src.response_engine.status_codes import StatusCodes


class ScriptAnalysisResponse:

    BAD_REQUEST = {
        "statusCode": StatusCodes.BAD_REQUEST,
        "body": {
            "status": "BAD REQUEST",
            "message": "Script cannot be processed due to a client-side error.",
            "details": None,
        },
    }

    APPROVED = {
        "statusCode": StatusCodes.SUCCESS,
        "body": {
            "status": "APPROVED",
            "message": "Script passed all checks and is approved for use.",
            "details": None,
        },
    }

    REJECTED = {
        "statusCode": StatusCodes.SUCCESS,
        "body": {
            "status": "REJECTED",
            "message": "Script failed one or more checks.",
            "details": None,
        },
    }

    SERVER_ERROR = {
        "statusCode": StatusCodes.INTERNAL_SERVER_ERROR,
        "body": {
            "status": "ERROR",
            "message": "An internal error occurred while processing the script.",
            "details": None,
        },
    }
