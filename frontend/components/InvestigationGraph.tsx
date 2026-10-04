"use client";

import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

import {
  AlertTriangle,
  FileText,
  HelpCircle,
  ShieldCheck,
} from "lucide-react";

import { Investigation } from "@/lib/api";


interface InvestigationGraphProps {
  investigation: Investigation;
}


export default function InvestigationGraph({
  investigation,
}: InvestigationGraphProps) {

  const nodes: Node[] = [];

  const edges: Edge[] = [];


  // ---------------------------------------------------------
  // Question node
  // ---------------------------------------------------------

  nodes.push({
    id: "question",
    position: {
      x: 350,
      y: 40,
    },
    data: {
      label: (
        <div className="w-64 rounded-xl border border-white/20 bg-slate-900 p-4 text-white">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-slate-400">
            <HelpCircle size={14} />
            Investigation
          </div>

          <p className="mt-2 text-sm leading-5">
            {investigation.question}
          </p>
        </div>
      ),
    },
  });


  // ---------------------------------------------------------
  // Evidence nodes
  // ---------------------------------------------------------

  investigation.evidence.forEach(
    (evidence, index) => {

      const nodeId = `evidence-${evidence.chunk_id}`;

      nodes.push({
        id: nodeId,

        position: {
          x: index % 2 === 0 ? 80 : 620,
          y: 220 + Math.floor(index / 2) * 190,
        },

        data: {
          label: (
            <div className="w-64 rounded-xl border border-blue-400/20 bg-slate-900 p-4 text-white">

              <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-blue-300">
                <FileText size={14} />
                Evidence #{evidence.chunk_id}
              </div>

              <p className="mt-2 line-clamp-4 text-xs leading-5 text-slate-300">
                {evidence.content}
              </p>

              <div className="mt-3 flex justify-between text-[10px] text-slate-500">
                <span>
                  Page {evidence.page_number ?? "N/A"}
                </span>

                <span>
                  {Math.round(
                    evidence.relevance_score * 100,
                  )}
                  %
                </span>
              </div>

            </div>
          ),
        },
      });


      edges.push({
        id: `question-${nodeId}`,
        source: "question",
        target: nodeId,
        animated: true,
      });
    },
  );


  // ---------------------------------------------------------
  // Conflict nodes
  // ---------------------------------------------------------

  investigation.conflicts.forEach(
    (conflict, index) => {

      const conflictId = `conflict-${index}`;

      nodes.push({
        id: conflictId,

        position: {
          x: 350,
          y: 280 + index * 220,
        },

        data: {
          label: (
            <div className="w-60 rounded-xl border border-amber-400/30 bg-amber-400/10 p-4 text-white">

              <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-amber-300">
                <AlertTriangle size={14} />
                Potential Conflict
              </div>

              <p className="mt-2 text-xs leading-5 text-slate-300">
                {conflict.claim_a.value}
                {" vs "}
                {conflict.claim_b.value}
              </p>

              <p className="mt-2 text-[10px] text-slate-500">
                {conflict.conflict_type}
              </p>

            </div>
          ),
        },
      });


      const claimAEdge = `conflict-${index}-a`;

      const claimBEdge = `conflict-${index}-b`;


      edges.push({
        id: claimAEdge,
        source: `evidence-${conflict.claim_a.chunk_id}`,
        target: conflictId,
        animated: true,
        label: "Claim A",
      });


      edges.push({
        id: claimBEdge,
        source: `evidence-${conflict.claim_b.chunk_id}`,
        target: conflictId,
        animated: true,
        label: "Claim B",
      });

    },
  );


  return (
    <div className="overflow-hidden rounded-2xl border border-white/10 bg-slate-950">

      <div className="border-b border-white/10 px-6 py-4">

        <div className="flex items-center gap-3">

          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white text-slate-950">
            <ShieldCheck size={18} />
          </div>

          <div>

            <h3 className="font-semibold">
              Investigation Graph
            </h3>

            <p className="text-xs text-slate-500">
              Trace the relationship between your question,
              evidence, and conflicts.
            </p>

          </div>

        </div>

      </div>


      <div className="h-[600px]">

        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
          attributionPosition="bottom-left"
        >

          <Background />

          <Controls />

          <MiniMap />

        </ReactFlow>

      </div>

    </div>
  );
}