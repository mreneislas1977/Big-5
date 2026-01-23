import React, { useState } from 'react';
import { Brain, ArrowRight, Activity, CheckCircle } from 'lucide-react';
import LeadGate from './components/LeadGate';

// --- CONFIGURATION ---
const questions = [
  { id: 1, text: "I am the life of the party.", trait: "Extraversion" },
  { id: 2, text: "I feel little concern for others.", trait: "Agreeableness" },
  { id: 3, text: "I am always prepared.", trait: "Conscientiousness" },
  { id: 4, text: "I get stressed out easily.", trait: "Neuroticism" },
  { id: 5, text: "I have a rich vocabulary.", trait: "Openness" },
];

const Header = () => (
  <header className="bg-brand-green text-white shadow-md sticky top-0 z-50">
    <div className="container mx-auto px-6 py-4 flex justify-between items-center">
      <div className="flex items-center space-x-3">
        <div className="h-8 w-8 bg-brand-gold rounded-sm flex items-center justify-center">
          <Brain className="text-brand-green w-5 h-5" />
        </div>
        <span className="font-heading font-bold text-xl tracking-wide">Crescere <span className="text-brand-gold">Psychometrics</span></span>
      </div>
    </div>
  </header>
);

function App() {
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [showResults, setShowResults] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // --- THE GATE ---
  if (!isUnlocked) {
    return (
      <LeadGate 
        appName="Big 5 Personality Assessment" 
        onUnlock={() => setIsUnlocked(true)} 
      />
    );
  }

  // --- MAIN APP ---
  const handleAnswer = (id: number, val: number) => {
    setAnswers(prev => ({ ...prev, [id]: val }));
  };

  const calculateScores = () => {
    setIsAnalyzing(true);
    // Simulate processing
    setTimeout(() => {
      setIsAnalyzing(false);
      setShowResults(true);
    }, 1500);
  };

  if (showResults) {
    return (
      <div className="min-h-screen bg-brand-cream font-body flex flex-col">
        <Header />
        <main className="flex-grow container mx-auto px-6 py-12 text-center">
           <div className="bg-white p-12 rounded-sm shadow-xl max-w-2xl mx-auto border-t-4 border-brand-green">
              <CheckCircle className="w-16 h-16 text-brand-green mx-auto mb-6" />
              <h2 className="font-heading text-3xl font-bold text-brand-green mb-4">Assessment Complete</h2>
              <p className="text-brand-brown/70 mb-8">
                Thank you for completing the Big 5 Assessment. Your preliminary results indicate high 
                <strong> Conscientiousness</strong> and moderate <strong>Extraversion</strong>.
              </p>
              <div className="bg-brand-green/5 p-6 rounded text-sm text-brand-brown/80 mb-8">
                "Individuals with this profile often excel in strategic leadership roles where detailed execution is as important as vision."
              </div>
              <button 
                onClick={() => { setShowResults(false); setAnswers({}); }}
                className="px-8 py-3 bg-brand-brown text-white font-bold uppercase tracking-widest text-sm rounded hover:bg-brand-green transition-colors"
              >
                Retake
              </button>
           </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-brand-cream font-body flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-6 py-12 max-w-4xl">
        <div className="text-center mb-12">
          <h1 className="font-heading text-4xl font-bold text-brand-green mb-4">The Big 5 Assessment</h1>
          <p className="text-xl text-brand-brown/70">Scientific insight into your leadership personality.</p>
        </div>

        <div className="bg-white rounded-sm shadow-xl p-8 md:p-12 border-t-4 border-brand-gold">
          {isAnalyzing ? (
            <div className="text-center py-12">
               <Activity className="w-12 h-12 text-brand-gold animate-pulse mx-auto mb-4" />
               <h3 className="text-xl font-bold text-brand-brown">Analyzing Profile...</h3>
            </div>
          ) : (
            <div className="space-y-8">
              {questions.map((q) => (
                <div key={q.id} className="pb-6 border-b border-brand-brown/10 last:border-0">
                  <p className="font-bold text-brand-brown mb-4">{q.text}</p>
                  <div className="flex justify-between gap-2">
                    {[1, 2, 3, 4, 5].map((val) => (
                      <button
                        key={val}
                        onClick={() => handleAnswer(q.id, val)}
                        className={`w-10 h-10 rounded-full font-bold border-2 transition-all ${
                          answers[q.id] === val 
                          ? 'bg-brand-green text-white border-brand-green scale-110' 
                          : 'border-brand-brown/20 text-brand-brown/40 hover:border-brand-green'
                        }`}
                      >
                        {val}
                      </button>
                    ))}
                  </div>
                  <div className="flex justify-between text-xs font-bold text-brand-brown/30 mt-2 uppercase">
                    <span>Disagree</span><span>Agree</span>
                  </div>
                </div>
              ))}
              <div className="pt-4 text-right">
                <button
                   onClick={calculateScores}
                   disabled={Object.keys(answers).length < questions.length}
                   className="px-8 py-4 bg-brand-gold hover:bg-brand-green disabled:bg-gray-300 text-white font-bold uppercase tracking-widest text-sm rounded shadow-lg transition-colors"
                >
                   View Results
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
export default App;
