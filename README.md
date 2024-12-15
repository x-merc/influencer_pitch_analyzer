
# Project Overview

Stages completed: Algorithm development, Backend development, Frontend development, deployment, provide public access

### 1. Backend

The backend is implemented using Python and is responsible for processing and analyzing user input, as well as interacting with external services like the OpenAI API.

#### Key Features:
- **Language:** Python-based implementation.
- **API Integration:** Utilizes the OpenAI API to perform various tasks, including analyzing the provided script and matching it against predefined criteria.
- **Response Handling:** The response from the OpenAI API is parsed using string manipulation techniques.
- **Data Management:** Custom data classes are employed for improved understanding and better management of data.
- **Reason for Choosing Python:**
  - Native support for OpenAI API integration.
  - Extensive libraries and frameworks available for AI development.
  - Seamless integration with AWS ecosystem.

### 2. Frontend

The frontend is built using HTML and JavaScript, providing a simple and functional interface for users to input their scripts and view the processed responses.

#### Key Features:
- **Language:** HTML and JavaScript-based frontend.
- **Functionality:** Designed to receive a script from the user and display the processed result.
- **Reason for Choosing HTML and JavaScript:**
  - HTML is the foundational technology for building web pages.
  - JavaScript provides the interactivity necessary to enhance user experience.

### 3. Deployment

The deployment architecture is based on AWS services.

#### Backend:
- **AWS Lambda, exposed via Function URL** 
- **Reason for AWS Lambda:**
  - No server management is required.
  - Highly scalable, providing dynamic allocation of RAM and CPU resources.
  - Cost-efficient pay-as-you-go pricing model.
  - Event-driven execution, ensuring resources are used only when triggered.
  - Simplified security management.
- **Reason for Function URL:**
  - Provides a timeout of up to 15 minutes, accommodating the use case's time requirements.
  - Efficient for deploying a single function-based API.

#### Core:
- **Open AI API**
- **Reason for Open AI API:**
  - Provides access to advanced generative models.
  - Pay-as-you-go model with pre-paid credits.
  - Highly scalable and easy integration with Python.
  - Capable of performing complex analysis tasks.

#### Frontend:
- **AWS Amplify with artifacts stored in S3** 
- **Reason for Using AWS Amplify:**
  - Fully managed hosting service that simplifies frontend deployment.
  - Ability to deploy changes rapidly.
  - Access control features when necessary.
  - Pay-as-you-go pricing.
  - Easy integration with other AWS services, such as S3.
- **Reason for Using S3:**
  - Ideal for storing large files within the AWS ecosystem.
  - Simple integration with AWS Amplify.
  - Provides versioning, useful for managing different iterations of files.

---

## Future Enhancements

### 1. Core Improvements:
- **Prompt Engineering:** Enhancing prompts to improve responses from generative models, as the quality of results often depends on how the questions are posed.
- **Model Optimization:** Evaluating different models to determine the best fit for the specific tasks, and tuning them for optimal performance.
- **Data Analysis and Filtering:** Employing data analysis techniques to refine the input context for the models.
- **Video Support:** Extending functionality to support video processing, including audio extraction (using `ffmpeg`), cleanup and preprocessing (using `pydub`, `noisereduce`, `librosa`), and transcription (using `openai-whisper`).
- **Algorithm Refinement:** In its current form it works for a specific client (Milanote), it needs to be developed separately for each client or a more generic one based on client needs common across multiple clients.

### 2. Deployment Improvements:
- **Serverless to Server-Based Transition:** Given AWS Lambda's 15-minute timeout limitation, a transition to a server-based model may be required for handling longer requests.
- **Handling Larger Payloads:** For large data uploads (e.g., video files), a new response mechanism may be needed, such as asynchronous requests with polling at repeated intervals. Implementing presigned URLs for direct file uploads to handle large payloads could be used effectively.

### 3. Backend and Frontend Enhancements:
- **Backend:** Support for processing additional formats and exposing multiple endpoints to improve flexibility.
- **Security:** Implementing security layer to data and user security.
- **Logging and Monitoring:** Setting up comprehensive logging and log management to improve system diagnostics and collect data for improvements.
- **Scalability and High Availability:** Ensuring the backend can scale efficiently and remain available during high load periods.
- **Frontend:** Improving the frontend for better user engagement, appeal, and overall user experience.

---

## Demo Links

1. **Frontend-based Demo:**
   [Frontend Demo](https://staging.d3ugxlxbskzqd7.amplifyapp.com/)

2. **Direct API Call Demo:**
   ```bash
   curl --location 'https://v5uxu6kjxlxnijvgofgqowvrve0yuegm.lambda-url.ap-south-1.on.aws/'    --header 'Content-Type: application/json'    --data '{
       "content": "Milanote is a powerful online platform for organizing creative projects. It'''s used for brainstorming, planning, and collaborating on visual boards. You can work with teams to organize thoughts, share ideas, and create an organized workspace.",
       "creator_name": "User"
   }'
   ```