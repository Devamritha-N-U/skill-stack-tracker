# Skill Stack Tracker 🚀

A personal application built to help developers and learners track their progress on courses, tutorials, and certifications. The application uses a Python FastAPI backend for the API and data storage, and a ReactJS frontend for the user interface and visualization.

## Features ✨

The Skill Stack Tracker implements the core requirements for tracking personal skill growth:

* **Goal Creation:** Allows users to add new learning goals by specifying the skill name, resource type (video, course, article), and platform (Udemy, YouTube, Coursera, etc.).
* **Progress Tracking:** Goals can be tracked with statuses such as `started`, `in-progress`, or `completed`.
* **Metric Logging:** Users can log hours spent on a goal and set a difficulty rating (1-10).
* **Analytics Dashboard:** A dashboard provides comprehensive skill growth insights, including key metrics (Total Goals, Hours Tracked) and a category-wise breakdown (e.g., Goals by Resource Type) using charts.
* **Clean UI/UX:** Utilizes modern React structure and Bootstrap for a clean, responsive interface.

## Setup Steps 🛠️

To get the application running locally, you must set up both the **Backend API** (Python/FastAPI) and the **Frontend** (ReactJS).

### Prerequisites

* Python (3.9+)
* Node.js (LTS recommended)
* Git

1. Clone repository: git clone https://github.com/Devamritha-N-U/skill-stack-tracker.git
cd skill-stack-tracker

2. Backend Setup (FastAPI)
The backend code is assumed to be in a directory like backend/.

Navigate to the backend directory and set up the virtual environment:

cd backend
python -m venv .venv
.venv\Scripts\activate    

Install uvicorn before using pip
uvicorn backend.main:app --reload
The API should now be running locally at http://127.0.0.1:8000/. Keep this terminal running.

3. Frontend Setup (ReactJS)

The frontend code is in the main project directory.

Open a new terminal window (or tab) and navigate back to the root directory (skill-stack-tracker).

Install dependencies: npm install

run:npm start

The application will automatically open in your browser at http://localhost:3000. You can now interact with the Skill Stack Tracker!
