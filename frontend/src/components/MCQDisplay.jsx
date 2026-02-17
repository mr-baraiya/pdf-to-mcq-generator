import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, RotateCcw, Download, Eye } from 'lucide-react';
import { jsPDF } from 'jspdf';

const MCQCard = ({ mcq, index, userAnswer, onAnswerSelect, showResults }) => {
  const isCorrect = userAnswer === mcq.answer;

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className="glass rounded-xl sm:rounded-2xl p-4 sm:p-6 border border-white/10 hover:border-white/20 transition-all group"
    >
      <div className="flex items-start justify-between mb-3 sm:mb-4">
        <span className="text-xs sm:text-sm font-semibold text-indigo-400">
          Question {index + 1}
        </span>
        {showResults && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            {isCorrect ? (
              <CheckCircle2 className="w-5 h-5 sm:w-6 sm:h-6 text-green-400" />
            ) : (
              <XCircle className="w-5 h-5 sm:w-6 sm:h-6 text-red-400" />
            )}
          </motion.div>
        )}
      </div>

      <h3 className="text-base sm:text-lg font-semibold text-white mb-4 sm:mb-6">
        {mcq.question}
      </h3>

      <div className="space-y-2 sm:space-y-3">
        {Array.isArray(mcq.options) ? (
          // Handle array format (e.g., ["Option 1", "Option 2", "Option 3", "Option 4"])
          mcq.options.map((value, optIndex) => {
            const key = String.fromCharCode(65 + optIndex); // A, B, C, D
            const isSelected = userAnswer === key;
            const isCorrectOption = key === mcq.answer;
            const showCorrect = showResults && isCorrectOption;
            const showIncorrect = showResults && isSelected && !isCorrectOption;

            return (
              <motion.button
                key={key}
                onClick={() => !showResults && onAnswerSelect(key)}
                disabled={showResults}
                className={`
                  w-full text-left p-3 sm:p-4 rounded-lg sm:rounded-xl border transition-all
                  ${isSelected && !showResults ? 'border-indigo-400 bg-indigo-500/10' : 'border-white/10'}
                  ${showCorrect ? 'border-green-400 bg-green-500/10' : ''}
                  ${showIncorrect ? 'border-red-400 bg-red-500/10' : ''}
                  ${!showResults && !isSelected ? 'hover:border-white/30 hover:bg-white/5' : ''}
                  ${showResults ? 'cursor-default' : 'cursor-pointer'}
                `}
                whileHover={!showResults ? { scale: 1.02, x: 4 } : {}}
                whileTap={!showResults ? { scale: 0.98 } : {}}
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center space-x-2 sm:space-x-3 flex-1 min-w-0">
                    <span className={`
                      flex items-center justify-center w-7 h-7 sm:w-8 sm:h-8 rounded-lg font-semibold text-sm flex-shrink-0
                      ${showCorrect ? 'bg-green-500/20 text-green-400' : ''}
                      ${showIncorrect ? 'bg-red-500/20 text-red-400' : ''}
                      ${!showResults && isSelected ? 'bg-indigo-500/20 text-indigo-400' : ''}
                      ${!showResults && !isSelected ? 'bg-white/5 text-gray-400' : ''}
                    `}>
                      {key}
                    </span>
                    <span className={`
                      text-sm sm:text-base break-words
                      ${showCorrect || showIncorrect || isSelected ? 'text-white' : 'text-gray-300'}
                    `}>
                      {value}
                    </span>
                  </div>
                  {showCorrect && (
                    <CheckCircle2 className="w-4 h-4 sm:w-5 sm:h-5 text-green-400 flex-shrink-0" />
                  )}
                  {showIncorrect && (
                    <XCircle className="w-4 h-4 sm:w-5 sm:h-5 text-red-400 flex-shrink-0" />
                  )}
                </div>
              </motion.button>
            );
          })
        ) : (
          // Handle object format (e.g., { "A": "Option 1", "B": "Option 2" })
          Object.entries(mcq.options).map(([key, value]) => {
            const isSelected = userAnswer === key;
            const isCorrectOption = key === mcq.answer;
            const showCorrect = showResults && isCorrectOption;
            const showIncorrect = showResults && isSelected && !isCorrectOption;

            return (
              <motion.button
                key={key}
                onClick={() => !showResults && onAnswerSelect(key)}
                disabled={showResults}
                className={`
                  w-full text-left p-3 sm:p-4 rounded-lg sm:rounded-xl border transition-all
                  ${isSelected && !showResults ? 'border-indigo-400 bg-indigo-500/10' : 'border-white/10'}
                  ${showCorrect ? 'border-green-400 bg-green-500/10' : ''}
                  ${showIncorrect ? 'border-red-400 bg-red-500/10' : ''}
                  ${!showResults && !isSelected ? 'hover:border-white/30 hover:bg-white/5' : ''}
                  ${showResults ? 'cursor-default' : 'cursor-pointer'}
                `}
                whileHover={!showResults ? { scale: 1.02, x: 4 } : {}}
                whileTap={!showResults ? { scale: 0.98 } : {}}
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center space-x-2 sm:space-x-3 flex-1 min-w-0">
                    <span className={`
                      flex items-center justify-center w-7 h-7 sm:w-8 sm:h-8 rounded-lg font-semibold text-sm flex-shrink-0
                      ${showCorrect ? 'bg-green-500/20 text-green-400' : ''}
                      ${showIncorrect ? 'bg-red-500/20 text-red-400' : ''}
                      ${!showResults && isSelected ? 'bg-indigo-500/20 text-indigo-400' : ''}
                      ${!showResults && !isSelected ? 'bg-white/5 text-gray-400' : ''}
                    `}>
                      {key}
                    </span>
                    <span className={`
                      text-sm sm:text-base break-words
                      ${showCorrect || showIncorrect || isSelected ? 'text-white' : 'text-gray-300'}
                    `}>
                      {value}
                    </span>
                  </div>
                  {showCorrect && (
                    <CheckCircle2 className="w-4 h-4 sm:w-5 sm:h-5 text-green-400 flex-shrink-0" />
                  )}
                  {showIncorrect && (
                    <XCircle className="w-4 h-4 sm:w-5 sm:h-5 text-red-400 flex-shrink-0" />
                  )}
                </div>
              </motion.button>
            );
          })
        )}
      </div>

      {showResults && mcq.answer && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mt-3 sm:mt-4 p-3 sm:p-4 rounded-lg sm:rounded-xl bg-white/5 border border-white/10"
        >
          <p className="text-xs sm:text-sm text-gray-400">
            <span className="font-semibold text-white">Correct Answer:</span>{' '}
            {mcq.answer}. {Array.isArray(mcq.options) 
              ? mcq.options[mcq.answer.charCodeAt(0) - 65] 
              : mcq.options[mcq.answer]}
          </p>
        </motion.div>
      )}
    </motion.div>
  );
};

