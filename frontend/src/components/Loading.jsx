import React from 'react';
import './Loading.css';

function Loading() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Processing your request...</p>
      <p className="loading-subtext">This may take a moment</p>
    </div>
  );
}

export default Loading;
