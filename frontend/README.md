# Frontend - PDF to MCQ Generator

This is the frontend application for the PDF to MCQ Generator, built with React and Vite.

## Directory Structure

```
frontend/
├── src/
│   ├── components/       # React components
│   ├── App.jsx          # Main App component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── index.html          # HTML template
├── vite.config.js      # Vite configuration
├── tailwind.config.js  # Tailwind CSS config
├── package.json        # Dependencies
└── .env                # Environment variables (not in git)
```

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment variables:**
   Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## Environment Variables

See `.env.example` for required environment variables:
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

## Build for Production

```bash
npm run build
```

The production build will be created in the `dist/` directory.

## Features

- PDF file upload
- AI-powered MCQ generation
- Interactive MCQ display
- Export MCQs to various formats
- Modern, responsive UI with Tailwind CSS

## Tech Stack

- **React**: UI library
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **Framer Motion**: Animations
- **Lucide React**: Icons