const MCQDisplay = ({ mcqs, onReset, onViewAnswers }) => {
  const [userAnswers, setUserAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  const handleAnswerSelect = (questionIndex, option) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionIndex]: option
    }));
  };

  const handleCheckAnswers = () => {
    setShowResults(true);
    // Scroll to top to show results
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 100);
  };

  const calculateScore = () => {
    let correct = 0;
    mcqs.forEach((mcq, index) => {
      if (userAnswers[index] === mcq.answer) {
        correct++;
      }
    });
    return { correct, total: mcqs.length };
  };

  const handleDownload = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 20;
    let yPosition = margin;

    // Title
    doc.setFontSize(20);
    doc.setFont('helvetica', 'bold');
    doc.text(showResults ? 'Quiz Results' : 'MCQ Questions', pageWidth / 2, yPosition, { align: 'center' });
    yPosition += 15;

    // Add score if results are shown
    if (showResults) {
      const { correct, total } = calculateScore();
      const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;
      doc.setFontSize(14);
      doc.setFont('helvetica', 'normal');
      doc.text(`Score: ${correct}/${total} (${percentage}%)`, pageWidth / 2, yPosition, { align: 'center' });
      yPosition += 15;
    }

    // Questions
    doc.setFontSize(12);
    mcqs.forEach((mcq, index) => {
      // Check if we need a new page
      if (yPosition > pageHeight - 60) {
        doc.addPage();
        yPosition = margin;
      }

      // Question number and text
      doc.setFont('helvetica', 'bold');
      const questionText = `Q${index + 1}. ${mcq.question}`;
      const splitQuestion = doc.splitTextToSize(questionText, pageWidth - 2 * margin);
      doc.text(splitQuestion, margin, yPosition);
      yPosition += 7 * splitQuestion.length;

      // Options
      doc.setFont('helvetica', 'normal');
      const optionsList = Array.isArray(mcq.options)
        ? mcq.options.map((opt, i) => ({ key: String.fromCharCode(65 + i), value: opt }))
        : Object.entries(mcq.options).map(([k, v]) => ({ key: k, value: v }));

      optionsList.forEach(({ key, value }) => {
        if (yPosition > pageHeight - 40) {
          doc.addPage();
          yPosition = margin;
        }
        
        const isCorrect = mcq.answer === key;
        const isUserAnswer = showResults && userAnswers[index] === key;
        
        if (isCorrect) {
          doc.setFont('helvetica', 'bold');
          doc.setTextColor(0, 128, 0); // Green for correct
        } else if (isUserAnswer) {
          doc.setFont('helvetica', 'normal');
          doc.setTextColor(255, 0, 0); // Red for wrong user answer
        } else {
          doc.setFont('helvetica', 'normal');
          doc.setTextColor(0, 0, 0);
        }
        
        const optionText = `   ${key}. ${value}`;
        const splitOption = doc.splitTextToSize(optionText, pageWidth - 2 * margin - 10);
        doc.text(splitOption, margin, yPosition);
        yPosition += 7 * splitOption.length;
      });

      doc.setTextColor(0, 0, 0);
      yPosition += 8;
    });

    // Footer
    const totalPages = doc.internal.pages.length - 1;
    for (let i = 1; i <= totalPages; i++) {
      doc.setPage(i);
      doc.setFontSize(10);
      doc.setFont('helvetica', 'normal');
      doc.text(
        `Generated by PDF2MCQ | Page ${i} of ${totalPages}`,
        pageWidth / 2,
        pageHeight - 10,
        { align: 'center' }
      );
    }

    doc.save(showResults ? 'quiz-results.pdf' : 'mcq-questions.pdf');
  };

  const { correct, total } = calculateScore();
  const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;

  return (
    <section className="py-20 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gradient">
            {showResults ? 'Quiz Results' : 'Attempt Quiz'}
          </h2>
          <p className="text-gray-400">
            {showResults 
              ? `You scored ${percentage}% - ${correct} out of ${total} correct`
              : `${mcqs.length} question${mcqs.length !== 1 ? 's' : ''} - Select your answers`}
          </p>
        </motion.div>

        {/* Action Buttons - Top */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="flex flex-col sm:flex-row flex-wrap justify-center gap-3 sm:gap-4 mb-6 sm:mb-8 px-4"
        >
          {/* Primary Action: Check Answers / Show Answers */}
          {!showResults ? (
            <motion.button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleCheckAnswers();
              }}
              className="px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold flex items-center space-x-2 hover:shadow-lg hover:shadow-indigo-500/50 transition-all cursor-pointer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <CheckCircle2 className="w-5 h-5" />
              <span>Check Answers</span>
            </motion.button>
          ) : null}
          {showResults && onViewAnswers ? (
            <motion.button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                onViewAnswers();
              }}
              className="px-8 py-4 rounded-xl bg-gradient-to-r from-purple-500 to-pink-600 text-white font-semibold flex items-center space-x-2 hover:shadow-lg hover:shadow-purple-500/50 transition-all cursor-pointer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Eye className="w-5 h-5" />
              <span>Show Answers</span>
            </motion.button>
          ) : null}
          
          {/* Secondary Action: Download PDF */}
          <motion.button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              handleDownload();
            }}
            className="px-8 py-4 rounded-xl glass border border-green-500/40 text-white font-semibold flex items-center space-x-2 hover:bg-green-500/20 hover:border-green-500/60 transition-all cursor-pointer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Download className="w-5 h-5 text-green-400" />
            <span>Download PDF</span>
          </motion.button>
          
          {/* Tertiary Action: Start Over */}
          <motion.button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              onReset();
            }}
            className="px-8 py-4 rounded-xl glass border border-white/10 text-gray-400 font-semibold flex items-center space-x-2 hover:bg-white/5 hover:border-white/20 hover:text-white transition-all cursor-pointer"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <RotateCcw className="w-5 h-5" />
            <span>Start Over</span>
          </motion.button>
        </motion.div>

        {/* Results Banner */}
        <AnimatePresence>
          {showResults && (
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.9 }}
              className="mb-6 sm:mb-8 p-4 sm:p-6 rounded-2xl glass border border-white/10 text-center"
            >
              <h3 className="text-xl sm:text-2xl font-bold mb-2 text-white">
                Your Score
              </h3>
              <div className="text-4xl sm:text-5xl font-bold mb-2">
                <span className={`${percentage >= 70 ? 'text-green-400' : percentage >= 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                  {percentage}%
                </span>
              </div>
              <p className="text-gray-400">
                {correct} out of {total} correct
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* MCQ Cards */}
        <div className="space-y-6 mb-8">
          {mcqs.map((mcq, index) => (
            <MCQCard
              key={index}
              mcq={mcq}
              index={index}
              userAnswer={userAnswers[index]}
              onAnswerSelect={(option) => handleAnswerSelect(index, option)}
              showResults={showResults}
            />
          ))}
        </div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: mcqs.length * 0.1 }}
          className="flex flex-col sm:flex-row flex-wrap justify-center gap-3 sm:gap-4 px-4"
        >
          {/* Primary Action: Check Answers / Show Answers */}
          {!showResults ? (
            <motion.button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleCheckAnswers();
              }}
              className="w-full sm:w-auto px-6 sm:px-8 py-3 sm:py-4 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold flex items-center justify-center space-x-2 hover:shadow-lg hover:shadow-indigo-500/50 transition-all cursor-pointer text-sm sm:text-base"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <CheckCircle2 className="w-5 h-5" />
              <span>Check Answers</span>
            </motion.button>
          ) : null}
          {showResults && onViewAnswers ? (
            <motion.button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                onViewAnswers();
              }}
              className="w-full sm:w-auto px-6 sm:px-8 py-3 sm:py-4 rounded-xl bg-gradient-to-r from-purple-500 to-pink-600 text-white font-semibold flex items-center justify-center space-x-2 hover:shadow-lg hover:shadow-purple-500/50 transition-all cursor-pointer text-sm sm:text-base"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Eye className="w-5 h-5" />
              <span>Show Answers</span>
            </motion.button>
          ) : null}
          
          {/* Secondary Action: Download PDF */}
          <motion.button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              handleDownload();
            }}
            className="w-full sm:w-auto px-6 sm:px-8 py-3 sm:py-4 rounded-xl glass border border-green-500/40 text-white font-semibold flex items-center justify-center space-x-2 hover:bg-green-500/20 hover:border-green-500/60 transition-all cursor-pointer text-sm sm:text-base"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Download className="w-5 h-5 text-green-400" />
            <span>Download PDF</span>
          </motion.button>
          
          {/* Tertiary Action: Start Over */}
          <motion.button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              onReset();
            }}
            className="w-full sm:w-auto px-6 sm:px-8 py-3 sm:py-4 rounded-xl glass border border-white/10 text-gray-400 font-semibold flex items-center justify-center space-x-2 hover:bg-white/5 hover:border-white/20 hover:text-white transition-all cursor-pointer text-sm sm:text-base"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <RotateCcw className="w-5 h-5" />
            <span>Start Over</span>
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
};

export default MCQDisplay;
