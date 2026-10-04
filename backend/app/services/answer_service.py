import re


def split_sentences(text: str) -> list[str]:
    """
    Split evidence text into readable sentences.
    """
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
        if sentence.strip()
    ]


def generate_grounded_answer(
    question: str,
    evidence: list[dict],
) -> dict:
    """
    Generate an extractive answer using only retrieved evidence.

    V1 intentionally does not use an LLM.
    This prevents unsupported claims while the core
    TruthLens evidence pipeline is being built.
    """

    if not evidence:
        return {
            "answer": (
                "INSUFFICIENT EVIDENCE: "
                "No relevant evidence was found in the uploaded documents."
            ),
            "answer_type": "insufficient_evidence",
            "supporting_evidence_ids": [],
        }

    question_words = {
        word.lower()
        for word in re.findall(r"\b[a-zA-Z0-9]+\b", question)
        if len(word) >= 3
    }

    candidates = []

    for item in evidence:
        sentences = split_sentences(item["content"])

        for sentence in sentences:
            sentence_words = {
                word.lower()
                for word in re.findall(
                    r"\b[a-zA-Z0-9]+\b",
                    sentence,
                )
                if len(word) >= 3
            }

            overlap = len(question_words & sentence_words)

            if overlap > 0:
                candidates.append(
                    {
                        "sentence": sentence,
                        "chunk_id": item["chunk_id"],
                        "document_id": item["document_id"],
                        "page_number": item["page_number"],
                        "score": overlap
                        + item["relevance_score"],
                    }
                )

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    if not candidates:
        top = evidence[0]

        return {
            "answer": (
                "Relevant evidence was found, but TruthLens "
                "could not extract a direct answer from it."
            ),
            "answer_type": "evidence_found",
            "supporting_evidence_ids": [
                top["chunk_id"]
            ],
        }

    best = candidates[:2]

    answer = " ".join(
        item["sentence"]
        for item in best
    )

    return {
        "answer": answer,
        "answer_type": "grounded_extract",
        "supporting_evidence_ids": [
            item["chunk_id"]
            for item in best
        ],
    }