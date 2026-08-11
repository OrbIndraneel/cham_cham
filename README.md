# 🛰️ Disaster Management AI Platform

> **Smart India Hackathon (SIH) 2026 Target Project**  
> An AI-powered platform for early cascade disaster prediction and dynamic hazard-avoiding evacuation route optimization.

---

## 📌 Executive Summary

India experiences 5 to 7 major natural disasters annually, affecting over 30 million people, causing 10,000+ preventable deaths, and driving over ₹40,000 crore in economic losses. 

Current disaster management infrastructure suffers from a **12-hour response latency gap**—the delay between initial hazard detection and actionable alert dissemination. Legacy systems rely on static rules from 2004 that fail to learn from historical data or adapt to evolving climate patterns.

This platform introduces an **AI-Learned Smart Automation Platform** that autonomously extracts patterns from historical disaster datasets, predicts secondary compound cascades (*e.g., Heavy Rainfall → Landslide*), and dynamically calculates safest evacuation routes—reducing response latency to **< 30 minutes** and boosting casualty prevention to **95%**.

---

## 📊 Impact Metrics Target

| Metric | Legacy Disaster Systems | Proposed AI Platform | Target Improvement |
| :--- | :--- | :--- | :--- |
| **Response Latency** | 12 hours | **< 30 minutes** | **24x Faster Response** |
| **Alert Lead Time** | 6–8 hours | **18–24 hours** | **3–4x Earlier Warnings** |
| **False Alarm Rate** | 25–30% | **< 10%** | **3x Reduction in Alarms** |
| **Detection Rate** | 60–70% | **> 95%** | **1.5x Better Coverage** |
| **Lives Saved** | — | **2,250 – 3,150 lives / year** | Direct Human Impact |
| **Economic Loss Saved** | — | **₹20,000+ crore / year** | National Economic Protection |

---

## 🏆 Core Strategy: Track C + Track D Synergy

The project integrates two core technical engines:

1. **Track C: Disaster Cascade Prediction (ML Engine)**
   * **Framework:** PyTorch Geometric (PyG) Graph Attention Networks (GAT).
   * **Function:** Models geographic regions as graph nodes and historical hazard relationships as edges. Predicts secondary chain-reaction hazards with 6–12 hours of lead time (*e.g., Heavy Rainfall + Saturated Soil → 88% Landslide probability*).

2. **Track D: Dynamic Evacuation Route Optimization (Optimization Engine)**
   * **Framework:** Google OR-Tools & NetworkX pathfinding.
   * **Function:** Ingests OpenStreetMap road networks and applies heavy penalties to road segments in GNN-flagged hazard zones, outputting safest turn-by-turn evacuation routes to shelters.

---

## 👥 Dual User Role System

* **🏛️ Control Room / Authority User (Server-End Admin):**
  * Master GIS hazard heatmap showing real-time GNN cascade predictions.
  * Disaster scenario simulator (*"What-If"* rainfall testing).
  * Shelter capacity monitor & emergency alert dispatcher.

* **📱 Evacuee / Civilian User (React Native Field App):**
  * Turn-by-turn navigation avoiding predicted cascade hazard zones.
  * High-priority emergency push alerts breaking through silent mode.
  * One-tap SOS broadcast & offline emergency mode (SMS fallback + SQLite caching).

---

## 🛠️ Tech Stack Specifications

```
 ┌──────────────────────────────────────────────────────────────────┐
 │                    REACT NATIVE MOBILE APP                       │
 │  Expo / React Native  ──>  TypeScript  ──>  react-native-maps    │
 │  expo-location        ──>  expo-notifications  ──>  expo-sqlite  │
 └────────────────────────────────┬─────────────────────────────────┘
                                  │ REST APIs / WebSockets
 ┌────────────────────────────────▼─────────────────────────────────┐
 │                      PYTHON BACKEND SERVER                       │
 │  FastAPI  ──>  PyTorch GNN (Cascade)  ──>  OR-Tools (Routing)    │
 │  PostgreSQL + PostGIS  ──>  OpenStreetMap Graph (OSM)            │
 └──────────────────────────────────────────────────────────────────┘
```

* **Mobile App (Frontend):** React Native (Expo SDK 50+), TypeScript, `react-native-maps`, `expo-location`, `expo-notifications`, `expo-sqlite`, `Zustand`.
* **Backend API (Server):** Python 3.10+, FastAPI, Uvicorn, Pydantic.
* **Machine Learning Engine:** PyTorch Geometric (PyG), PyTorch, Scikit-learn, Pandas.
* **Optimization Engine:** Google OR-Tools, NetworkX, GeoPandas.
* **Spatial Database:** PostgreSQL with PostGIS extension.

