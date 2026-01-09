import React from 'react'
import ReactDOM from 'react-dom/client'
import AssessmentView from './AssessmentView'
// We don't have a CSS file yet, so we skip importing index.css to prevent errors

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AssessmentView />
  </React.StrictMode>,
)
