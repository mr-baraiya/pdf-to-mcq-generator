import React, { useState } from 'react';
import './MCQDisplay.css';

function MCQDisplay({ mcqs, onReset }) {
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

  const { correct, total } = calculateScore();
  const percentage = Math.round((correct / total) * 100);

  return (
    <div className="mcq-display">
      {showResults && (
        <div className="results-banner">
          <h2>Results</h2>
          <p className="score">
            You got <span className={percentage >= 70 ? 'good' : 'needs-improvement'}>
              {correct}/{total}
            </span> correct ({percentage}%)
          </p>
        </div>
      )}

      <div className="questions-container">
        {mcqs.map((mcq, index) => (
          <div key={index} className="question-card">
            <div className="question-number">Question {index + 1}</div>
            <h3 className="question-text">{mcq.question}</h3>
            
            <div className="options">
              {Object.entries(mcq.options).map(([key, value]) => {
                const isSelected = userAnswers[index] === key;
                const isCorrect = key === mcq.answer;
                const showCorrect = showResults && isCorrect;
                const showIncorrect = showResults && isSelected && !isCorrect;

                return (
                  <button
                    key={key}
                    className={`option ${isSelected ? 'selected' : ''} ${
                      showCorrect ? 'correct' : ''
                    } ${showIncorrect ? 'incorrect' : ''}`}
                    onClick={() => !showResults && handleAnswerSelect(index, key)}
                    disabled={showResults}
                  >
                    <span className="option-label">{key}.</span>
                    <span className="option-text">{value}</span>
                    {showResults && isCorrect && <span className="checkmark">✓</span>}
                    {showResults && isSelected && !isCorrect && <span className="cross">✕</span>}
                  </button>
                );
              })}
            </div>

            {showResults && (
              <div className="answer-feedback">
                <p className="correct-answer">
                  <strong>Correct Answer:</strong> {mcq.answer}. {mcq.options[mcq.answer]}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="action-buttons">
        {!showResults && (
          <button className="btn-primary" onClick={handleCheckAnswers}>
            Check Answers
          </button>
        )}
        <button className="btn-secondary" onClick={onReset}>
          Generate New Questions
        </button>
      </div>
    </div>
  );
}

export default MCQDisplay;
