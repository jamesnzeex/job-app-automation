# Job Application Automation 🗻

Automated job application tracker and finder for LinkedIn and Indeed.

## 🎯 Features

- **Job Discovery**: Scrape LinkedIn and Indeed with smart filters
- **Application Tracking**: Centralized dashboard for all applications
- **Auto-fill**: Extract and auto-fill job application forms
- **Tailored Applications**: Resume/CV optimization per job description
- **Local-First**: All data stored locally, optional sync later
- **Analytics**: Response rates, conversion funnels, insights

## 📁 Project Structure

```
job-app-automation/
├── src/
│   ├── api/              # FastAPI backend
│   ├── scrapers/         # LinkedIn, Indeed scraping
│   ├── models/           # Data models & DB schema
│   └── utils/            # Helpers, config, logging
├── web/                  # Next.js frontend
├── scripts/              # Automation scripts
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── .env.example          # Environment template
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run the app
python -m src.api
cd web && npm run dev
```

## 🛠️ Tech Stack

- **Backend**: FastAPI + SQLite
- **Frontend**: Next.js + Tailwind
- **Scraping**: Playwright (for LinkedIn/Indeed)
- **Storage**: Local SQLite (expandable to PostgreSQL)
- **Automation**: Browser automation with Playwright

## 🔐 Environment Variables

```env
# LinkedIn (optional - for scraping)
LINKEDIN_EMAIL=
LINKEDIN_PASSWORD=

# Indeed (optional - for scraping)
INDEED_EMAIL=
INDEED_PASSWORD=

# Database
DB_PATH=./data/applications.db

# API
API_PORT=8000
```

## 📋 Roadmap

- [ ] Core: Application tracking database schema
- [ ] LinkedIn scraper (basic)
- [ ] Indeed scraper (basic)
- [ ] Web dashboard (React/Next.js)
- [ ] Auto-fill functionality
- [ ] Resume/CV optimization
- [ ] Analytics dashboard

## 🤝 Contributing

This is a personal project, but feel free to suggest improvements!

## License

MIT
