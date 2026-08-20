# 🛰️ Disaster Management AI Platform

> **Smart India Hackathon (SIH) 2026 Target Project**  
> An AI-powered platform for early cascade disaster prediction and dynamic hazard-avoiding evacuation route optimization.

---

## 📌 Executive Summary

India experiences 5 to 7 major natural disasters annually, affecting over 30 million people, causing 10,000+ preventable deaths, and driving over ₹40,000 crore in economic losses. 

Current disaster management infrastructure suffers from a **12-hour response latency gap**—the delay between initial hazard detection and actionable alert dissemination. Legacy systems rely on static rules from 2004 that fail to learn from historical data or adapt to evolving climate patterns.

This platform introduces an **AI-Learned Smart Automation Platform** that autonomously extracts patterns from historical disaster datasets, predicts secondary compound cascades (*e.g., Heavy Rainfall → Landslide*), and dynamically calculates safest evacuation routes—reducing response latency to **< 30 minutes** and boosting casualty prevention to **95%**.

---

## 🧱 The 4 Core Pillars of the Project

The entire architecture is divided into **four modular pillars**:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                       1. MOBILE APP (FRONTEND)                          │
 │  React Native / Expo  ──>  react-native-maps  ──>  expo-location/sqlite │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │ REST APIs / WebSockets
 ┌────────────────────────────────────▼────────────────────────────────────┐
 │                       3. BACKEND SERVER & API                           │
 │  FastAPI Server  ──>  OR-Tools Route Solver  ──>  Live Ingestion        │
 └─────────────┬─────────────────────────────────────────────┬─────────────┘
               │                                             │
 ┌─────────────▼─────────────┐                 ┌─────────────▼─────────────┐
 │    2. MACHINE LEARNING    │                 │    4. SPATIAL DATABASE    │
 │ PyTorch Geometric GNN     │                 │ PostgreSQL + PostGIS      │
 └───────────────────────────┘                 └───────────────────────────┘
```

1. 📱 **Mobile App (Frontend):** React Native (Expo), TypeScript, `react-native-maps`, `expo-location`, `expo-notifications`, `expo-sqlite`. Handles live map rendering of hazard polygons & route polylines, dual admin/user roles, high-priority push alerts, offline SQLite caching, and one-tap SOS.
2. 🧠 **Machine Learning (ML Engine):** PyTorch Geometric (PyG) GNN (Graph Attention Network) trained on EM-DAT and NDMA disaster datasets. Predicts secondary compound cascades (*e.g., Flood → Landslide*) with a 6–12 hour lead time.
3. ⚡ **Backend Server (API & Optimization):** Python FastAPI + Google OR-Tools / NetworkX. Exposes REST API endpoints (`/api/predict-cascade`, `/api/evacuation-route`), calculates hazard-avoiding evacuation routes, and ingests live IMD rainfall & CWC river gauge data.
4. 🗄️ **Database (Spatial & GIS Data Layer):** PostgreSQL with PostGIS extension. Manages spatial geofence indexing (`ST_Contains`), OpenStreetMap road network graphs, and shelter capacity records.

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

## 📁 Repository Structure

```text
disaster-management-platform/
│
├── 🐍 backend-server/                           # PYTHON ML & BACKEND SERVER
│   │
│   ├── 🧠 ml_engine/                            # [PILLAR 2: ML ENGINE - Machine Learning]
│   │   ├── models/                              # GNN Architecture & Weights (gnn_cascade_model.py)
│   │   ├── training/                            # Training & Evaluation Scripts (train_cascade_gnn.py)
│   │   └── feature_engineering/                 # Preprocessing & Graph Builders (build_hazard_graph.py)
│   │
│   ├── 🛣️ optimization/                         # [PILLAR 3: OPTIMIZATION ENGINE]
│   │   ├── route_optimizer.py                   # Google OR-Tools Dynamic Pathfinding Solver
│   │   └── hazard_avoidance.py                  # Hazard Penalty Weighting Logic
│   │
│   ├── 📊 data_pipeline/                        # [PILLAR 3: DATA PIPELINE]
│   │   ├── historical_disasters/                # EM-DAT & NDMA Historical Datasets
│   │   ├── weather_ingestion.py                 # IMD & CWC Live Data Scrapers
│   │   └── osm_road_networks/                   # OpenStreetMap Road Network Graphs
│   │
│   ├── ⚡ api/                                  # [PILLAR 3: BACKEND API SERVICES]
│   │   ├── main.py                              # FastAPI Application Entry Point
│   │   ├── routes/                              # HTTP REST Endpoints (predict, evacuation, shelters)
│   │   └── schemas/                             # Pydantic JSON Validation Schemas (disaster.py)
│   │
│   ├── 🗄️ database/                             # [PILLAR 4: SPATIAL DATABASE LAYER]
│   │   ├── db_config.py                         # PostgreSQL + PostGIS Configuration
│   │   └── spatial_queries.py                   # Geofencing & Spatial Polygon Matching
│   │
│   └── requirements.txt                         # Python Dependency Manifest
│
│
└── 📱 Suraksha_AI_App/                          # REACT NATIVE EXPO MOBILE APPLICATION
    │
    ├── package.json                             # npm package manifest & Expo SDK 57 dependencies
    ├── app.json                                 # Expo configuration manifest
    ├── app/                                     # Expo Router file-based app routes (civilian & authority)
    │   ├── civilian/                            # Civilian user UI (live map, bottom sheets, SOS)
    │   └── authority/                           # Authority control room dashboard & simulator
    └── src/
        ├── 🎨 components/                       # UI components (HazardMap, ShelterBottomSheet, AlertBanner)
        ├── 🌐 services/                         # Dual-mode API Client, Location, Notification & Storage
        ├── 🔄 store/                            # Zustand stores (useDisasterStore, useAuthorityStore, etc.)
        └── 📝 types/                            # TypeScript interfaces (Disaster, Alert, User profiles)
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
* Python 3.10+
* Node.js 18+ & npm
* Expo Go app on mobile device (or Android / iOS Emulator)

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

### 3. Mobile App Setup (Suraksha AI App)

```bash
# Navigate to Suraksha AI App directory
cd Suraksha_AI_App

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
