from enum import Enum
import sys
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import openai

sys.path.append("./")

from src.evaluation_engine.analysis_result import AnalysisResult
from src.evaluation_engine.criteria import (
    AVOID_ELEMENTS,
    CORE_REQUIREMENTS,
    SCRIPT_FLOW,
)
from src.evaluation_engine.script_submission import ScriptSubmission
from src.evaluation_engine.helpers import (
    check_section_requirements,
    extract_feedback,
    extract_section,
    extract_severity,
    extract_suggestions,
)


class ScriptAnalyzer:
    def __init__(self, openai_api_key: str):
        self.openai_client = openai.Client(api_key=openai_api_key)

    def _check_brand_safety(self, content: str) -> List[AnalysisResult]:
        prompt = f"""
        Analyze the following script for brand safety concerns. This is critical as Milanote has strict content guidelines.

        Check for ANY presence of:
        1. Adult Content:
           - Explicit themes
           - Adult language
           - Inappropriate imagery references
           - Suggestive content

        2. Political Content:
           - Politically polarizing topics
           - Controversial political statements
           - Political bias or advocacy
           - Divisive political commentary

        3. Harassment/Attacks:
           - Personal attacks
           - Targeted harassment
           - Negative comments about individuals/groups
           - Discriminatory language

        4. Misinformation:
           - Unverified theories presented as facts
           - Conspiracy theories
           - Unsubstantiated claims
           - Misleading information

        Script:
        {content}

        For each category:
        1. Flag ANY presence of problematic content (even subtle references)
        2. Mark severity (Low/Medium/High)
        3. Quote specific problematic phrases or references
        4. Indicate if the content is completely brand-safe or needs modification

        This is a zero-tolerance check - any presence of these elements should result in immediate flagging.
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  # Lower temperature for more conservative/consistent checking
        )

        # Process the response
        analysis = response.choices[0].message.content
        return self._process_brand_safety_analysis(analysis)

    def _check_core_requirements(self, content: str) -> List[AnalysisResult]:
        prompt = f"""
        Analyze the following script for how it introduces and describes Milanote.

        Key aspects to evaluate:
        1. Introduction of Milanote:
           - Looking for descriptions that convey Milanote is a tool for organizing creative projects
           - Accept variations that capture the same meaning (e.g., "platform for organizing creative work", "creative organization tool")
           - The core message should emphasize both "organizing" and "creative projects"

        2. Product Description and Features:
           - Should have description about Milanote
           - Can be described in the creator's own words/style

        Note: The script might not contain explicit screen direction cues like "[Screen: Show Logo]" - focus on the spoken/narration content.

        Script:
        {content}

        Provide analysis of:
        1. How effectively the script introduces Milanote (quote the relevant text)
        2. Whether the core message is conveyed, even if using different phrasing
        3. Explicity state which key aspects are present or not.
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        # Process response with more flexible matching
        analysis = response.choices[0].message.content
        return self._process_core_requirements_analysis(analysis)

    def _check_script_flow(self, content: str) -> List[AnalysisResult]:
        prompt = f"""
        Analyze the following script for content flow and narrative structure. 
        Note: The script might not contain explicit screen directions - focus on the narrative content.

        Expected content elements (can be in any natural order):
        1. Introduction of Milanote
           - Should introduce the tool and its purpose

        2. Personal Usage Example
           - Should describe how the creator uses Milanote
           - Should mention specific use cases or projects
           - Visual elements like board demonstrations may be implied in the narrative

        3. Feature Descriptions
           - Should mention key features (templates, collaboration, etc.)
           - Should explain benefits in creator's own style
           - Details should be presented in an accessible way

        4. Audience Benefits
           - Should explain how viewers can use Milanote
           - May highlight the presence of existing templates for different kinds of use cases or projects
           - Should mention different use cases or user types
           - Should mention about how teams can ollaborate and share work

        5. Call to Action
           - Must encourage audience to use Milanote
           - Must mention it's free
           - Must reference sign-up process (not download)

        Script:
        {content}

        Analyze:
        1. Whether each key element is present in the narrative
        2. How naturally the elements flow together
        3. Whether the script feels authentic to the creator while covering key points
        4. Any missing essential information
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        # Process the response
        analysis = response.choices[0].message.content
        return self._process_script_flow_analysis(analysis)

    def _check_avoided_elements(self, content: str) -> List[AnalysisResult]:
        prompt = f"""
        Review the following script for problematic elements, focusing on the actual content rather than formatting or screen directions.

        Check for these issues while allowing for natural variation in expression:

        1. Content Problems:
           - Too focused on YouTube-specific content
           - Missing essential information about Milanote
           - Incorrect feature descriptions
           - Confusing or misleading explanations

        2. Tone/Style Issues:
           - Overly promotional language
           - Inauthentic or forced delivery
           - Too technical or complicated explanation

        Script:
        {content}

        Provide:
        1. Any identified issues that would hurt the effectiveness of the sponsorship
        2. Whether the script maintains authenticity while meeting requirements
        3. Suggestions for improvement that preserve the creator's voice
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        analysis = response.choices[0].message.content

        return self._process_avoided_elements_analysis(analysis)

    def _process_brand_safety_analysis(
        self, openai_response: str
    ) -> List[AnalysisResult]:
        """Process OpenAI response for brand safety analysis"""
        try:
            results = []

            # Brand safety categories
            categories = {
                "adult content": ["explicit", "inappropriate"],
                "political": ["political", "polarizing", "controversial"],
                "harassment": ["personal attack", "discriminatory"],
                "misinformation": ["unverified", "conspiracy", "misleading"],
            }

            for category, keywords in categories.items():
                category_text = extract_section(openai_response, category)
                if category_text:
                    # Any mention of issues in these categories should fail
                    has_issues = any(
                        keyword in category_text.lower() for keyword in keywords
                    )
                    severity = extract_severity(category_text)

                    results.append(
                        AnalysisResult(
                            criteria=f"{category}",
                            passed=not has_issues,
                            feedback=extract_feedback(category_text),
                            suggestions=(
                                extract_suggestions(category_text)
                                if has_issues
                                else None
                            ),
                            severity=severity if has_issues else None,
                        )
                    )

            return results

        except Exception as e:
            return [
                AnalysisResult(
                    criteria="error",
                    passed=False,
                    feedback=f"Error processing brand safety analysis: {str(e)}",
                    suggestions=["Please review script for brand safety manually"],
                )
            ]

    def _process_core_requirements_analysis(
        self, openai_response: str
    ) -> List[AnalysisResult]:
        """Process OpenAI response for core requirements analysis"""
        try:
            results = []

            # Extract introduction analysis
            if "introduction" in openai_response.lower():
                intro_text = extract_section(openai_response, "introduction")

                # Check if core message is conveyed (allowing for variations)
                core_message_conveyed = any(
                    [
                        "tool for organizing" in intro_text.lower(),
                        "creative organization" in intro_text.lower(),
                        "organize creative" in intro_text.lower(),
                        "creative projects" in intro_text.lower(),
                    ]
                )

                results.append(
                    AnalysisResult(
                        criteria="introduction",
                        passed=core_message_conveyed,
                        feedback=extract_feedback(intro_text),
                        suggestions=(
                            extract_suggestions(intro_text)
                            if not core_message_conveyed
                            else None
                        ),
                    )
                )

            # Extract product description analysis
            if "product description" in openai_response.lower():
                desc_text = extract_section(openai_response, "product description")

                # Check for key product elements
                has_canvas = any(
                    keyword in text.lower()
                    for keyword in ["canvas", "workspace", "mind map", "plan"]
                    for text in [desc_text, intro_text]
                )
                has_planning = any(
                    keyword in text.lower()
                    for keyword in ["planning", "brainstorming", "organizing"]
                    for text in [desc_text, intro_text]
                )
                has_collab = any(
                    keyword in text.lower()
                    for keyword in ["collab", "team work", "members"]
                    for text in [desc_text, intro_text]
                )

                results.append(
                    AnalysisResult(
                        criteria="product_description",
                        passed=all([has_canvas, has_planning, has_collab]),
                        feedback=extract_feedback(desc_text),
                        suggestions=(
                            extract_suggestions(desc_text)
                            if not all([has_canvas, has_planning, has_collab])
                            else None
                        ),
                    )
                )

            return results

        except Exception as e:
            return [
                AnalysisResult(
                    criteria="error",
                    passed=False,
                    feedback=f"Error processing core requirements analysis: {str(e)}",
                    suggestions=[
                        "Please review the presence of core requirements manually"
                    ],
                )
            ]

    def _process_avoided_elements_analysis(self, analysis):
        try:
            results = []

            categories = {
                "content problems": ["missing", "incorrect", "confusing"],
                "tone": ["promotional", "inauthentic", "technical"],
            }

            for category, keywords in categories.items():
                category_text = extract_section(analysis, category)
                if category_text:
                    has_issues = any(
                        keyword in category_text.lower() for keyword in keywords
                    )

                    results.append(
                        AnalysisResult(
                            criteria=f"{category}",
                            passed=not has_issues,
                            feedback=extract_feedback(category_text),
                            suggestions=(
                                extract_suggestions(category_text)
                                if has_issues
                                else None
                            ),
                        )
                    )

            return results

        except Exception as e:
            return [
                AnalysisResult(
                    criteria="error",
                    passed=False,
                    feedback=f"Error processing avoided elements analysis: {str(e)}",
                    suggestions=[
                        "Please review the presence of elements to be avoided manually"
                    ],
                )
            ]

    def _process_script_flow_analysis(
        self, openai_response: str
    ) -> List[AnalysisResult]:
        """Process OpenAI response for script flow analysis"""
        try:
            results = []

            # Expected sections in the flow
            sections = [
                "introduction",
                "personal usage",
                "feature descriptions",
                "audience benefits",
                "Call to Action",
            ]

            for section in sections:
                section_text = extract_section(openai_response, section)
                if section_text:
                    # Check section requirements based on type
                    passed = check_section_requirements(section, section_text)

                    results.append(
                        AnalysisResult(
                            criteria=f"{section}",
                            passed=passed,
                            feedback=extract_feedback(section_text),
                            suggestions=(
                                extract_suggestions(section_text)
                                if not passed
                                else None
                            ),
                        )
                    )

            return results

        except Exception as e:
            return [
                AnalysisResult(
                    criteria="error",
                    passed=False,
                    feedback=f"Error processing flow analysis: {str(e)}",
                    suggestions=["Please review the script flow manually"],
                )
            ]

    def analyze_script(
        self, submission: ScriptSubmission
    ) -> Dict[str, List[AnalysisResult]]:
        """Main analysis method that runs all checks"""
        results = {
            "brand safety": self._check_brand_safety(submission.content),
            "core requirements": self._check_core_requirements(submission.content),
            "script flow": self._check_script_flow(submission.content),
            "avoided elements": self._check_avoided_elements(submission.content),
        }

        # If any brand safety check fails, mark the entire submission as failed
        if any(not result.passed for result in results["brand safety"]):
            return {"status": "REJECTED", "details": results}

        return {"status": "APPROVED", "details": results}
