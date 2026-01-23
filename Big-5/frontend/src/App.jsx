import { useState, useEffect } from 'react'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

export default function App() {
  const [questionsData, setQuestionsData] = useState([]);
  const [formData, setFormData] = useState({ name: '', email: '' });
  const [answers, setAnswers] = useState({});
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // 1. Fetch Questions on Load
  useEffect(() => {
    fetch('/api/questions')
      .then(res => res.json())
      .then(data => setQuestionsData(data))
      .catch(err => setError('Failed to load questions.'));
  }, []);

  // 2. Handle Input Changes
  const handleAnswerChange = (qId, value) => {
    setAnswers(prev => ({ ...prev, [qId]: parseInt(value) }));
  };

  // 3. Submit to Python Backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const payload = {
        name: formData.name,
        email: formData.email,
        answers: answers
      };

      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Submission failed');
      
      const data = await res.json();
      setReport(data.report);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 4. Render Results View
  if (report) {
    const chartData = {
      labels: Object.keys(report.scores),
      datasets: [
        {
          label: 'Your Profile',
          data: Object.values(report.scores),
          backgroundColor: 'rgba(1, 68, 33, 0.2)', // brand-green
          borderColor: '#014421',
          borderWidth: 1,
        },
      ],
    };

    return (
      <div className="max-w-2xl mx-auto p-8 bg-white shadow-xl rounded-lg my-10 border-t-4 border-brand-green">
        <h1 className="text-3xl font-bold text-center mb-2 text-brand-green">{report.archetype}</h1>
        <p className="text-center text-gray-600 mb-8 italic">{report.description}</p>
        
        <div className="h-64 mb-8 flex justify-center">
           <div className="w-64">
             <Radar data={chartData} options={{ scales: { r: { min: 0, max: 100 } } }} />
           </div>
        </div>

        <div className="bg-brand-cream p-6 rounded-lg border border-brand-brown">
          <h3 className="font-bold text-brand-brown mb-2">💡 Happiness Tip</h3>
          <p>{report.recommendation}</p>
        </div>

        <button 
          onClick={() => window.location.reload()}
          className="mt-6 w-full py-2 bg-brand-green text-white rounded hover:opacity-90 transition"
        >
          Take Assessment Again
        </button>
      </div>
    );
  }

  // 5. Render Survey Form
  return (
    <div className="min-h-screen p-4">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-xl shadow-lg">
        <header className="mb-8 border-b pb-4">
          <h1 className="text-2xl font-bold text-brand-green">Executive Assessment</h1>
          <p className="text-gray-500">Discover your leadership archetype.</p>
        </header>

        {error && <div className="bg-red-100 text-red-700 p-3 mb-4 rounded">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input 
              required
              placeholder="Full Name"
              className="p-2 border rounded"
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
            <input 
              required
              type="email"
              placeholder="Email Address"
              className="p-2 border rounded"
              value={formData.email}
              onChange={e => setFormData({...formData, email: e.target.value})}
            />
          </div>

          {questionsData.map((category, idx) => (
            <div key={idx} className="bg-gray-50 p-4 rounded-lg">
              <h2 className="font-bold text-lg mb-4 text-brand-brown">{category.category}</h2>
              <div className="space-y-4">
                {category.questions.map(q => (
                  <div key={q.id} className="flex flex-col sm:flex-row sm:items-center justify-between border-b pb-2">
                    <label className="text-sm mb-2 sm:mb-0 w-2/3">{q.text}</label>
                    <div className="flex space-x-2">
                      {[1, 2, 3, 4, 5].map(val => (
                        <label key={val} className="flex flex-col items-center cursor-pointer">
                          <input 
                            required
                            type="radio" 
                            name={q.id} 
                            value={val}
                            onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                            className="accent-brand-green"
                          />
                          <span className="text-xs text-gray-400 mt-1">{val}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-brand-green text-white py-3 rounded-lg font-bold text-lg hover:bg-opacity-90 transition disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Generate Report'}
          </button>
        </form>
      </div>
    </div>
  )
}
