from __future__ import annotations

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def clean_text(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


def split_terms(terms: str) -> list[str]:

    result = []

    for item in terms.replace(";", "\n").splitlines():

        item = item.strip()

        if item:
            item = item.lstrip("-• ").strip()
            result.append(item)

    return result


DEMO_TEMPLATE = """
{title}

EFFECTIVE DATE

{effective_date}

PARTIES

{parties}

PURPOSE

This document records the terms and conditions agreed by the parties.

KEY TERMS

{terms_block}

RESPONSIBILITIES

1. Each party will perform the responsibilities described in the agreed terms.

2. Each party will provide information reasonably necessary to carry out the agreement.

3. Any changes to this document should be made in writing and accepted by the parties.

CONFIDENTIALITY

The parties should keep confidential information received in connection with this agreement private, except where disclosure is required by law or agreed in writing.

TERM AND TERMINATION

This agreement begins on the effective date stated above. The parties may specify additional termination conditions in writing.

GENERAL PROVISIONS

This document is a draft for review. Any missing information should be completed before signing.

SIGNATURES

Party 1: ______________________________

Name: _________________________________

Date: __________________________________


Party 2: ______________________________

Name: _________________________________

Date: __________________________________
"""


class GeminiDocumentGenerator:

    def __init__(self, settings):

        self.settings = settings
        self.client = None

        if (
            settings.gemini_api_key
            and genai is not None
        ):

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ):

        document_type = clean_text(document_type)
        parties = clean_text(parties)
        terms = clean_text(terms)
        effective_date = clean_text(effective_date)

        terms_list = split_terms(terms)

        # DEMO MODE
        if self.settings.demo_mode:

            terms_block = "\n".join(
                f"- {term}"
                for term in terms_list
            )

            if not terms_block:
                terms_block = "- [NOT PROVIDED]"

            text = DEMO_TEMPLATE.format(
                title=document_type.upper(),
                effective_date=effective_date,
                parties=parties,
                terms_block=terms_block,
            )

            return {
                "text": clean_text(text),
                "terms": terms_list,
            }

        # REAL GEMINI MODE
        if self.client is None:

            raise RuntimeError(
                "Gemini is not configured. "
                "Add GEMINI_API_KEY to .env "
                "or set DEMO_MODE=true."
            )

        prompt = f"""
You are a careful legal-document drafting assistant.

Draft a structured document based ONLY on the information supplied below.

Document type:
{document_type}

Parties:
{parties}

Effective date:
{effective_date}

Terms and conditions:
{terms}

Rules:

- Do not invent names, dates, money amounts, addresses, laws, cases, or facts.
- If required information is missing, write [NOT PROVIDED].
- Do not fabricate legal citations.
- Use a clear title and useful headings.
- Include parties, effective date, key terms, responsibilities,
  confidentiality where relevant, term/termination where relevant,
  general provisions, and signatures.
- Treat the output as a draft for review, not legal advice.
- Return only the document text.
"""

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=8000,
            ),
        )

        generated = clean_text(
            getattr(response, "text", "") or ""
        )

        if not generated:

            raise RuntimeError(
                "Gemini returned an empty document."
            )

        return {
            "text": generated,
            "terms": terms_list,
        }