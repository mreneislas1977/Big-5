// UPDATED: Use relative paths. 
// This works automatically on localhost:8000 AND your Cloud Run URL.
const API_URL = "/api"; 

export const submitSurvey = async (name, email, answers) => {
    const payload = {
        name: name,
        email: email,
        answers: answers
    };

    // Changed endpoint from '/submit-assessment' to '/assess' to match REST standards
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

    // Changed endpoint from '/analyze-team' to '/team'
    const response = await fetch(`${API_URL}/team`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    return await response.json();
};
