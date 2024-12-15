const scriptInput = document.getElementById('scriptInput');
const creatorInput = document.getElementById('creatorName');
const analyzeButton = document.getElementById('analyzeButton');
const analysisResult = document.getElementById('analysisResult');

// Create a loading spinner element
const loadingSpinner = document.createElement('div');
loadingSpinner.innerHTML = `
    <style>
        .loading-spinner {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .loading-text {
            margin-left: 15px;
            color: #333;
        }
    </style>
    <div class="loading-spinner">
        <div class="spinner"></div>
        <div class="loading-text">Analyzing script... </div>
    </div>
`;

analyzeButton.addEventListener('click', () => {
    // Disable the button to prevent multiple submissions
    analyzeButton.disabled = true;

    // Clear previous results
    analysisResult.innerHTML = '';

    // Show loading spinner
    analysisResult.appendChild(loadingSpinner);

    const scriptText = scriptInput.value;
    const creatorName = creatorInput.value;

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
        content: scriptText,
        creator_name: creatorName
    });

    const requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("https://v5uxu6kjxlxnijvgofgqowvrve0yuegm.lambda-url.ap-south-1.on.aws/", requestOptions)
        .then(response => {
            data = response.json()
            if (data.status == "BAD REQUEST" || data.status == "SERVER_ERROR")
            {
                throw data;
            }
            return data;
        })
        .then(data => {
            // Remove loading spinner
            analysisResult.innerHTML = '';

            // Create a container for all feedback sections
            const feedbackContainer = document.createElement('div');

            // Process different sections of the feedback
            const sections = [
                { name: 'Script Flow', key: 'script flow' },
                { name: 'Core Requirements', key: 'core requirements' },
                { name: 'Avoided Elements', key: 'avoided elements' },
                { name: 'Brand Safety', key: 'brand safety' }
            ];

            sections.forEach(section => {
                if (data.details[section.key]) {
                    const sectionTitle = document.createElement('h3');
                    sectionTitle.textContent = section.name;
                    feedbackContainer.appendChild(sectionTitle);

                    const sectionList = document.createElement('ul');
                    data.details[section.key].forEach(item => {
                        const feedbackItem = document.createElement('li');
                        feedbackItem.innerHTML = `
            <strong>Criteria:</strong> ${item.criteria}<br>
            <strong>Feedback:</strong> ${item.feedback || 'No specific feedback'}<br>
            <strong>Passed:</strong> ${item.passed ? 'Yes' : 'No'}
          `;
                        sectionList.appendChild(feedbackItem);
                    });

                    feedbackContainer.appendChild(sectionList);
                }
            });

            // Add overall message and status
            const overallMessage = document.createElement('div');
            overallMessage.innerHTML = `
      <h3>Overall Result</h3>
      <p><strong>Message:</strong> ${data.message}</p>
      <p><strong>Status:</strong> ${data.status}</p>
    `;
            feedbackContainer.appendChild(overallMessage);

            // Add feedback to analysis result
            analysisResult.appendChild(feedbackContainer);
        })
        .catch(error => {
            console.log('Error:', error);
            analysisResult.innerHTML = `
      <div style="color: red;">
        <h3>Error</h3>
        <p>An error occurred. Please try again later.</p>
      </div>
    `;
        })
        .finally(() => {
            // Re-enable the button
            analyzeButton.disabled = false;
        });
});