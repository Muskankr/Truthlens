const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000/api";


export interface Evidence {
  chunk_id: number;
  document_id: number;
  page_number: number | null;
  content: string;
  relevance_score: number;
  support_type: string;
}


export interface ConflictClaim {
  id: number;
  document_id: number;
  chunk_id: number;
  text: string;
  value: number;
}


export interface Conflict {
  claim_a: ConflictClaim;
  claim_b: ConflictClaim;
  conflict_type: string;
  status: string;
}


export interface Confidence {
  score: number;
  level: string;
  reasons: string[];
}


export interface Investigation {
  investigation_id: number;
  question: string;
  status: string;
  answer: string;
  answer_type: string;
  supporting_evidence_ids: number[];
  confidence: Confidence;
  evidence: Evidence[];
  conflicts: Conflict[];
  missing_evidence: string[];
  why_this_answer: string[];
}


export async function investigate(
  question: string,
): Promise<Investigation> {

  const response = await fetch(
    `${API_BASE_URL}/investigations`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question,
        limit: 5,
      }),
    },
  );


  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      errorText || "Investigation failed.",
    );
  }


  return response.json();
}

export interface UploadedDocument {
  id: number;
  filename: string;
  file_type: string;
  status: string;
  page_count: number | null;
}


export async function uploadDocument(
  file: File,
): Promise<UploadedDocument> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/documents/upload`,
    {
      method: "POST",
      body: formData,
    },
  );

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      errorText || "Document upload failed.",
    );
  }

  return response.json();
}

export interface DocumentItem {
  id: number;
  filename: string;
  file_type: string;
  status: string;
  page_count: number | null;
  created_at: string | null;
}


export async function getDocuments(): Promise<{
  count: number;
  documents: DocumentItem[];
}> {
  const response = await fetch(
    `${API_BASE_URL}/documents`,
    {
      method: "GET",
      cache: "no-store",
    },
  );

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      errorText || "Failed to load documents.",
    );
  }

  return response.json();
}

export interface InvestigationHistoryItem {
  id: number;
  question: string;
  answer: string | null;
  confidence: number | null;
  status: string;
  created_at: string | null;
}


export async function getInvestigations(): Promise<{
  count: number;
  investigations: InvestigationHistoryItem[];
}> {
  const response = await fetch(
    `${API_BASE_URL}/investigations`,
    {
      method: "GET",
      cache: "no-store",
    },
  );

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      errorText || "Failed to load investigations.",
    );
  }

  return response.json();
}