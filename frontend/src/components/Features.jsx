import { motion } from 'framer-motion';
import { Zap, Shield, Sparkles, Download, Clock, FileCheck } from 'lucide-react';

const features = [
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Generate MCQs from your PDFs in seconds with our optimized AI engine',
    color: 'from-yellow-400 to-orange-500'
  },
  {
    icon: Sparkles,
    title: 'Smart Questions',
    description: 'Advanced technology ensures high-quality, contextually relevant questions',
    color: 'from-indigo-400 to-purple-500'
  },
  {
    icon: Shield,
    title: 'Secure & Private',
    description: 'Your files are processed securely and deleted immediately after generation',
    color: 'from-green-400 to-emerald-500'
  },
  {
    icon: FileCheck,
    title: 'Smart Extraction',
    description: 'Accurately extracts and processes text from complex PDF documents',
    color: 'from-blue-400 to-cyan-500'
  },
  {
    icon: Clock,
    title: 'Save Time',
    description: 'Create comprehensive MCQs in minutes instead of hours of manual work',
    color: 'from-pink-400 to-rose-500'
  },
  {
    icon: Download,
    title: 'Easy Export',
    description: 'Download your generated MCQs in multiple formats for immediate use',
    color: 'from-violet-400 to-purple-500'
  }
];

const FeatureCard = ({ feature, index }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className="group relative"
    >
      <div className="relative glass rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all h-full">
        {/* Glow Effect on Hover */}
        <div className={`absolute -inset-0.5 bg-gradient-to-r ${feature.color} rounded-2xl opacity-0 group-hover:opacity-20 blur transition-opacity duration-500`} />
        
        <div className="relative">
          {/* Icon */}
          <motion.div
            className="mb-4"
            whileHover={{ scale: 1.1, rotate: 5 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            <div className={`inline-flex p-3 rounded-xl bg-gradient-to-r ${feature.color} bg-opacity-10`}>
              <feature.icon className="w-6 h-6 text-white" />
            </div>
          </motion.div>

          {/* Content */}
          <h3 className="text-xl font-semibold text-white mb-2">
            {feature.title}
          </h3>
          <p className="text-gray-400 text-sm leading-relaxed">
            {feature.description}
          </p>
        </div>
      </div>
    </motion.div>
  );
};

const Features = () => {
  return (
    <section id="features" className="py-20 px-4 relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-indigo-500/5 to-transparent pointer-events-none" />
      
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="inline-flex items-center space-x-2 px-4 py-2 rounded-full glass border border-white/20 mb-6"
          >
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span className="text-sm text-gray-300">Why Choose PDF2MCQ</span>
          </motion.div>
          
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-gradient">
            Powerful Features
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Everything you need to create high-quality MCQs from your PDF documents
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard key={index} feature={feature} index={index} />
          ))}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-center mt-16"
        >
          <p className="text-gray-400 mb-4">
            Ready to transform your PDFs into MCQs?
          </p>
          <motion.button
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            className="px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold hover:shadow-lg hover:shadow-indigo-500/50 transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Get Started Now
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
};

export default Features;
