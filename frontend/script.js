async function analyzeResume() {
    const resume = document.getElementById("resume").files[0];
    const jobDescription = document.getElementById("jobDescription").value;
    const resultDiv = document.getElementById("result");

    if (!resume || !jobDescription) {
        resultDiv.innerHTML = "<div class='card'>Please upload resume and paste job description.</div>";
        return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    resultDiv.innerHTML = "<div class='card'>Analyzing your resume...</div>";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        resultDiv.innerHTML = `
            <div class="card">
                <h2>Resume Match Score</h2>
                <p class="score">${data.match_score}%</p>
            </div>

            <div class="card">
                <h2>Resume Strength Level</h2>
                <p class="strength">${data.resume_strength}</p>
            </div>

            <div class="card">
                <h3>Found Skills</h3>
                ${
                    data.found_skills.length
                    ? data.found_skills.map(skill => `<span class="skill-tag">${skill}</span>`).join("")
                    : "No skills found"
                }
            </div>

            <div class="card">
                <h3>Missing Skills</h3>
                ${
                    data.missing_skills.length
                    ? data.missing_skills.map(skill => `<span class="missing-tag">${skill}</span>`).join("")
                    : "No missing skills"
                }
            </div>

            <div class="card">
                <h3>ATS Section Check</h3>
                <ul>
                    ${Object.entries(data.ats_sections).map(([section, status]) =>
                        `<li>${section}: ${status ? "✅ Present" : "❌ Missing"}</li>`
                    ).join("")}
                </ul>
            </div>

            <div class="card">
                <h3>Career Tips</h3>
                <ul>
                    ${data.career_tips.map(tip => `<li>${tip}</li>`).join("")}
                </ul>
            </div>

            <div class="card">
                <h3>Project Suggestions</h3>
                <ul>
                    ${data.project_suggestions.map(project => `<li>${project}</li>`).join("")}
                </ul>
            </div>

            <div class="card">
                <h3>Interview Questions</h3>
                <ul>
                    ${data.interview_questions.map(question => `<li>${question}</li>`).join("")}
                </ul>
            </div>
        `;

    } catch (error) {
        resultDiv.innerHTML = "<div class='card'>Backend not running or API error.</div>";
    }
}