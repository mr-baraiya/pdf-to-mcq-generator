# Frontend Development Guide

## Project Overview

This is a React application built with Vite that serves as the user interface for the PDF to MCQ Generator. It communicates with a FastAPI backend to upload PDFs and generate MCQs.

## Technologies

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **React Icons** - Icon library
- **CSS 3** - Styling

## Project Structure

```
frontend/
 index.html              # Entry HTML file
 package.json            # Dependencies and scripts
 vite.config.js         # Vite configuration
 .gitignore
 src/
     main.jsx           # React-DOM render entry
     App.jsx            # Main App component
     App.css            # App-level styles
     index.css          # Global styles
     components/
         FileUpload.jsx     # PDF upload with drag-drop
         FileUpload.css
         MCQDisplay.jsx     # Question and answer display
         MCQDisplay.css
         Loading.jsx        # Loading spinner
         Loading.css
```

## Component Architecture

### App Component (App.jsx)

Main container component that manages:
- PDF upload state
- Extracted text state
- MCQ data state
- Loading and error states
- Routing between upload and MCQ display

#### Props: None
#### State:
- `mcqs` - Array of generated questions
- `loading` - Loading state
- `error` - Error messages
- `extractedText` - Text extracted from PDF

#### Methods:
- `handleFileUpload()` - Calls `/upload-pdf` endpoint
- `handleGenerateMCQs()` - Calls `/generate-mcqs` endpoint

### FileUpload Component

Handles PDF file upload with:
- Drag-and-drop support
- File validation
- Visual feedback

#### Props:
- `onFileSelect(file)` - Callback when file is selected
- `loading` - Boolean loading state

### MCQDisplay Component

Displays questions and manages quiz interaction:
- Shows all questions
- Allows answer selection
- Shows correct answers after submission
- Calculates score

#### Props:
- `mcqs` - Array of question objects
- `onReset()` - Callback to reset and generate new questions

#### State:
- `userAnswers` - Object mapping question index to selected answer
- `showResults` - Boolean to show results

### Loading Component

Simple loading spinner for UI feedback

## API Integration

### Endpoints Used

1. **POST /upload-pdf**
   - Sends: FormData with PDF file
   - Receives: { filename, text, status }
   - Used in: handleFileUpload()

2. **POST /generate-mcqs**
   - Sends: { text, num_questions }
   - Receives: { questions, status }
   - Used in: handleGenerateMCQs()

### Configuration

The API URL is configured in Vite config:
```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

But the app uses the full URL directly. For production, update API URL in `App.jsx`:
```javascript
const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';
```

## Styling

### Token System

```css
/* Colors */
Primary Gradient: #667eea  #764ba2
White: #ffffff
Dark Text: #333333
Light Text: #666666
Success: #28a745
Error: #dc3545
Warning: #fbbf24
```

### Responsive Design

- Desktop: Full layout (1024px)
- Tablet: Adjusted spacing (768px-1023px)
- Mobile: Stacked layout (<768px)

## Development Workflow

### Starting Development Server

```bash
npm install
npm run dev
```

Server runs at: `http://localhost:3000`

### Making Changes

1. Edit files in `src/`
2. Vite automatically refreshes the browser (Hot Module Replacement)
3. Check browser console for any errors

### Building for Production

```bash
npm run build
```

Outputs optimized bundle to `dist/` folder

---

## Component Lifecycle

```

          App Component             

                 
        
         No PDF uploaded?  
        
                 
        
          Show FileUpload  
            Component      
        
                 
        User chooses file
                 
        
         Upload PDF to API 
         (POST /upload-pdf)
        
                 
        
         PDF extracted OK? 
        
                 
        
         Show Generate     
          MCQs Options     
        
                 
        User clicks "Generate N Questions"
                 
        
        Generate MCQs from 
        API (POST /gen..)  
        
                 
        
         Show MCQDisplay   
           Component       
        
                 
        User answers questions
                 
        
         Show Results and  
            Score          
        
                 
        User clicks "Generate New Questions"
                 
        
         Reset MCQ state   
         Go to step 4      
        
```

## Common Tasks

### Add a New Component

1. Create `src/components/ComponentName.jsx`
2. Create `src/components/ComponentName.css`
3. Import in `App.jsx`: `import Component from './components/Component'`
4. Use in JSX: `<Component prop={value} />`

### Modify API Endpoint

Update the URL in `App.jsx`:
```javascript
const response = await axios.post('http://localhost:8000/endpoin...', ...)
```

### Change Styling

- Global styles: `src/index.css`
- Component styles: `src/components/ComponentName.css`
- App-level styles: `src/App.css`

### Add Error Handling

Errors are already caught and displayed at the top of the page:
```javascript
setError('Your error message')
```

## Testing

### Manual Testing Checklist

- [ ] PDF upload with drag-drop
- [ ] PDF upload with file selector
- [ ] Error on non-PDF file
- [ ] Text extraction displays correctly
- [ ] MCQ generation for different counts
- [ ] Answer selection works
- [ ] Score calculation is correct
- [ ] Results display properly
- [ ] Generate new questions works
- [ ] Responsive on mobile/tablet

### Browser Console

Check for:
- JavaScript errors
- API request/response details
- Network issues

## Performance Tips

- React DevTools browser extension for debugging
- Lighthouse for performance audits
- Monitor API response times
- Lazy load components if needed

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Netlify

```bash
npm run build
# Deploy dist folder to Netlify
```

### Traditional Server

```bash
npm run build
# Serve dist folder with nginx/apache
```

---

## Troubleshooting

### "Cannot find module 'react'"
```bash
npm install
```

### "API connection refused"
- Check backend is running on port 8000
- Check API URL in App.jsx

### "Hot reload not working"
- Restart dev server: `npm run dev`
- Check Vite configuration

### "Build fails"
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Axios Guide](https://axios-http.com)
- [React Icons](https://react-icons.github.io/react-icons)
