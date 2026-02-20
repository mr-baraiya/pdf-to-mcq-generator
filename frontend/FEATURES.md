# Frontend Features

## User Interface Components

### 1. AI Model Selection Dropdown

Users can now choose which AI model to use for MCQ generation:

**Available Options:**
- **✨ Auto (Recommended)** - Smart fallback system
  - Automatically tries: Ollama → Groq → Gemini
  - Best for reliability
  - No manual configuration needed

- **🏠 Ollama** - Local & Free
  - Private, no data sent to cloud
  - No API costs
  - Requires Ollama running locally

- **⚡ Groq** - Fast Cloud
  - Very fast inference (3-5 seconds)
  - Cloud-based using Llama 3.3 70B
  - Requires Groq API key (backend)

- **🧠 Gemini** - Advanced AI
  - Best for complex documents
  - Google's advanced AI
  - Requires Gemini API key (backend)

### 2. Number of Questions Dropdown

Users can select how many questions to generate:

**Available Options:**
- 3 Questions
- 5 Questions
- 10 Questions (default)
- 15 Questions
- 20 Questions
- 25 Questions
- 30 Questions

**Note:** More questions = longer generation time

---

## Technical Implementation

### State Management

```javascript
// In App.jsx
const [selectedModel, setSelectedModel] = useState('auto');
const [numQuestions, setNumQuestions] = useState(10);
```

### API Endpoint Selection

The frontend automatically selects the correct API endpoint based on the selected model:

```javascript
let endpoint = '/api/generate-mcqs'; // auto fallback
if (model === 'ollama') endpoint = '/api/generate-mcqs-ollama';
else if (model === 'groq') endpoint = '/api/generate-mcqs-groq';
else if (model === 'gemini') endpoint = '/api/generate-mcqs-gemini';
```

### Props Flow

```
App.jsx
  ↓ (props)
FileUpload.jsx
  - selectedModel
  - onModelChange
  - numQuestions
  - onNumQuestionsChange
```

---

## User Experience Flow

1. **User uploads PDF**
   - Drag & drop or click to browse
   - File validation (PDF only, up to 10MB)

2. **User configures settings**
   - Select AI model from dropdown
   - Choose number of questions
   - Real-time help text updates based on selection

3. **Generation starts automatically**
   - Uses selected model and question count
   - Shows loading animation with progress stages
   - Displays error if model unavailable

4. **Results displayed**
   - Can generate more questions with same settings
   - View as quiz or see answers
   - Download as PDF

---

## UI Design

### Dropdown Styling

```css
/* Glass morphism effect */
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Interactive states */
hover:border-indigo-400/50
focus:ring-2 focus:ring-indigo-500
disabled:opacity-50
```

### Layout

```
┌─────────────────────────────────────────┐
│         PDF Upload Area                 │
│   (Drag & Drop / Click to Browse)      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  ✨ Generation Settings                 │
│                                         │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │ AI Model     │  │ # of Questions  │ │
│  │ [Dropdown ▼] │  │ [Dropdown ▼]   │ │
│  └──────────────┘  └─────────────────┘ │
│                                         │
│  • Help text based on selection         │
└─────────────────────────────────────────┘
```

---

## Integration with Backend

### Environment Configuration

Frontend connects to backend via:

```env
# frontend/.env
VITE_API_URL=http://localhost:8000
```

### API Calls

```javascript
// Upload PDF
POST /api/upload-pdf
FormData: { file: pdfFile }

// Generate MCQs (model-specific)
POST /api/generate-mcqs-{model}
Body: {
  text: "extracted text...",
  num_questions: 10
}
```

### Error Handling

```javascript
// Handle model-specific errors
try {
  const response = await axios.post(endpoint, data);
} catch (err) {
  if (err.response?.status === 503) {
    // Ollama not running
    setError('Ollama is not running. Please start Ollama or choose a different model.');
  } else if (err.response?.status === 500) {
    // API key missing or generation failed
    setError('Generation failed. Try a different model or check backend configuration.');
  }
}
```

---

## Development

### Running Locally

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### Building for Production

```bash
npm run build
```

Output in `dist/` directory

---

## Responsive Design

The dropdowns and UI adapt to different screen sizes:

- **Desktop:** Side-by-side dropdowns (2 columns)
- **Mobile/Tablet:** Stacked dropdowns (1 column)
- **Touch-friendly:** Large touch targets, clear labels

---

## Future Enhancements

Potential improvements:

1. **AI Status Indicator**
   - Show which models are currently available
   - Display green/red status dots
   - Check `/ai-status` endpoint on page load

2. **Advanced Options**
   - Custom temperature/creativity settings
   - Question difficulty level
   - Topic focus selection

3. **History & Favorites**
   - Save generated questions
   - Star favorite questions
   - Export history

4. **Real-time Generation Progress**
   - Show percentage complete
   - Estimated time remaining
   - Cancel generation option

---

## Troubleshooting

### Dropdown Not Updating

- Check if state is properly connected
- Verify onChange handlers are called
- Check browser console for errors

### Model Selection Not Working

- Verify backend is running on correct port
- Check VITE_API_URL in .env file
- Test endpoints manually with curl/Postman

### Style Issues

- Clear browser cache
- Rebuild Tailwind: `npm run build`
- Check for conflicting CSS classes

---

## Related Documentation

- [Backend API Endpoints](../backend/API_ENDPOINTS.md)
- [Ollama Auto Install](../backend/OLLAMA_AUTO_INSTALL.md)
- [Environment Configuration](../backend/ENV_CONFIGURATION.md)
