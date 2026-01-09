// frontend/src/apiService.js

// Relative path works for both Localhost and Cloud Run
const API_URL = "/api"; 

// --- 1. The Function Your Test Button Needs ---
export const submitAnswers = async (answers) => {
    // We wrap the simple answers in the full payload the backend expects
    // We use "Anonymous" so the backend validation passes
    const payload = {
        name: "Test User",
        email: "test@example.com",
        answers: answers
    };

    console.log("Sending payload to backend:", payload);

    const response = await fetch(`${API_URL}/submit`, { // Endpoint likely /submit or /assess
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

    const response = await fetch(`${API_URL}/submit`, {
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
