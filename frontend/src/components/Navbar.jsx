import { motion } from 'framer-motion';
import { Github } from 'lucide-react';

const Navbar = ({ onLogoClick }) => {
  return (
    <motion.nav 
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand */}
          <motion.button
            onClick={onLogoClick}
            className="flex items-center space-x-3 cursor-pointer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            <div className="relative">
              <img 
                src="/assets/p2m-logo.png" 
                alt="PDF2MCQ Logo" 
                className="w-14 h-14 object-contain border-2 border-indigo-500 rounded-lg p-1"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'block';
                }}
              />
              <div className="hidden">
                <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-2xl border-2 border-indigo-400">
                  P2M
                </div>
              </div>
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-gradient">
                PDF2MCQ
              </h1>
            </div>
          </motion.button>

          {/* Navigation Links */}
          <div className="flex items-center space-x-2 sm:space-x-6">
            <motion.a
              href="#features"
              className="text-xs sm:text-sm text-gray-300 hover:text-white transition-colors hidden sm:block"
              whileHover={{ y: -2 }}
              whileTap={{ scale: 0.95 }}
            >
              Features
            </motion.a>
            <motion.a
              href="mailto:baraiyavishalbhai32@gmail.com"
              className="text-xs sm:text-sm text-gray-300 hover:text-white transition-colors hidden md:block"
              whileHover={{ y: -2 }}
              whileTap={{ scale: 0.95 }}
            >
              Contact
            </motion.a>
            <motion.a
              href="https://github.com/mr-baraiya/pdf-to-mcq-generator"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 px-3 sm:px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 transition-all group"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Github className="w-4 h-4 sm:w-5 sm:h-5" />
              <span className="text-xs sm:text-sm hidden sm:inline">GitHub</span>
            </motion.a>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;
