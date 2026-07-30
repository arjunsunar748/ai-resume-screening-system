import React from 'react';

export default function ScoreGauge({ title, score, weight, color = 'emerald' }) {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const colorMap = {
    emerald: 'text-emerald-500 stroke-emerald-500',
    sky: 'text-sky-500 stroke-sky-500',
    amber: 'text-amber-500 stroke-amber-500',
    indigo: 'text-indigo-500 stroke-indigo-500',
  };

  return (
    <div className="flex flex-col items-center bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 shadow-lg">
      <div className="relative w-28 h-28 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90">
          <circle
            cx="56"
            cy="56"
            r={radius}
            className="stroke-slate-700"
            strokeWidth="8"
            fill="transparent"
          />
          <circle
            cx="56"
            cy="56"
            r={radius}
            className={`transition-all duration-1000 ease-out ${colorMap[color] || colorMap.sky}`}
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>
        <span className="absolute text-2xl font-bold text-white">
          {Math.round(score)}%
        </span>
      </div>
      <h4 className="mt-3 text-sm font-semibold text-slate-200">{title}</h4>
      {weight && <p className="text-xs text-slate-400 mt-0.5">Weight: {weight}</p>}
    </div>
  );
}