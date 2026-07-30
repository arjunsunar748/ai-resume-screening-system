import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1/ats';

const api = axios.create({
  baseURL: API_BASE_URL,
});

/**
 * Uploads a PDF resume and job description to run hybrid ATS analysis.
 */
export const analyzePdfResume = async (file, jobDescription) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_description', jobDescription);

  const response = await api.post('/analyze-file', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

/**
 * Analyzes raw text for resume and job description.
 */
export const analyzeRawText = async (resumeText, jobDescription) => {
  const response = await api.post('/analyze', {
    resume_text: resumeText,
    job_description: jobDescription,
  });
  return response.data;
};