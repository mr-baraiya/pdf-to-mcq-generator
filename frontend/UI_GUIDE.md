# Frontend UI Update - Dropdown Menus

## ✨ New Features Added

### 1. AI Model Selection Dropdown
**Location:** Below the PDF upload area  
**Default:** Auto (Recommended)

```
┌──────────────────────────────────────────────┐
│ AI Model                                    │
│ ┌────────────────────────────────────────┐ │
│ │ ✨ Auto (Recommended) - Smart Fallback ▼│ │
│ └────────────────────────────────────────┘ │
│ • Tries Ollama → Groq → Gemini             │
└──────────────────────────────────────────────┘
```

**Dropdown Options:**
```
┌────────────────────────────────────────┐
│ ✨ Auto (Recommended) - Smart Fallback │
│ 🏠 Ollama - Local & Free              │
│ ⚡ Groq - Fast Cloud                   │
│ 🧠 Gemini - Advanced AI                │
└────────────────────────────────────────┘
```

### 2. Number of Questions Dropdown
**Location:** Next to AI Model dropdown (side-by-side on desktop)  
**Default:** 10 Questions

```
┌──────────────────────────────────────────────┐
│ Number of Questions                         │
│ ┌────────────────────────────────────────┐ │
│ │ 10 Questions                          ▼│ │
│ └────────────────────────────────────────┘ │
│ • More questions = longer generation time  │
└──────────────────────────────────────────────┘
```

**Dropdown Options:**
```
┌────────────────────┐
│ 3 Questions       │
│ 5 Questions       │
│ 10 Questions      │ ← Default
│ 15 Questions      │
│ 20 Questions      │
│ 25 Questions      │
│ 30 Questions      │
└────────────────────┘
```

---

## 📱 Complete UI Layout

```
╔══════════════════════════════════════════════════════════╗
║                    PDF2MCQ Navbar                        ║
╚══════════════════════════════════════════════════════════╝

                  Upload Your PDF
        Drag and drop your PDF or click to browse

┌──────────────────────────────────────────────────────────┐
│                                                          │
│                    📄 Upload Area                        │
│              (Drag & Drop / Click to Browse)             │
│                                                          │
│                  Supports PDF files up to 10MB           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  ✨ Generation Settings                                  │
│                                                          │
│  ┌─────────────────────────┐  ┌──────────────────────┐ │
│  │ AI Model                │  │ Number of Questions  │ │
│  │ ┌───────────────────┐   │  │ ┌────────────────┐  │ │
│  │ │ Auto (Rec.) ▼     │   │  │ │ 10 Questions ▼ │  │ │
│  │ └───────────────────┘   │  │ └────────────────┘  │ │
│  │ • Smart fallback        │  │ • Longer = more time│ │
│  └─────────────────────────┘  └──────────────────────┘ │
└──────────────────────────────────────────────────────────┘

        Your file is processed securely and 
             deleted after generation
```

---

## 🎨 Visual Features

### Glass Morphism Design
- Semi-transparent backgrounds with blur effect
- Subtle borders and hover effects
- Smooth transitions and animations

### Interactive States

**Normal:**
```
┌────────────────────────┐
│ Select Model      ▼   │
└────────────────────────┘
```

**Hover:**
```
┌────────────────────────┐ ← Border glows indigo
│ Select Model      ▼   │   Background brightens
└────────────────────────┘
```

**Focused:**
```
╔════════════════════════╗ ← Indigo ring appears
║ Select Model      ▼   ║   Border highlighted
╚════════════════════════╝
```

**Disabled:**
```
┌────────────────────────┐
│ Select Model      ▼   │ ← Grayed out, 50% opacity
└────────────────────────┘
```

---

## 🔄 User Flow

### Step-by-Step Interaction

**1. Initial Load**
```
• Hero section visible
• "Get Started" button
• Features showcase
```

**2. User Clicks "Get Started"**
```
• Scrolls to upload section
• Shows PDF upload area
• Generation settings visible below
• Default: Auto model, 10 questions
```

**3. User Configures Settings**
```
┌──────────────────────┐     ┌──────────────────┐
│ Click dropdown       │ →   │ Options appear   │
│ ✨ Auto (Rec.) ▼    │     │ • Auto           │
│                      │     │ • Ollama         │
└──────────────────────┘     │ • Groq           │
                             │ • Gemini         │
                             └──────────────────┘
                                     ↓
                             User selects option
                                     ↓
                             Help text updates
```

**4. User Uploads PDF**
```
• Drag file or click to browse
• File validation
• Automatic upload
• Extraction starts
```

**5. Generation Begins**
```
• Uses selected model
• Uses selected question count
• Loading animation
• Progress stages shown
```

**6. Results Displayed**
```
• Questions appear
• Can attempt quiz
• Can view answers
• Can generate more (uses same settings)
```

