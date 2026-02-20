import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, X, CheckCircle, Sparkles, Zap, Brain, ChevronDown } from 'lucide-react';

const FileUpload = ({ 
  onFileSelect, 
  loading,
  selectedModel,
  onModelChange,
  numQuestions,
  onNumQuestionsChange
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
        onFileSelect(file);
      }
    }
  }, [onFileSelect]);

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      onFileSelect(file);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
  };

  return (
    <section className="py-20 px-4">
      <div className="max-w-3xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gradient">
            Upload Your PDF
          </h2>
          <p className="text-gray-400">
            Drag and drop your PDF or click to browse
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`
            relative group
            ${dragActive || loading ? 'scale-[1.02]' : 'scale-100'}
            transition-transform duration-300
          `}
        >
          <div className={`
            relative glass rounded-2xl p-6 sm:p-12 border-2 border-dashed
            ${dragActive ? 'border-indigo-400 bg-indigo-500/10' : 'border-white/20'}
            ${loading ? 'opacity-50 pointer-events-none' : ''}
            transition-all duration-300
            hover:border-indigo-400/50 hover:bg-white/5
            cursor-pointer
          `}>
            {/* Glow Effect */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl opacity-0 group-hover:opacity-20 blur transition-opacity duration-500" />

            <input
              type="file"
              accept=".pdf"
              onChange={handleFileInput}
              disabled={loading}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            />

            <div className="relative z-0 flex flex-col items-center">
              <AnimatePresence mode="wait">
                {!selectedFile ? (
                  <motion.div
                    key="upload"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="flex flex-col items-center"
                  >
                    <motion.div
                      animate={{
                        y: [0, -10, 0],
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                      }}
                      className="mb-6"
                    >
                      <div className="relative">
                        <Upload className="w-16 h-16 text-indigo-400" />
                        <div className="absolute inset-0 blur-xl bg-indigo-500/50 animate-pulse-slow" />
                      </div>
                    </motion.div>
                    <h3 className="text-xl font-semibold mb-2 text-white">
                      Drop your PDF here
                    </h3>
                    <p className="text-gray-400 mb-4">or click to browse</p>
                    <div className="px-6 py-2 rounded-lg bg-indigo-500/20 border border-indigo-400/30 text-indigo-300 text-sm">
                      Supports PDF files up to 10MB
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    key="selected"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="w-full"
                  >
                    <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10">
                      <div className="flex items-center space-x-4">
                        <div className="p-3 rounded-lg bg-indigo-500/20">
                          <FileText className="w-6 h-6 text-indigo-400" />
                        </div>
                        <div>
                          <p className="font-semibold text-white">{selectedFile.name}</p>
                          <p className="text-sm text-gray-400">
                            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <CheckCircle className="w-6 h-6 text-green-400" />
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            clearFile();
                          }}
                          className="p-2 rounded-lg hover:bg-white/10 transition-colors"
                        >
                          <X className="w-5 h-5 text-gray-400" />
                        </button>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </motion.div>

        {/* AI Model Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-8 glass rounded-2xl p-6 border border-white/10"
        >
          <h3 className="text-lg font-semibold mb-4 text-white flex items-center">
            <Sparkles className="w-5 h-5 mr-2 text-indigo-400" />
            Generation Settings
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Model Selection Dropdown */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                AI Model
              </label>
              <div className="relative">
                <select
                  value={selectedModel}
                  onChange={(e) => onModelChange(e.target.value)}
                  disabled={loading}
                  className="w-full appearance-none glass rounded-xl px-4 py-3 pr-10 
                    border border-white/10 text-white bg-white/5
                    hover:border-indigo-400/50 hover:bg-white/10
                    focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                    disabled:opacity-50 disabled:cursor-not-allowed
                    transition-all duration-200 cursor-pointer"
                >
                  <option value="auto" className="bg-gray-900 text-white">
                    ✨ Auto (Recommended) - Smart Fallback
                  </option>
                  <option value="ollama" className="bg-gray-900 text-white">
                    🏠 Ollama - Local & Free
                  </option>
                  <option value="groq" className="bg-gray-900 text-white">
                    ⚡ Groq - Fast Cloud
                  </option>
                  <option value="gemini" className="bg-gray-900 text-white">
                    🧠 Gemini - Advanced AI
                  </option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>
              <p className="mt-2 text-xs text-gray-500">
                {selectedModel === 'auto' && '• Tries Ollama → Groq → Gemini'}
                {selectedModel === 'ollama' && '• Private, no API costs (requires Ollama running)'}
                {selectedModel === 'groq' && '• Very fast inference, cloud-based'}
                {selectedModel === 'gemini' && '• Best for complex documents'}
              </p>
            </div>

            {/* Number of Questions Dropdown */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Number of Questions
              </label>
              <div className="relative">
                <select
                  value={numQuestions}
                  onChange={(e) => onNumQuestionsChange(parseInt(e.target.value))}
                  disabled={loading}
                  className="w-full appearance-none glass rounded-xl px-4 py-3 pr-10 
                    border border-white/10 text-white bg-white/5
                    hover:border-indigo-400/50 hover:bg-white/10
                    focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                    disabled:opacity-50 disabled:cursor-not-allowed
                    transition-all duration-200 cursor-pointer"
                >
                  <option value="3" className="bg-gray-900 text-white">3 Questions</option>
                  <option value="5" className="bg-gray-900 text-white">5 Questions</option>
                  <option value="10" className="bg-gray-900 text-white">10 Questions</option>
                  <option value="15" className="bg-gray-900 text-white">15 Questions</option>
                  <option value="20" className="bg-gray-900 text-white">20 Questions</option>
                  <option value="25" className="bg-gray-900 text-white">25 Questions</option>
                  <option value="30" className="bg-gray-900 text-white">30 Questions</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>
              <p className="mt-2 text-xs text-gray-500">
                • More questions = longer generation time
              </p>
            </div>
          </div>
        </motion.div>

        {/* Info Text */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-6 text-center text-sm text-gray-500"
        >
          Your file is processed securely and deleted after generation
        </motion.div>
      </div>
    </section>
  );
};

export default FileUpload;
