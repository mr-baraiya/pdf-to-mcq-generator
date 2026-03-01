import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import GeneratorPage from './pages/GeneratorPage';
import AnimatedBackground from './components/AnimatedBackground';

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white relative overflow-x-hidden">
      {/* Animated Background */}
      <AnimatedBackground />

      {/* Navbar */}
      <Navbar />

      {/* Main Content */}
      <div className="relative z-10">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/generator" element={<GeneratorPage />} />
        </Routes>
      </div>

      {/* Footer */}
      <footer className="relative z-10 py-8 px-4 border-t border-white/10 mt-20">
        <div className="max-w-7xl mx-auto text-center text-gray-400 text-sm">
          <p>© 2026 PDF2MCQ. Built with ❤️ using React, Tailwind, and AI.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
