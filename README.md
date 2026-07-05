# 📝 AI Document Summarizer (Text & PDF)

A production-ready, premium web application built using Python/Flask, Vanilla JS, and the Groq API (Llama 3.3). It distills long text and PDF files into clear, concise, bulleted summaries.

The project is structured as a unified application where the Flask backend serves the premium frontend statically, simplifying deployment to a single free service on platforms like Render.

---

## 🌟 Features
* **Premium Glassmorphic Dark UI**: Modern responsive design with smooth micro-animations.
* **Drag-and-Drop Area**: Easily upload `.txt` and `.pdf` files.
* **Markdown Parsing**: Renders bulleted lists, headers, and bold text beautifully using `marked.js`.
* **Copy-to-Clipboard**: Quickly copy the generated report with a single click.
* **Robust Error Handling**: Gracefully handles missing files, malformed PDFs, and API key issues.

---

## 🛠️ Local Development

### 1. Prerequisites
Make sure you have **Python 3.9+** installed.

### 2. Set Up Environment Variables
Create a file named `.env` inside the `backend/` directory:
```env
GROQ_API_KEY=your_actual_groq_api_key
```
*(Get a free key from [console.groq.com](https://console.groq.com/))*

### 3. Install Dependencies
Navigate to the root directory and install requirements:
```bash
pip install -r backend/requirements.txt
```

### 4. Run the Application
Start the Flask development server:
```bash
python backend/app.py
```
Open your browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🚀 Deployment Guide (Render.com)

Render.com is the recommended free hosting platform for this application. It supports Python applications and has a generous free tier.

### Step 1: Initialize Git Repository
If you haven't already, push this project to a GitHub repository:
1. Open terminal at the project root directory.
2. Initialize Git:
   ```bash
   git init
   git add .
   git commit -m "Initial production commit"
   ```
3. Create a new repository on [GitHub](https://github.com/) (e.g., `ai-document-summarizer`).
4. Link and push to GitHub:
   ```bash
   git remote add origin https://github.com/your-username/ai-document-summarizer.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Create a Web Service on Render
1. Sign up/log in to [Render.com](https://render.com/).
2. Click **New** -> **Web Service**.
3. Connect your GitHub repository.
4. Configure the Web Service:
   * **Name**: `ai-document-summarizer` (or any custom name)
   * **Region**: Choose the closest one to you
   * **Branch**: `main`
   * **Root Directory**: Leave it blank (keeps root folder `/`)
   * **Runtime**: `Python 3`
   * **Build Command**: `pip install -r backend/requirements.txt`
   * **Start Command**: `gunicorn --chdir backend app:app`
   * **Instance Type**: `Free`

### Step 3: Configure Environment Variables
1. Scroll down to **Environment Variables** (or go to the **Variables** tab after service creation).
2. Click **Add Environment Variable**:
   * **Key**: `GROQ_API_KEY`
   * **Value**: *Your Groq API key (starts with `gsk_`)*
3. Click **Save Changes** and deploy!

---

## 📂 Project Structure
```text
summarizer/
├── backend/
│   ├── app.py             # Flask backend & static file server
│   ├── requirements.txt   # Python dependencies
│   └── .env               # Local env file (git-ignored in production)
├── frontend/
│   └── index.html         # Premium UI and client logic
├── render.yaml            # Render blueprint config
└── README.md              # Documentation
```
