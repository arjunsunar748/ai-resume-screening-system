import React from 'react';
import { CheckCircle2, XCircle } from 'lucide-react';

export default function SkillBadges({ matchedSkills = [], missingSkills = [] }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
      {/* Matched Skills */}
      <div className="bg-slate-800/60 border border-emerald-500/30 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-3 text-emerald-400 font-semibold">
          <CheckCircle2 className="w-5 h-5" />
          <h3>Matched Skills ({matchedSkills.length})</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {matchedSkills.length > 0 ? (
            matchedSkills.map((skill) => (
              <span
                key={skill}
                className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-medium rounded-full capitalize"
              >
                {skill}
              </span>
            ))
          ) : (
            <p className="text-xs text-slate-400">No overlapping skills detected.</p>
          )}
        </div>
      </div>

      {/* Missing Skills */}
      <div className="bg-slate-800/60 border border-rose-500/30 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-3 text-rose-400 font-semibold">
          <XCircle className="w-5 h-5" />
          <h3>Missing Target Skills ({missingSkills.length})</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {missingSkills.length > 0 ? (
            missingSkills.map((skill) => (
              <span
                key={skill}
                className="px-3 py-1 bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-medium rounded-full capitalize"
              >
                {skill}
              </span>
            ))
          ) : (
            <p className="text-xs text-slate-400">Great job! No key technical skills missing.</p>
          )}
        </div>
      </div>
    </div>
  );
}