# SignCare MVP

SignCare is an assistive technology platform designed to bridge communication gaps between doctors and deaf/HOH patients using **Rwanda Sign Language recognition, speech-to-text transcription, and sign language avatar rendering**.  

This repository contains the **Flask-based MVP** with authentication, hospital-specific deployments, and scalable backend design.

---

## Features
- 🔐 User authentication (JWT-based, HIPAA/GDPR ready)
- 🏥 Multi-hospital deployment architecture
- 🖥️ Dual-screen consultation support (doctor & patient views)
- 🎤 Offline speech-to-text with [Vosk](https://alphacephei.com/vosk/)
- ✋ Real-time gesture recognition using MediaPipe
- 🤖 Translation with fine-tuned lightweight LLM (Rwanda Sign Language + medical vocabulary)
- 🗄️ PostgreSQL database (SQLite supported for local dev)
- 🐳 Dockerized deployment (NGINX reverse proxy)

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/signcare.git
cd signcare

python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt

cp .env.example .env

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=supersecretkey

# Database: use SQLite for dev or PostgreSQL for production
SQLALCHEMY_DATABASE_URI=sqlite:///signcare.db
# Example for PostgreSQL:
# SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/signcare

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

flask run

docker-compose up --build

signcare/
│── app/               # Application code
│   ├── auth/          # Authentication blueprint
│   ├── hospital/      # Hospital-specific features
│   ├── static/        # CSS, JS, images
│   ├── templates/     # HTML templates
│   ├── models.py      # Database models
│   ├── routes.py      # Route definitions
│   └── __init__.py    # App factory
│
│── migrations/        # Database migrations
│── requirements.txt   # Python dependencies
│── run.py             # Flask entry point
│── Dockerfile         # Docker configuration
│── docker-compose.yml # Multi-container setup
│── .env.example       # Example environment variables
│── README.md          # Documentation


Contribution

Fork the repo 🍴

Create a feature branch (git checkout -b feature/awesome)

Commit your changes (git commit -m "Add awesome feature")

Push to branch (git push origin feature/awesome)

Create a Pull Request

License

📜 MIT License – see LICENSE
 file for details.

Maintainer

👨‍💻 Developed by Nasiru I. Liya
🌍 Rwanda | 💡 CMU Africa | ❤️ Building AI for accessibility