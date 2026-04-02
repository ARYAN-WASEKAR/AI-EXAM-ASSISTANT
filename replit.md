# AI Exam Assistant

A web application that helps students prepare for exams by providing structured, comprehensive answers to any exam question using Google's Gemini AI.

## Features

- Simple Explanation of the topic
- Bullet Points summary
- 2-Mark Answer (concise)
- 5-Mark Answer (detailed)
- Keywords for the topic
- Hindi Translation of the explanation

## Tech Stack

- **Backend**: Python + Flask
- **AI**: Google Gemini 1.5 Flash (`google-generativeai`)
- **Frontend**: Vanilla HTML/CSS/JavaScript

## Project Structure

```
main.py              # Flask server + Gemini API integration
templates/index.html # Frontend UI
static/style.css     # Styles
```

## Environment Variables

- `GEMINI_API_KEY` — Google Gemini API key (stored as a secret)

## Running

The app runs on port 5000 via the "Start application" workflow:
```
python main.py
```
