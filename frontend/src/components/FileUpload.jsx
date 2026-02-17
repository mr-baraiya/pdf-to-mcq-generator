import React, { useRef } from 'react';
import { FiUploadCloud } from 'react-icons/fi';
import './FileUpload.css';

function FileUpload({ onFileSelect, loading }) {
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
  };

  const handleDragLeave = (e) => {
    e.currentTarget.classList.remove('drag-over');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileChange(files[0]);
    }
  };

  const handleFileChange = (file) => {
    if (file && file.type === 'application/pdf') {
      onFileSelect(file);
    } else {
      alert('Please select a valid PDF file');
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleInputChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileChange(file);
    }
  };

  return (
    <div className="file-upload">
      <div
        className="upload-zone"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <FiUploadCloud size={48} className="upload-icon" />
        <h2>Upload PDF Document</h2>
        <p>Drag and drop your PDF here, or click to select</p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleInputChange}
          disabled={loading}
          style={{ display: 'none' }}
        />
        <button className="btn-primary" disabled={loading}>
          {loading ? 'Uploading...' : 'Choose File'}
        </button>
      </div>
    </div>
  );
}

export default FileUpload;
