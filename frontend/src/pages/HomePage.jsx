import { useNavigate } from 'react-router-dom';
import Hero from '../components/Hero';
import Features from '../components/Features';

function HomePage() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/generator');
  };

  return (
    <>
      <Hero onGetStarted={handleGetStarted} />
      <Features />
    </>
  );
}

export default HomePage;
