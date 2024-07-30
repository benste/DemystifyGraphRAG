from default_prompts import graph_extraction as entity_default_prompt
from default_prompts import claims_extraction as claim_default_prompt


def extract(documents: dict[int: str], configured_llm: dict):
    formatting = claim_default_prompt.DEFAULT_FORMATTING
    formatting['default_prompt'] = claim_default_prompt.CLAIM_EXTRACTION_PROMPT
    formatting['continue_prompt'] = entity_default_prompt.CONTINUE_PROMPT
    formatting['loop_prompt'] = entity_default_prompt.LOOP_PROMPT
    
    llm_raw_output = loop_extraction(documents, formatting, configured_llm)
    
    all_claims = []
    for source_doc_id, extracted_data in llm_raw_output.items():
        claims = parse_claim_tuples(extracted_data, formatting)
        for c in claims:
            c["doc_id"] = f"{source_doc_id}"
            all_claims.append(_clean_claim(c, source_doc_id, {}))
        
   
def parse_claim_tuples(claims: str, formatting: dict) -> list:
    """Parse claim tuples."""
    record_delimiter = formatting['record_delimiter']
    completion_delimiter = formatting['completion_delimiter']
    tuple_delimiter = formatting['tuple_delimiter']

    def pull_field(index: int, fields: list[str]) -> str | None:
        return fields[index].strip() if len(fields) > index else None

    result = []
    claims_values = (
        claims.strip().removesuffix(completion_delimiter).split(record_delimiter)
    )
    for claim in claims_values:
        claim = claim.strip().removeprefix("(").removesuffix(")")

        # Ignore the completion delimiter
        if claim == completion_delimiter:
            continue

        claim_fields = claim.split(tuple_delimiter)
        result.append({
            "subject_id": pull_field(0, claim_fields),
            "object_id": pull_field(1, claim_fields),
            "type": pull_field(2, claim_fields),
            "status": pull_field(3, claim_fields),
            "start_date": pull_field(4, claim_fields),
            "end_date": pull_field(5, claim_fields),
            "description": pull_field(6, claim_fields),
            "source_text": pull_field(7, claim_fields),
            "doc_id": pull_field(8, claim_fields),
        })
    return result

def _clean_claim(claim: dict, document_id: str, resolved_entities: dict) -> dict:
        # clean the parsed claims to remove any claims with status = False
        obj = claim.get("object_id", claim.get("object"))
        subject = claim.get("subject_id", claim.get("subject"))

        # If subject or object in resolved entities, then replace with resolved entity
        obj = resolved_entities.get(obj, obj)
        subject = resolved_entities.get(subject, subject)
        claim["object_id"] = obj
        claim["subject_id"] = subject
        claim["doc_id"] = document_id
        return claim