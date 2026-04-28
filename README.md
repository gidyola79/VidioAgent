# VidioAgent
‎### AI Customer Relations Video Agent for Small Businesses
‎
This repository contains a FastAPI backend, Celery worker, and a Next.js frontend.

‎VidioAgent is an AI-powered customer relations assistant that helps small and local businesses create **personalized video messages** for customer engagement using simple text inputs and a short reference video.
‎VidioAgent is an AI-powered service that receives WhatsApp messages for registered businesses, generates a personalized spoken response and lip-synced video, and sends it back to the customer.

‎It automates communication, improves response time, and enables businesses to build stronger relationships with customers across platforms like WhatsApp and Instagram.
‎
‎---
‎
‎## 🚀 Problem
‎
‎Small and medium-sized businesses rely heavily on messaging platforms to communicate with customers, but they face:
‎
‎- Slow or delayed responses to customer inquiries  
‎- Inconsistent promotions and engagement  
‎- Lack of skills/tools to create video content  
‎- Limited time to manage customer relationships  
‎
‎This results in **lost sales, weak engagement, and poor customer retention**.
‎
‎---
‎
‎## 💡 Solution
‎
‎VidioAgent acts as an **AI Customer Relations Agent** that:
‎
‎- Converts text into personalized video messages  
‎- Responds to customer queries automatically  
‎- Generates promotional and announcement videos  
‎- Maintains consistent communication  
‎- Works across messaging and social platforms  
‎
‎---
‎
‎## 🤖 Key Features
‎
‎- 🎬 **Text-to-Video Generation**  
‎  Turn simple text into engaging video messages
‎
‎- 🧑‍💼 **Owner Video Personalization**  
‎  Use a short reference video to generate videos in the business owner's voice/style
‎
‎- 💬 **Automated Customer Replies**  
‎  AI-generated video responses to customer questions
‎
‎- 📱 **Multi-Platform Sharing**  
‎  WhatsApp, Instagram, and social media ready
‎
‎- 📊 **CRM Dashboard (Planned)**  
‎  Track customers, messages, and engagement
‎
‎- 🌍 **Multi-language Support (Planned)**  
‎  Including local languages and Pidgin
‎
‎---
‎
‎## 🧠 How It Works
‎
‎1. Business uploads a short video of themselves  
‎2. Inputs text or receives a customer message  
‎3. AI generates:
‎   - Script  
‎   - Voice  
‎   - Video  
‎4. Video is sent to customers or posted online  
‎5. System tracks engagement and improves over time  
‎
‎---
‎
‎## 🏗️ Architecture Overview
‎
‎Frontend → FastAPI Backend → Celery Workers → Redis Queue → AI Services → Delivery Channels
‎
‎### Core Components:
‎- **FastAPI** – Backend API  
‎- **Celery** – Background task processing  
‎- **Redis** – Task queue & job state  
‎- **PostgreSQL** – Database (users, customers, jobs)  
‎- **AI Models/APIs** – Text, voice, and video generation  
‎
‎---
‎## Quick start (development)
Prerequisites:
- Python 3.11 (recommended)
- Node.js & npm
- Docker (optional, recommended for redis)
‎## ⚙️ Tech Stack
‎
‎| Layer | Technology |
‎|------|-----------|
‎| Backend | FastAPI (Python) |
‎| Task Queue | Celery |
‎| Broker | Redis (Upstash / Redis Cloud) |
‎| Database | PostgreSQL |
‎| Frontend | React (planned) |
‎| Deployment | Render / Railway |
‎| AI | LLM APIs, TTS, Video generation |
‎
‎---
‎
‎## 📦 Project Structure
‎vidioagent/ │ ├── app/ │   ├── main.py │   ├── celery_app.py │   ├── tasks.py │   ├── models/ │   ├── services/ │ ├── requirements.txt ├── .env (not committed) ├── README.md
‎
‎---
‎
‎## 🔧 Setup Instructions
‎
‎### 1. Clone the repository
‎```bash
‎git clone https://github.com/gidyola79/vidioagent.git
‎cd vidioagent
‎2. Create virtual environment
‎Bash
‎python -m venv venv
‎source venv/bin/activate   # Linux/Mac
‎venv\Scripts\activate      # Windows
‎3. Install dependencies
‎Bash
‎pip install -r requirements.txt
‎4. Set environment variables
‎Create a .env file:
‎Copy `.env.example` to `.env` and fill in the required API keys and settings.
 
‎REDIS_URL=your_redis_url
‎DATABASE_URL=your_database_url
‎OPENAI_API_KEY=your_api_key
...etc
‎
‎5. Run FastAPI server
‎Bash
‎uvicorn app.main:app --reload
‎6. Run Celery worker
‎Bash
‎celery -A app.celery_app.celery_app worker --loglevel=info
‎🌐 Deployment
‎Backend: Render / Railway
‎Redis: Upstash / Redis Cloud
‎Database: Render PostgreSQL / Supabase
‎
Password policy: business owner accounts require a password with a minimum of 8 characters. Use a mix of uppercase, lowercase, numbers, and symbols for stronger protection.

‎🎥 Demo
‎(https://)
‎Example flow:
‎Upload short video
‎Enter text
‎Generate video
‎Send to WhatsApp
‎
‎📈 Impact
‎VidioAgent helps:
‎Increase customer engagement
‎Improve response time
‎Build trust and loyalty
‎Enable small businesses to compete digitally.
‎
‎🔐 Security & Ethics
‎User consent required for video/voice usage
‎No storage of sensitive customer data without encryption
‎Designed to prevent misuse of generated content
‎🚀 Future Improvements
‎Full CRM dashboard
‎WhatsApp automation integration
‎Multi-language support (Yoruba, Igbo, Hausa, Pidgin)
‎Analytics & recommendation engine
‎Mobile app version
‎
‎🤝 Contributing
‎Contributions are welcome!
‎Feel free to fork the repo and submit a pull request.
‎
‎📄 License
‎This project is licensed under the MIT License.
‎
‎🙌 Acknowledgements
‎Built as part of an AI Hackathon focused on improving customer relations for local businesses.
‎
‎👤 Author
‎Olamide Gideon
‎GitHub: https://github.com/gidyola79
