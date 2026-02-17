import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, RotateCcw, Download } from 'lucide-react';

const MCQCard = ({ mcq, index, userAnswer, onAnswerSelect, showResults }) => {
  const isCorrect = userAnswer === mcq.answer;

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className="glass rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all group"
    >
      <div className="flex items-start justify-between mb-4">
        <span className="text-sm font-semibold text-indigo-400">
          Question {index + 1}
        </span>
        {showResults && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            {isCorrect ? (
              <CheckCircle2 className="w-6 h-6 text-green-400" />
            ) : (
              <XCircle className="w-6 h-6 text-red-400" />
            )}
          </motion.div>
        )}
      </div>

      <h3 className="text-lg font-semibold text-white mb-6">
        {mcq.question}
      </h3>

      <div className="space-y-3">
        {Object.entries(mcq.options).map(([key, value]) => {
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
                w-full text-left p-4 rounded-xl border transition-all
                ${isSelected && !showResults ? 'border-indigo-400 bg-indigo-500/10' : 'border-white/10'}
                ${showCorrect ? 'border-green-400 bg-green-500/10' : ''}
                ${showIncorrect ? 'border-red-400 bg-red-500/10' : ''}
                ${!showResults && !isSelected ? 'hover:border-white/30 hover:bg-white/5' : ''}
                ${showResults ? 'cursor-default' : 'cursor-pointer'}
              `}
              whileHover={!showResults ? { scale: 1.02, x: 4 } : {}}
              whileTap={!showResults ? { scale: 0.98 } : {}}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className={`
                    flex items-center justify-center w-8 h-8 rounded-lg font-semibold
                    ${showCorrect ? 'bg-green-500/20 text-green-400' : ''}
                    ${showIncorrect ? 'bg-red-500/20 text-red-400' : ''}
                    ${!showResults && isSelected ? 'bg-indigo-500/20 text-indigo-400' : ''}
                    ${!showResults && !isSelected ? 'bg-white/5 text-gray-400' : ''}
                  `}>
                    {key}
                  </span>
                  <span className={`
                    ${showCorrect || showIncorrect || isSelected ? 'text-white' : 'text-gray-300'}
                  `}>
                    {value}
                  </span>
                </div>
                {showCorrect && (
                  <CheckCircle2 className="w-5 h-5 text-green-400" />
                )}
                {showIncorrect && (
                  <XCircle className="w-5 h-5 text-red-400" />
                )}
              </div>
            </motion.button>
          );
        })}
      </div>

      {showResults && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mt-4 p-4 rounded-xl bg-white/5 border border-white/10"
        >
          <p className="text-sm text-gray-400">
            <span className="font-semibold text-white">Correct Answer:</span>{' '}
            {mcq.answer}. {mcq.options[mcq.answer]}
          </p>
        </motion.div>
      )}
    </motion.div>
  );
};

const MCQDisplay = ({ mcqs, onReset }) => {
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
    const content = mcqs.map((mcq, idx) => {
      return `Question ${idx + 1}: ${mcq.question}\n${Object.entries(mcq.options)
        .map(([k, v]) => `${k}. ${v}`)
        .join('\n')}\nCorrect Answer: ${mcq.answer}\n\n`;
    }).join('---\n\n');

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'mcqs.txt';
    a.click();
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
            Generated MCQs
          </h2>
          <p className="text-gray-400">
            {mcqs.length} question{mcqs.length !== 1 ? 's' : ''} ready for review
          </p>
        </motion.div>

        {/* Results Banner */}
        <AnimatePresence>
          {showResults && (
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.9 }}
              className="mb-8 p-6 rounded-2xl glass border border-white/10 text-center"
            >
              <h3 className="text-2xl font-bold mb-2 text-white">
                Your Score
              </h3>
              <div className="text-5xl font-bold mb-2">
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
          className="flex flex-wrap justify-center gap-4"
        >
          {!showResults && (
            <motion.button
              onClick={handleCheckAnswers}
              className="px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold flex items-center space-x-2 hover:shadow-lg hover:shadow-indigo-500/50 transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <CheckCircle2 className="w-5 h-5" />
              <span>Check Answers</span>
            </motion.button>
          )}
          <motion.button
            onClick={handleDownload}
            className="px-8 py-4 rounded-xl glass border border-white/20 text-white font-semibold flex items-center space-x-2 hover:bg-white/10 transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Download className="w-5 h-5" />
            <span>Download</span>
          </motion.button>
          <motion.button
            onClick={onReset}
            className="px-8 py-4 rounded-xl glass border border-white/20 text-white font-semibold flex items-center space-x-2 hover:bg-white/10 transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
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
