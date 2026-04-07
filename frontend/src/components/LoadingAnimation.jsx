import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import { Upload, FileSearch, Sparkles, CheckCircle2 } from 'lucide-react';

const LoadingStep = ({ icon: Icon, text, active, completed }) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className={`flex items-center space-x-4 p-4 rounded-xl transition-all duration-300 ${
        active ? 'bg-indigo-500/10 border border-indigo-400/30' : 
        completed ? 'bg-green-500/10 border border-green-400/30' : 
        'bg-white/5 border border-white/10'
      }`}
    >
      <div className={`p-3 rounded-lg ${
        active ? 'bg-indigo-500/20' : 
        completed ? 'bg-green-500/20' : 
        'bg-white/5'
      }`}>
        {completed ? (
          <CheckCircle2 className="w-6 h-6 text-green-400" />
        ) : (
          <Icon className={`w-6 h-6 ${
            active ? 'text-indigo-400 animate-pulse' : 'text-gray-500'
          }`} />
        )}
      </div>
      <span className={`font-medium ${
        active || completed ? 'text-white' : 'text-gray-500'
      }`}>
        {text}
      </span>
    </motion.div>
  );
};

const LoadingAnimation = ({ stage = 'uploading' }) => {
  const progressRef = useRef(null);
  const [currentStep, setCurrentStep] = useState(0);
  
  const steps = [
    { icon: Upload, text: 'Uploading PDF...', id: 'uploading' },
    { icon: FileSearch, text: 'Extracting text...', id: 'extracting' },
    { icon: Sparkles, text: 'Generating MCQs...', id: 'generating' }
  ];

  useEffect(() => {
    const stepIndex = steps.findIndex(s => s.id === stage);
    if (stepIndex >= 0) {
      setCurrentStep(stepIndex);
    }
  }, [stage]);

  useEffect(() => {
    if (progressRef.current) {
      gsap.to(progressRef.current, {
        width: `${((currentStep + 1) / steps.length) * 100}%`,
        duration: 0.8,
        ease: 'power2.out'
      });
    }
  }, [currentStep]);

  return (
    <section className="py-20 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Loading Animation */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center mb-12"
        >
          <motion.div
            className="relative w-24 h-24 mx-auto mb-6"
            animate={{ rotate: 360 }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "linear"
            }}
          >
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 opacity-20 blur-xl" />
            <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-indigo-500 border-r-purple-600" />
          </motion.div>
          <h3 className="text-2xl font-bold text-white mb-2">
            Processing Your PDF
          </h3>
          <p className="text-gray-400">
            This might take 1-2 minutes. Please wait while we generate your MCQs.
          </p>
        </motion.div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="relative h-2 bg-white/5 rounded-full overflow-hidden">
            <div
              ref={progressRef}
              className="absolute left-0 top-0 h-full bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full transition-all duration-300"
              style={{ width: '0%' }}
            />
          </div>
        </div>

        {/* Steps */}
        <div className="space-y-4">
          {steps.map((step, index) => (
            <LoadingStep
              key={step.id}
              icon={step.icon}
              text={step.text}
              active={index === currentStep}
              completed={index < currentStep}
            />
          ))}
        </div>

        {/* Animated Dots */}
        <motion.div
          className="flex justify-center space-x-2 mt-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-2 h-2 bg-indigo-400 rounded-full"
              animate={{
                scale: [1, 1.5, 1],
                opacity: [0.5, 1, 0.5]
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: i * 0.2
              }}
            />
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default LoadingAnimation;
