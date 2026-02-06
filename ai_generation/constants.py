"""
Single source of truth for generation commands and document types.
Used by views (duplicate check), services (API prompts), and serializers (choices).
"""

# Commands accepted by the generate endpoint and serializer
COMMAND_CHOICES = ("generate_resume", "generate_cover_letter", "generate_both")

# Map each command to the document_type(s) it creates (for DB and duplicate check)
COMMAND_TO_DOCUMENT_TYPES = {
    "generate_resume": ["resume"],
    "generate_cover_letter": ["cover_letter"],
    "generate_both": ["resume", "cover_letter"],
}

# Map document_type (DB value) to label used in prompts (e.g. "cover letter" with space)
COMMAND_TO_READABLE_COMMAND = {
    "resume": "resume",
    "cover_letter": "cover letter",
}
