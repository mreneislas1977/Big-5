import React, { useState, useEffect } from 'react';
import { submitSurvey } from './apiService';
import BigFiveChart from './BigFiveChart';

const AssessmentView = () => {
   // --- STATE MANAGEMENT ---
   const [status, setStatus] = useState("loading_questions");
   const [questions, setQuestions] = useState([]);
   const [answers, setAnswers] = useState({});
   const [report, setReport] = useState(null);
   const [userData, setUserData] = useState({ name: "", email: "" });

   // --- 1. FETCH QUESTIONS ON LOAD ---
   useEffect(() => {
     fetch('/api/questions')
       .then(res => res.json())
       .then(data => {
         if (Array.isArray(data)) {
           // Flatten the categories to get a simple list of questions
           const flatList = data.flatMap(cat => cat.questions);
           setQuestions(flatList);
           setStatus("idle");
         } else {
           setStatus("error");
         }
       })
       .catch(() => setStatus("error"));
   }, []);

   // --- 2. HANDLE INPUTS ---
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
         console.error("Submission failed:", error);
         setStatus("error");
     }
   };

   // --- 3. SUB-COMPONENT: HEADER ---
   const PortalHeader = () => (
     <div className="portal-header">
       <div className="portal-logo">CRESCERE <span>STRATEGY</span></div>
     </div>
   );

   // --- VIEW: RESULTS (DASHBOARD) ---
   if (status === "done" && report) {
       return (
           <>
             <PortalHeader />
             <div className="container">
               <div className="card">
                   <h1>{report.archetype}</h1>
                   <p className="subtitle">{report.description}</p>
                   
                   {/* CHART SECTION */}
                   <div style={{ maxWidth: 500, margin: '40px auto' }}>
                       <BigFiveChart scores={report.scores} />
                   </div>
                   
                   {/* RECOMMENDATION BOX */}
                   <div style={{
                       background: '#F9FAFB', 
                       padding: '30px', 
                       borderRadius: '8px', 
                       textAlign: 'left',
                       borderLeft: '5px solid #800020' /* Burgundy Accent */
                   }}>
                     <h3 style={{ margin: '0 0 10px 0', color: '#014421' }}>Executive Recommendation</h3>
                     <p style={{ margin: 0, color: '#5c4033', lineHeight: '1.6' }}>
                        {report.recommendation}
                     </p>
                   </div>
                   
                   {/* RESTART BUTTON */}
                   <button 
                     onClick={() => window.location.reload()}
                     style={{
                       marginTop: 30, 
                       background: 'transparent', 
                       border: '2px solid #014421', 
                       color: '#014421',
                       padding: '12px 24px',
                       borderRadius: '6px',
                       cursor: 'pointer',
                       fontWeight: '600',
                       fontSize: '1rem'
                     }}
                   >
                     Restart Assessment
                   </button>
               </div>
             </div>
           </>
       );
   }

   // --- VIEW: LOADING / ERROR ---
   if (status === "loading_questions") return <div style={{padding:40, textAlign:'center', color:'#014421'}}>Loading Portal...</div>;
   if (status === "error") return <div style={{padding:40, textAlign:'center', color:'#800020'}}>System Error. Please check your connection and refresh.</div>;

   // --- VIEW: INTAKE FORM ---
   return (
       <>
         <PortalHeader />
         <div className="container">
           <div className="card">
               <h1>Executive Insights Assessment</h1>
               <p className="subtitle">
                 Discover your leadership archetype and how your personality traits shape your strategic decision-making.
               </p>
               
               <form onSubmit={handleSubmit}>
                 {/* USER DETAILS */}
                 <div className="form-grid">
                   <div>
                     <label style={{display:'block', marginBottom:8, fontWeight:600, fontSize:14}}>Full Name</label>
                     <input 
                       type="text" 
                       placeholder="e.g. Jane Doe" 
                       required 
                       onChange={e => setUserData({...userData, name: e.target.value})}
                     />
                   </div>
                   <div>
                     <label style={{display:'block', marginBottom:8, fontWeight:600, fontSize:14}}>Work Email</label>
                     <input 
                       type="email" 
                       placeholder="e.g. jane@company.com" 
                       required 
                       onChange={e => setUserData({...userData, email: e.target.value})}
                     />
                   </div>
                 </div>

                 <div style={{textAlign:'left', marginBottom:20, borderBottom:'2px solid #eee', paddingBottom:10}}>
                    <strong style={{fontSize:14, color:'#014421'}}>INSTRUCTIONS:</strong>
                    <span style={{fontSize:14, color:'#5c4033', marginLeft:8}}>
                        Rate how well each statement describes you (1 = Disagree, 5 = Agree).
                    </span>
                 </div>

                 {/* QUESTIONS LOOP */}
                 {questions.map((q) => (
                   <div key={q.id} className="question-row">
                     <span className="question-text">{q.text}</span>
                     <div className="scale-options">
                       {[1, 2, 3, 4, 5].map(val => (
                         <label key={val} className="radio-circle">
                           <input 
                             type="radio" 
                             name={q.id} 
                             value={val} 
                             required
                             onChange={() => handleAnswerChange(q.id, val)}
                           />
                           <span>{val}</span>
                         </label>
                       ))}
                     </div>
                   </div>
                 ))}

                 {/* SUBMIT BUTTON */}
                 <button type="submit" className="btn-submit" disabled={status === "processing"}>
                   {status === "processing" ? "Analyzing Profile..." : "Generate Executive Report"}
                 </button>
               </form>
           </div>
         </div>
       </>
   );
};

export default AssessmentView;
