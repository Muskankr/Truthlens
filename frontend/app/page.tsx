"use client";

import { FormEvent, useState } from "react";
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  FileText,
  Lightbulb,
  Search,
  ShieldCheck,
} from "lucide-react";

import {
  investigate,
  Investigation,
} from "@/lib/api";

import DocumentUploader from "@/components/DocumentUploader";
import InvestigationGraph from "@/components/InvestigationGraph";
import DocumentLibrary from "@/components/DocumentLibrary";
import InvestigationHistory from "@/components/InvestigationHistory";


export default function Home() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<Investigation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleInvestigate(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const investigation = await investigate(
        question.trim(),
      );

      setResult(investigation);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <header className="border-b border-white/10">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-slate-950">
              <ShieldCheck size={23} />
            </div>

            <div>
              <h1 className="text-xl font-semibold">
                TruthLens
              </h1>

              <p className="text-xs text-slate-400">
                Evidence-aware AI investigation
              </p>
            </div>
          </div>

          <div className="hidden items-center gap-2 text-sm text-slate-400 sm:flex">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            Evidence engine online
          </div>
        </div>
      </header>

      {/* Main */}
      <section className="mx-auto max-w-7xl px-6 py-16">
        <div className="mx-auto max-w-4xl text-center">
          {/* Badge */}
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300">
            <Search size={15} />
            Ask questions. Trace evidence.
          </div>

          {/* Hero */}
          <h2 className="text-4xl font-bold tracking-tight sm:text-6xl">
            Don&apos;t just get an answer.
            <span className="block text-slate-400">
              Investigate the evidence.
            </span>
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-slate-400">
            TruthLens analyzes your documents, finds
            supporting evidence, detects conflicting
            claims, and explains how confident the system is.
          </p>

          {/* Question form */}
          <form
            onSubmit={handleInvestigate}
            className="mx-auto mt-10"
          >
            <div className="rounded-2xl border border-white/10 bg-white/5 p-2 shadow-2xl">
              <div className="flex flex-col gap-2 sm:flex-row">
                <input
                  value={question}
                  onChange={(event) =>
                    setQuestion(event.target.value)
                  }
                  placeholder="Ask something about your documents..."
                  className="min-h-14 flex-1 bg-transparent px-4 text-base outline-none placeholder:text-slate-500"
                />

                <button
                  type="submit"
                  disabled={
                    loading || !question.trim()
                  }
                  className="flex min-h-14 items-center justify-center gap-2 rounded-xl bg-white px-6 font-medium text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading
                    ? "Investigating..."
                    : "Investigate"}

                  {!loading && (
                    <ArrowRight size={18} />
                  )}
                </button>
              </div>
            </div>
          </form>

          <div className="mx-auto mt-6 max-w-4xl">
  <DocumentUploader />

  <div className="mt-6">
  <DocumentLibrary />
</div>

<div className="mt-6">
  <InvestigationHistory />
</div>

