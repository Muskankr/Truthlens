"use client";

import { useEffect, useState } from "react";
import {
  CheckCircle2,
  FileText,
  Loader2,
  RefreshCw,
  AlertCircle,
} from "lucide-react";

import {
  getDocuments,
  DocumentItem,
} from "@/lib/api";


export default function DocumentLibrary() {
  const [documents, setDocuments] = useState<
    DocumentItem[]
  >([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  async function loadDocuments() {
    try {
      setLoading(true);
      setError("");

      const result = await getDocuments();

      setDocuments(result.documents);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load documents.",
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadDocuments();
  }, []);


  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

      <div className="flex items-center justify-between">

        <div>

          <div className="flex items-center gap-2">

            <FileText size={19} />

            <h3 className="font-semibold">
              Documents
            </h3>

          </div>

          <p className="mt-1 text-xs text-slate-500">
            Your evidence library
          </p>

        </div>


        <button
          type="button"
          onClick={loadDocuments}
          disabled={loading}
          className="rounded-lg border border-white/10 p-2 text-slate-400 transition hover:bg-white/5 hover:text-white disabled:opacity-50"
          title="Refresh documents"
        >
          <RefreshCw
            size={16}
            className={
              loading
                ? "animate-spin"
                : ""
            }
          />
        </button>

      </div>


      {loading && (
        <div className="flex items-center justify-center py-10 text-sm text-slate-500">
          <Loader2
            size={18}
            className="mr-2 animate-spin"
          />
          Loading documents...
        </div>
      )}


      {!loading && error && (
        <div className="mt-5 rounded-xl border border-red-500/20 bg-red-500/10 p-4">

          <div className="flex gap-2 text-sm text-red-300">

            <AlertCircle
              size={17}
              className="shrink-0"
            />

            <span>{error}</span>

          </div>

        </div>
      )}


      {!loading &&
        !error &&
        documents.length === 0 && (
          <div className="py-10 text-center">

            <FileText
              size={30}
              className="mx-auto text-slate-600"
            />

            <p className="mt-3 text-sm text-slate-400">
              No documents uploaded yet.
            </p>

            <p className="mt-1 text-xs text-slate-600">
              Upload a PDF to start an investigation.
            </p>

          </div>
        )}


      {!loading &&
        !error &&
        documents.length > 0 && (
          <div className="mt-5 space-y-3">

            {documents.map((document) => (

              <div
                key={document.id}
                className="rounded-xl border border-white/10 bg-black/20 p-4 transition hover:border-white/20"
              >

                <div className="flex items-start gap-3">

                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white/10">

                    <FileText
                      size={17}
                      className="text-slate-300"
                    />

                  </div>


                  <div className="min-w-0 flex-1">

                    <p
                      className="truncate text-sm font-medium text-slate-200"
                      title={document.filename}
                    >
                      {document.filename}
                    </p>


                    <div className="mt-2 flex flex-wrap gap-2 text-[11px] text-slate-500">

                      <span>
                        {document.page_count ?? 0} pages
                      </span>

                      <span>•</span>

                      <span>
                        {document.file_type.toUpperCase()}
                      </span>

                    </div>

                  </div>


                  <div className="shrink-0">

                    {document.status ===
                    "processed" ? (

                      <CheckCircle2
  size={17}
  className="text-emerald-400"
/>

                    ) : (

                      <span className="text-xs text-amber-400">
                        {document.status}
                      </span>

                    )}

                  </div>

                </div>

              </div>

            ))}

          </div>
        )}

    </div>
  );
}