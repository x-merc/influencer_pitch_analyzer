import sys

sys.path.append("./")

from src.response_engine.script_analysis_response import ScriptAnalysisResponse


def details_formatting(details):
    details_dict = {}
    for criteria, list_of_results in details.items():
        details_dict[criteria] = []
        for result in list_of_results:
            details_dict[criteria].append(result.to_dict())
    return details_dict


class ScriptAnalysisResponseHandler:

    @staticmethod
    def bad_request(details=None):
        response = ScriptAnalysisResponse.BAD_REQUEST.copy()
        response["body"]["details"] = details
        return response

    @staticmethod
    def success(details=None):
        response = ScriptAnalysisResponse.APPROVED.copy()
        response["body"]["details"] = details_formatting(details)
        return response

    @staticmethod
    def rejection(details=None):
        response = ScriptAnalysisResponse.REJECTED.copy()
        response["body"]["details"] = details_formatting(details)
        return response

    @staticmethod
    def error(details=None):
        response = ScriptAnalysisResponse.SERVER_ERROR.copy()
        response["body"]["details"] = details
        return response
