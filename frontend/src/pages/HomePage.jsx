import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Hero from '../components/Hero';
import Features from '../components/Features';

function HomePage() {
  const navigate = useNavigate();
  const [showDemo, setShowDemo] = useState(false);

  const handleGetStarted = () => {
    navigate('/generator');
  };

  return (
    <>
      <Hero onGetStarted={handleGetStarted} />
      <Features />
      <section className="relative py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 via-white/3 to-transparent px-6 py-12 text-center md:px-12">
            <h2 className="text-3xl md:text-4xl font-bold text-white">Project Idea</h2>
            <p className="text-gray-300 mt-3">
              Instantly convert PDFs into high-quality MCQs with AI.
            </p>
            <div className="mt-6 flex justify-center">
              <button
                type="button"
                onClick={() => setShowDemo(true)}
                className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 px-6 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition hover:from-indigo-400 hover:to-purple-500"
              >
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </section>

      <AnimatePresence>
        {showDemo && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowDemo(false)}
          >
            <motion.div
              className="relative w-full max-w-5xl overflow-hidden rounded-2xl border border-white/10 bg-black/90 shadow-2xl"
              initial={{ opacity: 0, y: 20, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 20, scale: 0.98 }}
              transition={{ type: 'spring', stiffness: 220, damping: 24 }}
              onClick={e => e.stopPropagation()}
            >
              <button
                type="button"
                className="absolute right-3 top-3 z-10 rounded-full border border-white/10 bg-white/10 px-3 py-1 text-xs font-semibold text-white hover:bg-white/20"
                onClick={() => setShowDemo(false)}
                aria-label="Close demo"
              >
                Close
              </button>
              <div className="relative pt-[56.25%]">
                <iframe
                  className="absolute inset-0 h-full w-full"
                  src="https://www.youtube.com/embed/Tf-Ylb-x7fc"
                  title="PDF to MCQ Generator Demo"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  referrerPolicy="strict-origin-when-cross-origin"
                  allowFullScreen
                />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

export default HomePage;