---

## 💡 Smart Features

### Context-Aware Help Text

Each model selection shows relevant information:

```javascript
Auto:      "• Tries Ollama → Groq → Gemini"
Ollama:    "• Private, no API costs (requires Ollama running)"
Groq:      "• Very fast inference, cloud-based"
Gemini:    "• Best for complex documents"
```

### Question Count Hint
```
"• More questions = longer generation time"
```

---

## 🎯 Technical Details

### Component Updates

**App.jsx** - Added state:
```javascript
const [selectedModel, setSelectedModel] = useState('auto');
const [numQuestions, setNumQuestions] = useState(10);
```

**FileUpload.jsx** - Added props:
```javascript
const FileUpload = ({ 
  onFileSelect, 
  loading,
  selectedModel,
  onModelChange,
  numQuestions,
  onNumQuestionsChange
}) => {
  // Dropdown UI rendering
}
```

### Icons Used
- ✨ Sparkles (Settings header)
- 🏠 Home (Ollama)
- ⚡ Zap (Groq)
- 🧠 Brain (Gemini)
- 🔽 ChevronDown (Dropdown indicator)

---

## 📊 Model Comparison

| Model    | Speed      | Cost      | Privacy   | Requirements      |
|----------|------------|-----------|-----------|-------------------|
| Auto     | Variable   | Variable  | Variable  | None (fallback)   |
| Ollama   | Medium     | Free      | 100%      | Local install     |
| Groq     | Fast       | API key   | Cloud     | API key           |
| Gemini   | Medium     | API key   | Cloud     | API key           |

---

## 🚀 Testing the UI

### Local Development

1. **Start Backend:**
```bash
cd backend
uvicorn index:app --reload --host 0.0.0.0 --port 8000
```

2. **Start Frontend:**
```bash
cd frontend
npm install    # if first time
npm run dev
```

3. **Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Test Scenarios

**Scenario 1: Default Settings**
- Upload PDF
- Leave "Auto" model selected
- Leave "10 Questions" selected
- Verify generation works

**Scenario 2: Groq Selection**
- Select "Groq - Fast Cloud"
- Select "5 Questions"
- Upload PDF
- Verify Groq endpoint is called
- Check for faster generation

**Scenario 3: Ollama Selection**
- Select "Ollama - Local & Free"
- Select "15 Questions"
- If Ollama not running: See error
- If Ollama running: See generation

**Scenario 4: More Questions**
- Generate initial set
- Click "Generate More"
- Verify same model/count is used
- New questions append to existing

---

## 📸 Key UI Elements

### Dropdown Styling Classes

```css
/* Base dropdown */
glass rounded-xl px-4 py-3
border border-white/10
text-white bg-white/5

/* Hover state */
hover:border-indigo-400/50
hover:bg-white/10

/* Focus state */
focus:ring-2 focus:ring-indigo-500
focus:border-transparent

/* Disabled state */
disabled:opacity-50
disabled:cursor-not-allowed
```

### Grid Layout

```css
/* Desktop: 2 columns */
grid grid-cols-1 md:grid-cols-2 gap-4

/* Mobile: 1 column (stacked) */
```

---

## ✅ Testing Checklist

- [x] Dropdowns render correctly
- [x] Default values set properly (Auto, 10)
- [x] Dropdown options display with emojis
- [x] Help text updates on selection
- [x] State propagates to parent (App.jsx)
- [x] API endpoint changes based on model
- [x] Generate More uses saved settings
- [x] Responsive on mobile/tablet
- [x] Hover/focus states work
- [x] Disabled state during loading
- [x] Icons display correctly
- [x] Smooth animations

---

## 🎓 For Frontend Developers

### Adding New Model Options

1. **Add to backend** (create endpoint)
2. **Update dropdown** in FileUpload.jsx:
```javascript
<option value="new-model">
  🆕 New Model - Description
</option>
```

3. **Update endpoint logic** in App.jsx:
```javascript
else if (model === 'new-model') 
  endpoint = '/api/generate-mcqs-new-model';
```

4. **Add help text**:
```javascript
{selectedModel === 'new-model' && '• Help text here'}
```

### Adding New Question Counts

Simply add to dropdown:
```javascript
<option value="50">50 Questions</option>
```

No backend changes needed!

---

## 📚 Related Files

- Frontend:
  - [src/App.jsx](../frontend/src/App.jsx) - Main app logic
  - [src/components/FileUpload.jsx](../frontend/src/components/FileUpload.jsx) - Upload & settings UI
  - [frontend/FEATURES.md](FEATURES.md) - Detailed features doc

- Backend:
  - [backend/routes.py](../backend/routes.py) - All API endpoints
  - [backend/API_ENDPOINTS.md](../backend/API_ENDPOINTS.md) - API documentation
