import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import FileUpload from './components/FileUpload';
import MCQDisplay from './components/MCQDisplay';
import Loading from './components/Loading';

function App() {
  const [mcqs, setMcqs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [extractedText, setExtractedText] = useState('');

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post('http://localhost:8000/upload-pdf', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setExtractedText(response.data.text);
      setError('');
    } catch (err) {
      setError('Error uploading file: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  const handleGenerateMCQs = async (numQuestions) => {
    if (!extractedText) {
      setError('Please upload a PDF first');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('http://localhost:8000/generate-mcqs', {
        text: extractedText,
        num_questions: numQuestions
      });
      
      setMcqs(response.data.questions);
      setLoading(false);
    } catch (err) {
      setError('Error generating MCQs: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>📄 PDF to MCQ Generator</h1>
        <p>Convert your PDF documents into multiple choice questions automatically</p>
      </header>

      <main className="app-container">
        {error && <div className="error-message">{error}</div>}
        
        {!extractedText ? (
          <FileUpload onFileSelect={handleFileUpload} loading={loading} />
        ) : (
          <>
            <div className="text-preview">
              <h3>Extracted Text Preview</h3>
              <p>{extractedText.substring(0, 300)}...</p>
              <button className="btn-secondary" onClick={() => setExtractedText('')}>
                Upload Another PDF
              </button>
            </div>
            
            {loading ? (
              <Loading />
            ) : mcqs.length === 0 ? (
              <div className="generate-section">
                <h2>Generate MCQs</h2>
                <div className="question-count-selector">
                  {[3, 5, 10].map(num => (
                    <button
                      key={num}
                      className="btn-primary"
                      onClick={() => handleGenerateMCQs(num)}
                    >
                      Generate {num} Questions
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <MCQDisplay mcqs={mcqs} onReset={() => setMcqs([])} />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
