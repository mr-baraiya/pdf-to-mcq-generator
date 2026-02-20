import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import FileUpload from './components/FileUpload';
import LoadingAnimation from './components/LoadingAnimation';
import MCQResults from './components/MCQResults';
import MCQDisplay from './components/MCQDisplay';
import Features from './components/Features';
import AnimatedBackground from './components/AnimatedBackground';
import { AlertCircle } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [mcqs, setMcqs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('uploading');
  const [error, setError] = useState('');
  const [extractedText, setExtractedText] = useState('');
  const [showUpload, setShowUpload] = useState(false);
  const [viewMode, setViewMode] = useState('results'); // 'results' or 'attempt'
  const [selectedModel, setSelectedModel] = useState('auto'); // 'auto', 'ollama', 'groq', 'gemini'
  const [numQuestions, setNumQuestions] = useState(10); // Number of questions to generate

  const handleFileUpload = async (file) => {
    setLoading(true);
    setLoadingStage('uploading');
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      setLoadingStage('extracting');
      const response = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setExtractedText(response.data.text);
      
      // Auto-generate MCQs after upload using selected settings
      await handleGenerateMCQs(numQuestions, response.data.text, selectedModel);
    } catch (err) {
      let errorMessage = 'Error uploading file: ';
      
      if (err.response?.status === 413) {
        errorMessage = 'File too large! Maximum size is 5MB. Please upload a smaller PDF file.';
      } else {
        errorMessage += err.response?.data?.detail || err.message;
      }
      
      setError(errorMessage);
      setLoading(false);
    }
  };

  const handleGenerateMCQs = async (numQs = numQuestions, text = extractedText, model = selectedModel) => {
    if (!text) {
      setError('Please upload a PDF first');
      return;
    }
    
    setLoading(true);
    setLoadingStage('generating');
    setError('');
    
    try {
      // Select the appropriate endpoint based on model
      let endpoint = '/generate-mcqs'; // default auto fallback
      if (model === 'ollama') endpoint = '/generate-mcqs-ollama';
      else if (model === 'groq') endpoint = '/generate-mcqs-groq';
      else if (model === 'gemini') endpoint = '/generate-mcqs-gemini';
      
      const response = await axios.post(`${API_BASE_URL}${endpoint}`, {
        text: text,
        num_questions: numQs
      });
      
      // Normalize response - handle both 'answer' and 'correct_answer' fields
      const questions = response.data.questions.map(q => ({
        ...q,
        answer: q.answer || q.correct_answer // Support both field names
      }));
      
      // Append new questions to existing ones
      setMcqs(prev => [...prev, ...questions]);
      setViewMode('attempt'); // Start with quiz attempt
      setLoading(false);
    } catch (err) {
      setError('Error generating MCQs: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  const handleReset = () => {
    setMcqs([]);
    setExtractedText('');
    setError('');
    setShowUpload(false);
    setViewMode('results');
  };

  const handleGenerateMore = async () => {
    // Generate more MCQs using selected settings
    await handleGenerateMCQs(numQuestions, extractedText, selectedModel);
  };

  const handleGetStarted = () => {
    setShowUpload(true);
    setTimeout(() => {
      document.querySelector('section')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
  };

  const handleLogoClick = () => {
    // Reset to landing page
    handleReset();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white relative overflow-x-hidden">
      {/* Animated Background */}
      <AnimatedBackground />

      {/* Navbar */}
      <Navbar onLogoClick={handleLogoClick} />

      {/* Main Content */}
      <div className="relative z-10">
        {/* Error Banner */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              className="fixed top-20 left-1/2 -translate-x-1/2 z-50 max-w-md mx-4"
            >
              <div className="glass rounded-xl p-4 border border-red-500/50 bg-red-500/10 flex items-start space-x-3">
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-red-400">Error</p>
                  <p className="text-sm text-red-300">{error}</p>
                </div>
                <button
                  onClick={() => setError('')}
                  className="ml-auto text-red-400 hover:text-red-300"
                >
                  ×
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Hero Section - Show when no content */}
        {!showUpload && !loading && mcqs.length === 0 && (
          <Hero onGetStarted={handleGetStarted} />
        )}

        {/* File Upload Section */}
        {(showUpload || extractedText) && !loading && mcqs.length === 0 && (
          <FileUpload 
            onFileSelect={handleFileUpload} 
            loading={loading}
            selectedModel={selectedModel}
            onModelChange={setSelectedModel}
            numQuestions={numQuestions}
            onNumQuestionsChange={setNumQuestions}
          />
        )}

        {/* Loading State */}
        {loading && <LoadingAnimation stage={loadingStage} />}

        {/* MCQ Results or Quiz Attempt */}
        {!loading && mcqs.length > 0 && (
          <>
            {viewMode === 'attempt' ? (
              <MCQDisplay 
                mcqs={mcqs} 
                onReset={handleReset}
                onViewAnswers={() => setViewMode('results')}
              />
            ) : (
              <MCQResults 
                mcqs={mcqs} 
                onReset={handleReset}
                onGenerateMore={handleGenerateMore}
                onAttemptQuiz={() => setViewMode('attempt')}
              />
            )}
          </>
        )}

        {/* Features Section - Show on initial load */}
        {!showUpload && !loading && mcqs.length === 0 && (
          <Features />
        )}
      </div>

      {/* Footer */}
      <footer className="relative z-10 py-8 px-4 border-t border-white/10 mt-20">
        <div className="max-w-7xl mx-auto text-center text-gray-400 text-sm">
          <p>© 2026 PDF2MCQ. Built with ❤️ using React, Tailwind, and AI.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
