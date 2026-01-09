// frontend/src/apiService.js

// Relative path works for both Localhost and Cloud Run
const API_URL = "/api"; 

// --- 1. The Function Your Test Button Needs ---
export const submitAnswers = async (answers) => {
    const payload = {
        name: "Test User",
        email: "test@example.com",
        answers: answers
    };

    console.log("Sending payload to backend:", payload);

    // FIX: Changed from '/submit' to '/assess' to match main.py
    const response = await fetch(`${API_URL}/assess`, { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error("Server Error:", errorText);
        throw new Error(`Submission Failed: ${response.status}`);
    }
    
    return await response.json();
};

// --- 2. The Future Function for the Real Survey ---
export const submitSurvey = async (name, email, answers) => {
    const payload = {
        name: name,
        email: email,
        answers: answers
    };

    // FIX: Changed from '/submit' to '/assess' to match main.py
    const response = await fetch(`${API_URL}/assess`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error("Submission Failed");
    return await response.json();
};

export const createTeam = async (teamName, userIds) => {
    const payload = {
        team_name: teamName,
        member_doc_ids: userIds
    };

    const response = await fetch(`${API_URL}/team`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    return await response.json();
};
