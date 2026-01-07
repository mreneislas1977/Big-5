import React from 'react';
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

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const BigFiveChart = ({ scores }) => {
 const data = {
   labels: ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Stability'],
   datasets: [
     {
       label: 'Personality Profile',
       data: [scores.OPN, scores.CSN, scores.EXT, scores.AGR, scores.EST],
       backgroundColor: 'rgba(54, 162, 235, 0.2)',
       borderColor: 'rgba(54, 162, 235, 1)',
       borderWidth: 2,
     },
   ],
 };

 const options = {
   scales: {
     r: {
       suggestedMin: 0,
       suggestedMax: 100,
       ticks: { stepSize: 20 }
     },
   },
 };

 return <Radar data={data} options={options} />;
};

export default BigFiveChart;
