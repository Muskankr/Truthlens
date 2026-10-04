"use client";

import { useEffect, useState } from "react";
import {
  AlertCircle,
  Clock3,
  FileSearch,
  Loader2,
  RefreshCw,
} from "lucide-react";

import {
  getInvestigations,
  InvestigationHistoryItem,
} from "@/lib/api";


export default function InvestigationHistory() {
  const [investigations, setInvestigations] =
    useState<InvestigationHistoryItem[]>([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  async function loadInvestigations() {
    try {
      setLoading(true);
      setError("");

      const result = await getInvestigations();

      setInvestigations(result.investigations);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not load investigation history.",
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadInvestigations();
  }, []);


  function formatDate(
    date: string | null,
  ) {
    if (!date) {
      return "Unknown date";
    }

    return new Date(date).toLocaleString();
  }


  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

      <div className="flex items-center justify-between">

        <div>

          <div className="flex items-center gap-2">

            <FileSearch size={19} />

            <h3 className="font-semibold">
              Investigation History
            </h3>

          </div>

          <p className="mt-1 text-xs text-slate-500">
            Previously analyzed questions
          </p>

        </div>


        <button
          type="button"
          onClick={loadInvestigations}
          disabled={loading}
          className="rounded-lg border border-white/10 p-2 text-slate-400 transition hover:bg-white/5 hover:text-white disabled:opacity-50"
          title="Refresh investigations"
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

          Loading investigation history...

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
        investigations.length === 0 && (
          <div className="py-10 text-center">

            <FileSearch
              size={30}
              className="mx-auto text-slate-600"
            />

            <p className="mt-3 text-sm text-slate-400">
              No investigations yet.
            </p>

            <p className="mt-1 text-xs text-slate-600">
              Ask a question to start your first investigation.
            </p>

          </div>
        )}


      {!loading &&
        !error &&
        investigations.length > 0 && (
          <div className="mt-5 space-y-3">

            {investigations.map(
              (investigation) => {

                const confidence =
                  investigation.confidence ?? 0;

                return (
                  <div
                    key={investigation.id}
                    className="rounded-xl border border-white/10 bg-black/20 p-4 transition hover:border-white/20"
                  >

                    <div className="flex items-start gap-3">

                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white/10">

                        <FileSearch
                          size={17}
                          className="text-slate-300"
                        />

                      </div>


                      <div className="min-w-0 flex-1">

                        <p className="text-sm font-medium leading-5 text-slate-200">
                          {investigation.question}
                        </p>


                        <div className="mt-2 flex flex-wrap items-center gap-2 text-[11px] text-slate-500">

                          <span>
                            Investigation #{investigation.id}
                          </span>

                          <span>•</span>

                          <span className="flex items-center gap-1">
                            <Clock3 size={11} />
                            {formatDate(
                              investigation.created_at,
                            )}
                          </span>

                        </div>

                      </div>


                      <div className="shrink-0 text-right">

                        <p className="text-sm font-semibold text-slate-200">
                          {Math.round(confidence)}
                        </p>

                        <p className="text-[10px] uppercase tracking-wide text-slate-500">
                          confidence
                        </p>

                      </div>

                    </div>


                    <div className="mt-3 border-t border-white/5 pt-3">

                      <p className="line-clamp-2 text-xs leading-5 text-slate-500">
                        {investigation.answer ||
                          "No answer generated."}
                      </p>

                    </div>

                  </div>
                );
              },
            )}

          </div>
        )}

    </div>
  );
}