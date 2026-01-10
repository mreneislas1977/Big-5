import React, { useState, useEffect } from 'react';
import { submitSurvey } from './apiService';
import BigFiveChart from './BigFiveChart';

const AssessmentView = () => {
   const [status, setStatus] = useState("loading_questions");
   const [questions, setQuestions] = useState([]);
   const [answers, setAnswers] = useState({});
   const [report, setReport] = useState(null);
   const [userData, setUserData] = useState({ name: "", email: "" });

   // 1. Fetch Questions on Load
   useEffect(() => {
     fetch('/api/questions')
       .then(res => res.json())
       .then(data => {
         if (Array.isArray(data)) {
           // Flatten the categories into a single list of questions
           const flatList = data.flatMap(cat => cat.questions);
           setQuestions(flatList);
           setStatus("idle");
         } else {
           console.error("Invalid question format", data);
           setStatus("error");
         }
       })
       .catch(err => {
         console.error(err);
         setStatus("error");
       });
   }, []);

   // 2. Handle Inputs
   const handleAnswerChange = (qId, value) => {
     setAnswers(prev => ({ ...prev, [qId]: parseInt(value) }));
   };

   const handleSubmit = async (e) => {
     e.preventDefault();
     setStatus("processing");
     try {
         const result = await submitSurvey(userData.name, userData.email, answers);
         setReport(result.report);
         setStatus("done");
     } catch (error) {
         console.error(error);
         setStatus("error");
     }
   };

   // 3. Render: Report View
   if (status === "done" && report) {
       return (
           <div style={{ padding: 40, maxWidth: 800, margin: '0 auto', fontFamily: 'sans-serif' }}>
               <h1 style={{color: '#333'}}>Archetype: {report.archetype}</h1>
               <p style={{fontSize: '1.2rem', lineHeight: '1.6'}}>{report.description}</p>
               
               <div style={{ maxWidth: 500, margin: '40px auto' }}>
                   <BigFiveChart scores={report.scores} />
               </div>
               
               <div style={{backgroundColor: '#f0f9ff', padding: 20, borderRadius: 8}}>
                 <h3>🚀 Growth Tip:</h3>
                 <p style={{ color: "#0066cc", fontWeight: 'bold' }}>{report.recommendation}</p>
               </div>
               
               <button onClick={() => window.location.reload()} style={{marginTop: 30, padding: '10px 20px'}}>
                 Take Test Again
               </button>
           </div>
       );
   }

   // 4. Render: Loading / Error
   if (status === "loading_questions") return <div style={{padding:20}}>Loading Assessment...</div>;
   if (status === "error") return <div style={{padding:20, color: 'red'}}>Error loading system. Please refresh.</div>;

   // 5. Render: Questionnaire Form
   return (
       <div style={{ padding: 40, maxWidth: 700, margin: '0 auto', fontFamily: 'sans-serif' }}>
           <h1>Big Five Assessment</h1>
           <p style={{marginBottom: 30}}>Rate yourself from 1 (Disagree) to 5 (Agree).</p>
           
           <form onSubmit={handleSubmit}>
             <div style={{marginBottom: 20, display: 'flex', gap: 10}}>
               <input 
                 type="text" 
                 placeholder="Your Name" 
                 required 
                 style={{padding: 8, flex: 1}}
                 onChange={e => setUserData({...userData, name: e.target.value})}
               />
               <input 
                 type="email" 
                 placeholder="Your Email" 
                 required 
                 style={{padding: 8, flex: 1}}
                 onChange={e => setUserData({...userData, email: e.target.value})}
               />
             </div>

             {questions.map((q) => (
               <div key={q.id} style={{ marginBottom: 15, padding: 15, backgroundColor: '#f9f9f9', borderRadius: 5 }}>
                 <p style={{margin: '0 0 10px 0', fontWeight: 500}}>{q.text}</p>
                 <div style={{ display: 'flex', justifyContent: 'space-between', maxWidth: 300 }}>
                   {[1, 2, 3, 4, 5].map(val => (
                     <label key={val} style={{cursor: 'pointer'}}>
                       <input 
                         type="radio" 
                         name={q.id} 
                         value={val} 
                         required
                         onChange={() => handleAnswerChange(q.id, val)}
                       />
                       <br/><span style={{fontSize: 12, color: '#666'}}>{val}</span>
                     </label>
                   ))}
                 </div>
               </div>
             ))}

             <button 
               type="submit" 
               disabled={status === "processing"}
               style={{
                 padding: '15px 30px', 
                 fontSize: 18, 
                 backgroundColor: '#007bff', 
                 color: 'white', 
                 border: 'none', 
                 borderRadius: 5, 
                 cursor: 'pointer',
                 marginTop: 20
               }}
             >
               {status === "processing" ? "Analyzing Profile..." : "Submit Assessment"}
             </button>
           </form>
       </div>
   );
};

export default AssessmentView;
