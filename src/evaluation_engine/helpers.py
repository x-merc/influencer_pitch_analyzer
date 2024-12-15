import sys
from typing import List

sys.path.append("./")


def extract_section(text: str, section_name: str) -> str:
    """Extract specific section from OpenAI response"""
    try:
        # Look for section headers in different formats
        patterns = [
            f"{section_name}:",
            f"{section_name.title()}:",
            f"{section_name.upper()}:",
            f"{section_name}",
            f"{section_name.title()}",
            f"{section_name.upper()}",
        ]

        for pattern in patterns:
            if pattern in text:
                section_text = text.split(pattern)[1].split("\n\n")[0]
                return section_text.strip()

        return ""

    except Exception:
        return ""


def extract_feedback(text: str) -> str:
    """Extract feedback from section text"""
    try:
        if "feedback:" in text.lower():
            return text.split("feedback:")[1].split("\n")[0].strip()
        return text.strip()
    except Exception:
        return text


def extract_suggestions(text: str) -> List[str]:
    """Extract suggestions from section text"""
    try:
        suggestions = []
        if "suggestions:" in text.lower():
            suggestions_text = text.split("suggestions:")[1]
            # Split by newlines or bullet points
            for line in suggestions_text.split("\n"):
                if line.strip() and not line.strip().startswith(
                    ("suggestions:", "Suggestions:")
                ):
                    # Clean up bullet points and numbering
                    clean_line = line.strip().lstrip("•-*123456789.)")
                    if clean_line:
                        suggestions.append(clean_line.strip())
        return suggestions
    except Exception:
        return []


def extract_severity(text: str) -> str:
    """Extract severity level from text"""
    try:
        if "severity:" in text.lower():
            severity = text.split("severity:")[1].split("\n")[0].strip().lower()
            return severity if severity in ["low", "medium", "high"] else "medium"
        return "medium"
    except Exception:
        return "medium"


def check_section_requirements(section: str, text: str) -> bool:
    """Check if a section meets its specific requirements"""
    requirements = {
        "introduction": ["tool", "creative", "projects"],
        "personal_usage": ["using", "project", "board"],
        "feature_descriptions": ["template", "collaborate", "organize"],
        "audience_benefits": ["can use", "perfect for", "designed for"],
        "call_to_action": ["free", "sign up", "description"],
    }

    if section in requirements:
        return any(keyword in text.lower() for keyword in requirements[section])
    return True
