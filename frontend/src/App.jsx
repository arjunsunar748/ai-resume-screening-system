import React, { useState } from 'react';
import { Upload, FileText, Sparkles, AlertCircle, RefreshCw } from 'lucide-react';
import { analyzePdfResume } from './api/ats';
import ScoreGauge from './components/ScoreGauge';
import SkillBadges from './components/SkillBadges';

export default function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid PDF document (.pdf).');
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please upload a resume PDF file.');
      return;
    }
    if (!jobDescription.trim()) {
      setError('Please paste the target job description.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await analyzePdfResume(file, jobDescription);
      setAnalysisResult(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to analyze resume. Ensure backend is running at http://127.0.0.1:8000');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 pb-16">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Sparkles className="w-7 h-7 text-sky-400" />
            <h1 className="text-xl font-bold bg-gradient-to-r from-sky-400 to-indigo-400 bg-clip-text text-transparent">
              AI Resume Screening & ATS System
            </h1>
          </div>
          <span className="text-xs bg-slate-800 text-slate-300 border border-slate-700 px-3 py-1 rounded-full font-mono">
            v1.0.0
          </span>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-6xl mx-auto px-6 mt-8">
        <form onSubmit={handleAnalyze} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* File Dropzone */}
          <div className="bg-slate-800/40 border border-slate-700/60 rounded-xl p-6 flex flex-col justify-between">
            <div>
              <label className="block text-sm font-semibold mb-2 text-slate-200">
                1. Upload PDF Resume
              </label>
              <div className="border-2 border-dashed border-slate-700 hover:border-sky-500/50 rounded-xl p-8 text-center transition-colors cursor-pointer relative bg-slate-900/30">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
                />
                <Upload className="w-10 h-10 mx-auto text-sky-400 mb-2" />
                <p className="text-sm font-medium text-slate-300">
                  {file ? file.name : 'Click or Drag & Drop PDF Resume'}
                </p>
                <p className="text-xs text-slate-500 mt-1">Supports PDF format up to 10MB</p>
              </div>
            </div>

            {file && (
              <div className="mt-4 flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-lg">
                <FileText className="w-4 h-4" /> Selected: {file.name}
              </div>
            )}
          </div>

          {/* Job Description Textarea */}
          <div className="bg-slate-800/40 border border-slate-700/60 rounded-xl p-6 flex flex-col justify-between">
            <div>
              <label className="block text-sm font-semibold mb-2 text-slate-200">
                2. Target Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the full job requirements, skills, and duties here..."
                rows={6}
                className="w-full bg-slate-900/60 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500 resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-4 w-full bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold py-3 px-6 rounded-xl flex items-center justify-center gap-2 transition-all disabled:opacity-50 shadow-lg shadow-sky-500/20 cursor-pointer"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" /> Evaluating Semantics & Skills...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" /> Analyze ATS Match Score
                </>
              )}
            </button>
          </div>
        </form>

        {/* Error Alert */}
        {error && (
          <div className="mt-6 bg-rose-500/10 border border-rose-500/30 text-rose-300 p-4 rounded-xl flex items-center gap-3 text-sm">
            <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
            {error}
          </div>
        )}

        {/* Results Section */}
        {analysisResult && (
          <section className="mt-10 bg-slate-800/30 border border-slate-800 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-6">ATS Evaluation Results</h2>

            {/* Score Gauges Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <ScoreGauge
                title="Overall Match Score"
                score={analysisResult.overall_score}
                weight="Combined Hybrid"
                color="indigo"
              />
              <ScoreGauge
                title="Semantic Similarity"
                score={analysisResult.semantic_score}
                weight="60%"
                color="sky"
              />
              <ScoreGauge
                title="Skill Keyword Fit"
                score={analysisResult.skill_score}
                weight="40%"
                color="emerald"
              />
            </div>

            {/* Skill Badges */}
            <SkillBadges
              matchedSkills={analysisResult.matched_skills}
              missingSkills={analysisResult.missing_skills}
            />

            {/* Actionable Suggestions */}
            {analysisResult.suggestions?.length > 0 && (
              <div className="mt-6 bg-slate-800/80 border border-slate-700/60 rounded-xl p-6">
                <h3 className="text-md font-semibold text-sky-400 mb-3 flex items-center gap-2">
                  <Sparkles className="w-4 h-4" /> Recommended Resume Enhancements
                </h3>
                <ul className="space-y-2">
                  {analysisResult.suggestions.map((suggestion, idx) => (
                    <li key={idx} className="text-sm text-slate-300 flex items-start gap-2">
                      <span className="text-sky-400 font-bold">•</span> {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}