</div>

          {/* Error */}
          {error && (
            <div className="mt-5 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-left text-sm text-red-300">
              {error}
            </div>
          )}
        </div>

        {/* Investigation Results */}
        {result && (
          <div className="mt-16 space-y-6">
            {/* Answer + Confidence */}
            <div className="grid gap-6 lg:grid-cols-3">
              {/* Answer */}
              <div className="rounded-2xl border border-white/10 bg-white/5 p-6 lg:col-span-2">
                <div className="mb-4 flex items-center gap-2 text-sm text-slate-400">
                  <CheckCircle2 size={17} />
                  Investigation #{result.investigation_id}
                </div>

                <h3 className="text-lg font-medium text-slate-300">
                  {result.question}
                </h3>

                <div className="mt-5 text-xl leading-8">
                  {result.answer}
                </div>
              </div>

              {/* Confidence */}
              <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <p className="text-sm text-slate-400">
                  Confidence
                </p>

                <div className="mt-3 flex items-end gap-2">
                  <span className="text-5xl font-bold">
                    {Math.round(
                      result.confidence.score,
                    )}
                  </span>

                  <span className="mb-2 text-slate-400">
                    / 100
                  </span>
                </div>

                <div className="mt-3 text-sm uppercase tracking-wider text-slate-400">
                  {result.confidence.level}
                </div>

                {/* Confidence reasons */}
                {result.confidence.reasons?.length > 0 && (
                  <div className="mt-5 space-y-2">
                    {result.confidence.reasons.map(
                      (reason, index) => (
                        <p
                          key={index}
                          className="text-sm leading-5 text-slate-400"
                        >
                          • {reason}
                        </p>
                      ),
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Status */}
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <div className="flex flex-wrap items-center gap-3">
                <span className="text-sm text-slate-400">
                  Investigation status
                </span>

                <span className="rounded-full border border-white/10 bg-white/10 px-3 py-1 text-xs font-medium uppercase tracking-wide">
                  {result.status.replace(
                    /_/g,
                    " ",
                  )}
                </span>

                <span className="text-sm text-slate-500">
                  Answer type:{" "}
                  {result.answer_type.replace(
                    /_/g,
                    " ",
                  )}
                </span>
              </div>
            </div>

            {/* Conflicts */}
            {result.conflicts.length > 0 && (
              <div className="rounded-2xl border border-amber-400/20 bg-amber-400/5 p-6">
                <div className="flex items-center gap-3">
                  <AlertTriangle className="text-amber-400" />

                  <div>
                    <h3 className="font-semibold">
                      Potential conflicts detected
                    </h3>

                    <p className="text-sm text-slate-400">
                      {result.conflicts.length} conflicting
                      claim(s) require review.
                    </p>
                  </div>
                </div>

                <div className="mt-6 space-y-4">
                  {result.conflicts.map(
                    (conflict, index) => (
                      <div
                        key={index}
                        className="grid gap-4 rounded-xl border border-white/10 bg-black/20 p-4 md:grid-cols-2"
                      >
                        <div>
                          <p className="mb-2 text-xs uppercase text-slate-500">
                            Claim A
                          </p>

                          <p className="text-sm leading-6">
                            {conflict.claim_a.text}
                          </p>

                          <p className="mt-2 text-xs text-slate-500">
                            Value:{" "}
                            {conflict.claim_a.value}
                          </p>
                        </div>

                        <div>
                          <p className="mb-2 text-xs uppercase text-slate-500">
                            Claim B
                          </p>

                          <p className="text-sm leading-6">
                            {conflict.claim_b.text}
                          </p>

                          <p className="mt-2 text-xs text-slate-500">
                            Value:{" "}
                            {conflict.claim_b.value}
                          </p>
                        </div>
                      </div>
                    ),
                  )}
                </div>
              </div>
            )}

            {/* Investigation Graph */}
<div>
  <InvestigationGraph
    investigation={result}
  />
</div>

{/* Why This Answer */}
<div className="rounded-2xl border border-white/10 bg-white/5 p-6">

  <div className="flex items-start gap-3">

    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-slate-950">
      <Lightbulb size={19} />
    </div>

    <div>
      <h3 className="text-lg font-semibold">
        Why this answer?
      </h3>

      <p className="mt-1 text-sm text-slate-500">
        How TruthLens reached this conclusion.
      </p>
    </div>

  </div>


  <div className="mt-6 space-y-3">

    {result.why_this_answer.map(
      (reason, index) => (

        <div
          key={index}
          className="flex items-start gap-3 rounded-xl border border-white/5 bg-black/20 p-4"
        >

          <CheckCircle2
            size={17}
            className="mt-0.5 shrink-0 text-emerald-400"
          />

          <p className="text-sm leading-6 text-slate-300">
            {reason}
          </p>

        </div>

      ),
    )}

  </div>

</div>

{/* Evidence Matrix */}
<div className="rounded-2xl border border-white/10 bg-white/5 p-6">

  <div className="mb-5">

    <h3 className="text-xl font-semibold">
      Evidence Matrix
    </h3>

    <p className="mt-1 text-sm text-slate-500">
      Every retrieved source contributing to this investigation.
    </p>

  </div>


  <div className="overflow-x-auto">

    <table className="w-full text-left text-sm">

      <thead className="border-b border-white/10 text-xs uppercase tracking-wide text-slate-500">

        <tr>

          <th className="px-4 py-3">
            Evidence
          </th>

          <th className="px-4 py-3">
            Document
          </th>

          <th className="px-4 py-3">
            Page
          </th>

          <th className="px-4 py-3">
            Relevance
          </th>

          <th className="px-4 py-3">
            Role
          </th>

        </tr>

      </thead>


      <tbody>

        {result.evidence.map(
          (item) => (

            <tr
              key={item.chunk_id}
              className="border-b border-white/5 last:border-0"
            >

              <td className="px-4 py-4 font-medium text-slate-200">
                #{item.chunk_id}
              </td>

              <td className="px-4 py-4 text-slate-400">
                Document #{item.document_id}
              </td>

              <td className="px-4 py-4 text-slate-400">
                {item.page_number ?? "N/A"}
              </td>

              <td className="px-4 py-4">

                <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-300">

                  {Math.round(
                    item.relevance_score * 100,
                  )}
                  %

                </span>

              </td>

              <td className="px-4 py-4 text-emerald-300">
                Supporting evidence
              </td>

            </tr>

          ),
        )}

      </tbody>

    </table>

  </div>

</div>

            {/* Evidence */}
            <div>
              <div className="mb-4 flex items-center gap-2">
                <FileText size={19} />

                <h3 className="text-xl font-semibold">
                  Evidence
                </h3>

                <span className="text-sm text-slate-500">
                  {result.evidence.length} source(s)
                </span>
              </div>

              <div className="grid gap-4">
                {result.evidence.map((item) => (
                  <div
                    key={item.chunk_id}
                    className="rounded-2xl border border-white/10 bg-white/5 p-6"
                  >
                    <div className="mb-4 flex flex-wrap items-center gap-3 text-xs text-slate-400">
                      <span>
                        Document #{item.document_id}
                      </span>

                      <span>•</span>

                      <span>
                        Page{" "}
                        {item.page_number ?? "N/A"}
                      </span>

                      <span>•</span>

                      <span>
                        Evidence #{item.chunk_id}
                      </span>

                      <span>•</span>

                      <span>
                        Relevance{" "}
                        {Math.round(
                          item.relevance_score * 100,
                        )}
                        %
                      </span>
                    </div>

                    <p className="text-sm leading-7 text-slate-300">
                      {item.content}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Supporting evidence IDs */}
            {result.supporting_evidence_ids.length > 0 && (
              <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <h3 className="font-semibold">
                  Supporting evidence
                </h3>

                <div className="mt-4 flex flex-wrap gap-2">
                  {result.supporting_evidence_ids.map(
                    (id) => (
                      <span
                        key={id}
                        className="rounded-lg border border-emerald-400/20 bg-emerald-400/10 px-3 py-2 text-sm text-emerald-300"
                      >
                        Evidence #{id}
                      </span>
                    ),
                  )}
                </div>
              </div>
            )}

            {/* Missing Evidence */}
            {result.missing_evidence.length > 0 && (
              <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <h3 className="font-semibold">
                  Investigation notes
                </h3>

                <ul className="mt-3 space-y-2 text-sm text-slate-400">
                  {result.missing_evidence.map(
                    (item, index) => (
                      <li key={index}>
                        • {item}
                      </li>
                    ),
                  )}
                </ul>
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}