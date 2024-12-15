import asyncio
import sys

sys.path.append("./")

from evaluation_engine.script_analysis import ScriptAnalyzer
from evaluation_engine.script_submission import ScriptSubmission

script_content = """script content"""

OPEN_API_KEY = "api-key"


async def main():
    # Initialize ScriptAnalyzer with an OpenAI API key
    analyzer = ScriptAnalyzer(openai_api_key=OPEN_API_KEY)

    # Create a script submission object
    submission = ScriptSubmission(content=script_content, creator_name="ani")

    # Analyze the script
    results = await analyzer.analyze_script(submission)
    print(
        f"Raw Results:\n{results}",
    )

    # Print the analysis results
    print("Analysis Results:")
    print(f"Status: {results['status']}")
    print("Details:")
    for category, analysis_results in results["details"].items():
        print(f"\nCategory: {category}")
        for result in analysis_results:
            print(f"  Criteria: {result.criteria}")
            print(f"  Passed: {result.passed}")
            print(f"  Feedback: {result.feedback}")
            if result.suggestions:
                print(f"  Suggestions: {', '.join(result.suggestions)}")
            if hasattr(result, "severity") and result.severity:
                print(f"  Severity: {result.severity}")


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
