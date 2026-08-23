async function analyzeCode() {

    const code = document.getElementById("codeInput").value;

    const result = document.getElementById("result");


    if (code.trim() === "") {

        result.textContent =
            "Please paste some Python code first.";

        return;
    }


    result.textContent = "🔄 Analyzing your code...";


    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                code: code
            })

        });


        const data = await response.json();


        if (data.success) {

            result.innerHTML = `

                <h3>🤖 AI Code Analysis</h3>

                <br>

                <strong>⚠️ Error Type</strong>

                <p>
                    ${data.error_type}
                </p>

                <br>

                <strong>📊 Confidence</strong>

                <p>
                    ${data.confidence}%
                </p>

                <br>

                <strong>💡 Explanation</strong>

                <p>
                    ${data.explanation}
                </p>

                <br>

                <strong>🛠️ Suggested Fix</strong>

                <p>
                    ${data.fix}
                </p>

            `;

        } else {

            result.innerHTML = `

                <strong>❌ ${data.status}</strong>

                <br><br>

                <strong>Error Type:</strong>
                ${data.error_type}

                <br><br>

                <strong>Explanation:</strong>
                ${data.explanation}

                <br><br>

                <strong>Line:</strong>
                ${data.line || "Unknown"}

            `;

        }


    } catch (error) {

        result.textContent =
            "Something went wrong while connecting to the server.";

        console.error(error);

    }
}
async function searchGitHub() {

    const username =
        document.getElementById("githubUsername").value.trim();

    const result =
        document.getElementById("githubResult");


    if (username === "") {

        result.innerHTML =
            "<p>Please enter a GitHub username.</p>";

        return;
    }


    result.innerHTML =
        "<p>🔄 Loading GitHub profile...</p>";


    try {

        const response =
            await fetch(`/github/${username}`);


        const data =
            await response.json();


        if (!data.success) {

            result.innerHTML = `
                <p>❌ ${data.message}</p>
            `;

            return;
        }


        let repositoriesHTML = "";


        if (data.repo_list.length === 0) {

            repositoriesHTML =
                "<p>No public repositories found.</p>";

        } else {

            data.repo_list.forEach(repo => {

                repositoriesHTML += `

                    <div class="repo-card">

                        <h4>
                            ${repo.name}
                        </h4>

                        <p>
                            ${repo.description ||
                            "No description available."}
                        </p>

                        <div class="repo-info">

                            <span>
                                💻
                                ${repo.language ||
                                "Not specified"}
                            </span>

                            <span>
                                ⭐
                                ${repo.stars}
                            </span>

                            <span>
                                🍴
                                ${repo.forks}
                            </span>

                        </div>

                        <a
                            href="${repo.url}"
                            target="_blank"
                        >
                            View Repository →
                        </a>

                    </div>

                `;

            });

        }


        result.innerHTML = `

            <div class="github-profile">

                <img
                    src="${data.avatar}"
                    alt="GitHub profile"
                    class="github-avatar"
                >

                <div>

                    <h3>
                        ${data.name || data.username}
                    </h3>

                    <p>
                        @${data.username}
                    </p>

                </div>

            </div>


            <p>
                ${data.bio || "No bio available."}
            </p>


            <div class="github-stats">

                <div>

                    <strong>
                        ${data.repositories}
                    </strong>

                    <span>
                        Repositories
                    </span>

                </div>


                <div>

                    <strong>
                        ${data.followers}
                    </strong>

                    <span>
                        Followers
                    </span>

                </div>


                <div>

                    <strong>
                        ${data.following}
                    </strong>

                    <span>
                        Following
                    </span>

                </div>

            </div>


            <h3>
                📦 Recent Repositories
            </h3>

            <br>

            ${repositoriesHTML}

            <br>

            <a
                href="${data.profile_url}"
                target="_blank"
                class="primary-btn"
            >
                View GitHub Profile →
            </a>

        `;


    } catch (error) {

        result.innerHTML =
            "<p>❌ Could not connect to GitHub.</p>";

        console.error(error);

    }
}
async function loadVCSData() {

    const branch =
        document.getElementById("vcsBranch");

    const commits =
        document.getElementById("vcsCommits");

    const files =
        document.getElementById("vcsFiles");

    const status =
        document.getElementById("vcsStatus");

    const commitList =
        document.getElementById("commitList");


    try {

        const response =
            await fetch("/vcs");


        const data =
            await response.json();


        branch.textContent =
            data.branch || "Unknown";

        commits.textContent =
            data.commits;

        files.textContent =
            data.files;

        status.textContent =
            data.status;


        if (data.recent_commits.length === 0) {

            commitList.innerHTML =
                "<p>No commits found.</p>";

            return;
        }


        commitList.innerHTML =
            data.recent_commits.map(commit => `

                <div class="commit-item">

                    <span class="commit-hash">
                        ${commit.hash}
                    </span>

                    <span class="commit-message">
                        ${commit.message}
                    </span>

                    <span class="commit-author">
                        ${commit.author}
                    </span>

                </div>

            `).join("");


    } catch (error) {

        console.error(error);

        commitList.innerHTML =
            "<p>❌ Unable to load Git information.</p>";

    }
}


document.addEventListener(
    "DOMContentLoaded",
    loadVCSData
);