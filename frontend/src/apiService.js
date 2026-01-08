// UPDATED: This now points to your Google Cloud Run Backend
const API_URL = "https://eibigfive-642930760060.us-east4.run.app"; 

export const submitSurvey = async (name, email, answers) => {
    const payload = {
        name: name,
        email: email,
        answers: answers
    };

    const response = await fetch(`${API_URL}/submit-assessment`, {
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

    const response = await fetch(`${API_URL}/analyze-team`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    return await response.json();
};
