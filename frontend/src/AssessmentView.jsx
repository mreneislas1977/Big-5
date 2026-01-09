import React, { useState } from 'react';
import { submitSurvey } from './apiService';
import BigFiveChart from './BigFiveChart';

const AssessmentView = () => {
   const [status, setStatus] = useState("idle");
   const [report, setReport] = useState(null);

   const dummyAnswers = {
       "EXT_1": 5, "EXT_2": 1, "EXT_3": 5, "EXT_4": 1, "EXT_5": 5,
       "AGR_1": 5, "AGR_2": 1, "AGR_3": 5, "AGR_4": 1, "AGR_5": 5,
       "CSN_1": 5, "CSN_2": 1, "CSN_3": 5, "CSN_4": 1, "CSN_5": 5,
       "EST_1": 5, "EST_2": 1, "EST_3": 5, "EST_4": 1, "EST_5": 5,
       "OPN_1": 5, "OPN_2": 1, "OPN_3": 5, "OPN_4": 1, "OPN_5": 5,
   };

   const handleSubmit = async () => {
       setStatus("loading");
       try {
           const result = await submitSurvey("John Doe", "john@example.com", dummyAnswers);
           setReport(result.report);
           setStatus("done");
       } catch (error) {
           console.error(error);
           setStatus("error");
       }
   };

   if (status === "done" && report) {
       return (
           <div style={{ padding: 20 }}>
               <h1>Archetype: {report.archetype}</h1>
               <p>{report.description}</p>
               <div style={{ maxWidth: 500 }}>
                   <BigFiveChart scores={report.scores} />
               </div>
               <h3>Growth Tip:</h3>
               <p style={{ color: "green" }}>{report.recommendation}</p>
           </div>
       );
   }

   return (
       <div style={{ padding: 20 }}>
           <h1>Big Five Assessment</h1>
           <p>Click below to simulate submission.</p>
           <button onClick={handleSubmit} disabled={status === "loading"}>
               {status === "loading" ? "Processing..." : "Submit Answers"}
           </button>
       </div>
   );
};

export default AssessmentView;
