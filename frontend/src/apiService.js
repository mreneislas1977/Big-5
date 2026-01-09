// frontend/src/apiService.js

// Relative path works for both Localhost and Cloud Run
const API_URL = "/api"; 

export const submitAnswers = async (answers) => {
    // We automatically add "Test User" so the backend accepts the data
    const payload = {
        name: "Test User",
        email: "test@example.com",
        answers: answers
    };

    console.log("Sending payload to backend:", payload);

    // FIX: This now correctly points to "/assess"
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

export const submitSurvey = async (name, email, answers) => {
    const payload = {
        name: name,
        email: email,
        answers: answers
    };

    // FIX: This also points to "/assess"
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