---

## 📁 Repository Structure

```text
disaster-management-platform/
│
├── 🐍 backend-server/                           # PYTHON ML & BACKEND SERVER
│   │
│   ├── 🧠 ml_engine/                            # [ML ENGINE - Machine Learning & AI]
│   │   ├── models/                              # GNN Architecture & Weights (gnn_cascade_model.py)
│   │   ├── training/                            # Training & Evaluation Scripts (train_cascade_gnn.py)
│   │   └── feature_engineering/                 # Preprocessing & Graph Builders (build_hazard_graph.py)
│   │
│   ├── 🛣️ optimization/                         # [OPTIMIZATION ENGINE - Route Calculation]
│   │   ├── route_optimizer.py                   # Google OR-Tools Dynamic Pathfinding Solver
│   │   └── hazard_avoidance.py                  # Hazard Penalty Weighting Logic
│   │
│   ├── 📊 data_pipeline/                        # [GIS & DATA PIPELINE - Data Processing]
│   │   ├── historical_disasters/                # EM-DAT & NDMA Historical Datasets
│   │   ├── weather_ingestion.py                 # IMD & CWC Live Data Scrapers
│   │   └── osm_road_networks/                   # OpenStreetMap Road Network Graphs
│   │
│   ├── ⚡ api/                                  # [BACKEND API SERVICES - Server Endpoints]
│   │   ├── main.py                              # FastAPI Application Entry Point
│   │   ├── routes/                              # HTTP REST Endpoints (predict, evacuation, shelters)
│   │   └── schemas/                             # Pydantic JSON Validation Schemas (disaster.py)
│   │
│   ├── 🗄️ database/                             # [DATABASE & SPATIAL GIS LAYER]
│   │   ├── db_config.py                         # PostgreSQL + PostGIS Configuration
│   │   └── spatial_queries.py                   # Geofencing & Spatial Polygon Matching
│   │
│   └── requirements.txt                         # Python Dependency Manifest
│
│
└── 📱 mobile-app/                               # REACT NATIVE MOBILE APPLICATION
    │
    ├── package.json                             # npm package manifest
    ├── App.tsx                                  # React Native Entry Point
    └── src/
        ├── 🎨 components/                       # Reusable UI Widgets (HazardMap, ShelterCard, AlertBanner)
        ├── 📱 screens/                          # Application Views (MapScreen, AlertsScreen, SOSScreen)
        ├── 🌐 services/                         # Native Services & Hardware APIs (api.ts, location, notifications)
        ├── 🔄 store/                            # Zustand Global State Management
        ├── 🧭 navigation/                       # React Navigation Bottom Tabs & Stacks
        └── 📝 types/                            # TypeScript Data Interfaces
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
* Python 3.10+
* Node.js 18+ & npm
* Expo Go app on mobile device (or Android Emulator)

---

### 2. Backend Server Setup

```bash
# Navigate to backend directory
cd backend-server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn api.main:app --reload --port 8000
```

The backend server will be live at `http://localhost:8000`. You can inspect interactive API documentation at `http://localhost:8000/docs`.

---

### 3. Mobile App Setup (React Native)

```bash
# Navigate to mobile app directory
cd mobile-app

# Install npm dependencies
npm install

# Start Expo development server
npx expo start
```

Scan the generated QR code using the **Expo Go** app on your Android or iOS device to launch the application.

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check endpoint |
| `POST` | `/api/predict-cascade` | Triggers GNN cascade model inference given rainfall & location |
| `POST` | `/api/evacuation-route` | Triggers OR-Tools route solver returning hazard-avoiding polyline |
| `GET` | `/api/shelters` | Returns list of nearby safe emergency shelters & current capacities |

---

## 🗓️ Development Roadmap

- [x] **Phase 1:** Project Architecture & Repository Setup
- [ ] **Phase 2:** GNN Model Training on Historical Data & OR-Tools Solver Integration
- [ ] **Phase 3:** React Native Live Map Rendering & Navigation UI
- [ ] **Phase 4:** Offline SQLite Caching & Push Notification Triggers
- [ ] **Phase 5:** Field Testing & SIH 2026 Deployment Demonstration

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).
