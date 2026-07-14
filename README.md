# StayFinder Coimbatore 🏢

StayFinder is a premium, full-stack web application designed to help students, working professionals, and parents discover PGs, hostels, and rental rooms exclusively in and around Coimbatore, Tamil Nadu. Built with a modern aesthetic inspired by platforms like Airbnb, it offers a seamless booking and property management experience.

---

## 🌟 Key Features

### User Roles & Dashboards
- **Student Flow:** Search properties by location/amenities, view property details on interactive maps, wishlist properties, schedule visits, and complete mock payments for advances.
- **Owner Flow:** Manage property listings, upload property images to Cloudinary, track analytics (views, bookings, revenue) via an interactive dashboard, and approve/reject/reschedule visit requests.
- **Admin Panel:** Centralized command center to monitor the platform, verify properties to ensure quality standards, and suspend/activate users.

### Core Platform Integrations
- **Real-Time Chat:** WebSocket-powered messaging allowing students and owners to communicate seamlessly.
- **Interactive Maps:** OpenStreetMap integration (`react-leaflet`) for accurate property location visualization.
- **Mock Payment Gateway:** Simulated checkout flow (inspired by Razorpay) for advance booking payments.
- **Notification Center:** In-app real-time alerts for booking status updates, payments, and messages.

---

## 🛠️ Technology Stack

**Frontend:**
- React 18 (Vite)
- Tailwind CSS (Custom thematic UI with dark/light mode)
- React Router DOM (with Lazy Loading / Code Splitting)
- Lucide React (Icons)
- React Leaflet (Maps)

**Backend:**
- Python 3.11 / Django 5.x
- Django REST Framework (DRF)
- Django Channels & Redis (for WebSockets / Real-Time Chat)
- PostgreSQL (Database)
- Simple JWT (Authentication)
- Cloudinary (Media Storage)

**DevOps & Deployment:**
- Docker & Docker Compose
- Multi-stage builds for production

---

## 🚀 Getting Started

You can run this project either natively on your machine or fully containerized using Docker.

### Option A: Using Docker (Recommended)
Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

1. Clone the repository and navigate to the root directory.
2. Run the following command:
   ```bash
   docker compose up --build
   ```
3. The frontend will be available at `http://localhost` and the backend at `http://localhost:8000`.

### Option B: Local Setup (Without Docker)

#### 1. Setup Backend (Django)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the Django server (Uses ASGI Daphne automatically)
python manage.py runserver
```

#### 2. Setup Frontend (React)
Open a new terminal window:
```powershell
cd frontend
npm install

# Start the Vite development server
npm run dev
```
The frontend will be available at `http://localhost:5173`.

---

## 📁 Project Structure

```text
Stay_finder_App-1/
├── backend/                  # Django Backend
│   ├── apps/                 # Django apps (users, properties, bookings, chat, etc.)
│   ├── stayfinder/           # Core Django settings and ASGI/WSGI configs
│   ├── manage.py             
│   └── requirements.txt      
├── frontend/                 # React Frontend
│   ├── src/                  
│   │   ├── components/       # Reusable UI components (Navbar, Modals, Forms)
│   │   ├── pages/            # View components (Home, Dashboards, Auth)
│   │   ├── services/         # API integration layers
│   │   ├── contexts/         # React Contexts (Auth, Theme)
│   │   └── index.css         # Tailwind directives and CSS variables
│   ├── package.json          
│   └── vite.config.js        
├── docker-compose.yml        # Orchestration for PostgreSQL, Redis, Django, and React
└── README.md
```

## 🔒 Environment Variables
Ensure you have the appropriate environment variables set up (especially for Cloudinary and PostgreSQL). Defaults are provided in the respective `settings.py` and `vite.config.js` files for local development.
