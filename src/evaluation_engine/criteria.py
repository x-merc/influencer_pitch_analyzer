CORE_REQUIREMENTS = {
    "introduction": {
        "rule": "Must introduce Milanote as 'a tool for organizing creative projects'",
        "importance": "critical",
    },
    "basic_description": {
        "rule": "Must describe Milanote as an online canvas for planning, brainstorming, and collaboration",
        "importance": "high",
    },
}

SCRIPT_FLOW = [
    {
        "step": "introduce_sponsorship",
        "requirements": ["Show Milanote Logo", "Sponsorship mention"],
    },
    {
        "step": "describe_milanote",
        "requirements": ["Tool description", "Canvas/workspace explanation"],
    },
    {
        "step": "personal_usage",
        "requirements": ["Show project board", "Demonstrate personal use case"],
    },
    {
        "step": "audience_usage",
        "requirements": ["Show templates", "Mention multiple use cases"],
    },
    {
        "step": "collaboration_features",
        "requirements": ["Show sharing/collaboration", "Real-time feedback features"],
    },
    {
        "step": "call_to_action",
        "requirements": ["Free with no time limit", "Link in description mention"],
    },
]

AVOID_ELEMENTS = [
    {
        "category": "youtube_planning",
        "description": "References to YouTube content planning, thumbnails, or scheduling",
        "severity": "high",
    },
    {
        "category": "missing_intro",
        "description": "Starting without proper Milanote introduction",
        "severity": "high",
    },
    {
        "category": "incorrect_signup",
        "description": "Mentioning 'download' instead of 'sign up'",
        "severity": "medium",
    },
    {
        "category": "missing_cta",
        "description": "No clear call-to-action at the end",
        "severity": "high",
    },
]
