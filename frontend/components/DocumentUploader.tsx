"use client";

import { ChangeEvent, useState } from "react";
import {
  CheckCircle2,
  FileUp,
  Loader2,
  Upload,
} from "lucide-react";

import {
  uploadDocument,
  UploadedDocument,
} from "@/lib/api";


interface DocumentUploaderProps {
  onUploaded?: (
    document: UploadedDocument,
  ) => void;
}


export default function DocumentUploader({
  onUploaded,
}: DocumentUploaderProps) {

  const [uploading, setUploading] =
    useState(false);

  const [uploaded, setUploaded] =
    useState<UploadedDocument | null>(null);

  const [error, setError] =
    useState("");


  async function handleFileChange(
    event: ChangeEvent<HTMLInputElement>,
  ) {

    const file = event.target.files?.[0];

    if (!file) {
      return;
    }


    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are supported.");
      return;
    }


    setUploading(true);
    setError("");
    setUploaded(null);


    try {

      const document =
        await uploadDocument(file);

      setUploaded(document);

      onUploaded?.(document);

    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Document upload failed.",
      );

    } finally {

      setUploading(false);

    }
  }


  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

      <div className="flex items-start gap-4">

        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-white text-slate-950">
          <FileUp size={21} />
        </div>


        <div>

          <h3 className="font-semibold">
            Add evidence
          </h3>

          <p className="mt-1 text-sm text-slate-400">
            Upload a PDF to make it searchable by TruthLens.
          </p>

        </div>

      </div>


      <label
        className={`mt-6 flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-white/15 bg-black/20 px-6 py-8 text-center transition hover:border-white/30 hover:bg-white/5 ${
          uploading
            ? "pointer-events-none opacity-60"
            : ""
        }`}
      >

        {uploading ? (

          <>
            <Loader2
              size={28}
              className="animate-spin text-slate-300"
            />

            <p className="mt-3 text-sm font-medium">
              Processing document...
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Extracting pages and creating evidence chunks
            </p>
          </>

        ) : (

          <>
            <Upload
              size={28}
              className="text-slate-400"
            />

            <p className="mt-3 text-sm font-medium">
              Click to upload a PDF
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Text-based PDF files are currently supported
            </p>
          </>

        )}


        <input
          type="file"
          accept=".pdf,application/pdf"
          className="hidden"
          onChange={handleFileChange}
        />

      </label>


      {error && (

        <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-300">
          {error}
        </div>

      )}


      {uploaded && (

        <div className="mt-4 flex items-start gap-3 rounded-xl border border-emerald-400/20 bg-emerald-400/5 p-4">

          <CheckCircle2
            size={19}
            className="mt-0.5 shrink-0 text-emerald-400"
          />

          <div className="min-w-0">

            <p className="text-sm font-medium text-emerald-300">
              Document processed successfully
            </p>

            <p className="mt-1 truncate text-sm text-slate-300">
              {uploaded.filename}
            </p>

            <p className="mt-1 text-xs text-slate-500">
              {uploaded.page_count ?? 0} page(s)
              {" • "}
              {uploaded.status}
            </p>

          </div>

        </div>

      )}

    </div>
  );
}