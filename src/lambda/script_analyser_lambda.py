import json
import os
import sys

sys.path.append("./")

from src.evaluation_engine.script_analysis import ScriptAnalyzer
from src.evaluation_engine.script_submission import ScriptSubmission
from src.response_engine.script_analysis_response_handler import (
    ScriptAnalysisResponseHandler,
)


def lambda_handler(event, context):
    try:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        body = json.loads(event.get("body"))
        script_content = body.get("content", "")
        creator_name = body.get("creator_name", "")
        if not script_content or not creator_name:
            return ScriptAnalysisResponseHandler.bad_request(
                details="The request body must include 'content' and 'creator name'."
            )

        analyzer = ScriptAnalyzer(openai_api_key=openai_api_key)
        submission = ScriptSubmission(content=script_content, creator_name=creator_name)
        analysis_results = analyzer.analyze_script(submission)
        if analysis_results["status"] == "REJECTED":
            response = ScriptAnalysisResponseHandler.rejection(
                details=analysis_results.get("details")
            )
        else:
            response = ScriptAnalysisResponseHandler.success(
                details=analysis_results.get("details")
            )
        return response

    except Exception as e:
        return ScriptAnalysisResponseHandler.error(details=str(e))
