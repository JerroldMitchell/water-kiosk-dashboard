# Tusafishe Water Kiosk System - Integration Overview

**Purpose**: Unified view of the entire Tusafishe system showing how hardware, cloud services, and dashboard interconnect.

**Status**: Hardware mature & production-ready | Cloud services skeleton in place | Dashboard spec complete, implementation pending

---

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CUSTOMER INTERACTION LAYER                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────┐       ┌──────────────────────────┐          │
│  │   Physical Water Kiosks  │       │  USSD/SMS Registration   │          │
│  │   (in field)             │       │  (Africa's Talking)      │          │
│  │                          │       │                          │          │
│  │ • Server (ESP32-S3)      │       │ • REGISTER via *123#     │          │
│  │ • Clients (5-6 per)      │       │ • SMS Commands           │          │
│  │ • 4G Modem               │       │ • MTN/Airtel payments    │          │
│  │ • Credential caching     │       └──────────────────────────┘          │
│  └──────────────────────────┘                                             │
│           ▲                                     ▲                         │
│           │                                     │                         │
│   HTTP POST /dispense-                 ngrok HTTP Tunnel                 │
│   verification                         (Port 5000)                       │
│                                                 │                         │
└─────────────────────────┬───────────────────────┼─────────────────────────┘
                          │                       │
┌─────────────────────────┼───────────────────────┼─────────────────────────┐
│              CLOUD SERVICES LAYER (Home Server)                           │
├─────────────────────────┼───────────────────────┼─────────────────────────┤
│                         │                       │                         │
│  ┌──────────────────────▼────────┐   ┌─────────▼──────────────────────┐  │
│  │   Hardware Server              │   │   USSD/SMS Server              │  │
│  │   (water_kiosk_hardware_*)     │   │   (at_server.py)               │  │
│  │   Port: 8080 (local)           │   │   Port: 5000 (ngrok tunnel)    │  │
│  │                                │   │                                │  │
│  │ • Dispense verification        │   │ • USSD registration            │  │
│  │ • PIN validation               │   │ • SMS message handling         │  │
│  │ • Subscription checking        │   │ • Mobile money integration     │  │
│  │ • Credential lookup            │   │ • Customer account creation    │  │
│  │ • Database queries             │   │ • Payment processing (MTN/Air) │  │
│  └──────────┬─────────────────────┘   └─────────┬──────────────────────┘  │
│             │                                   │                         │
│             └─────────────┬─────────────────────┘                         │
│                           │                                               │
│                  HTTP API Calls (localhost)                              │
│                           │                                               │
│             ┌─────────────▼──────────────────────┐                        │
│             │  Appwrite Database                 │                        │
│             │  (localhost/v1)                    │                        │
│             │                                    │                        │
│             │ • customers collection             │                        │
│             │   - phone_number (key)             │                        │
│             │   - pin                            │                        │
│             │   - active (subscription status)   │                        │
│             │   - credits_ml (balance)           │                        │
│             │   - account_id (unique ID)         │                        │
│             │   - full_name                      │                        │
│             │   - kiosk associations             │                        │
│             │   - created_at, updated_at         │                        │
│             │                                    │                        │
│             │ • audit_logs collection (future)   │                        │
│             │ • transaction_logs collection (future) │                    │
│             └────────────────────────────────────┘                        │
│                           ▲                                               │
│                           │                                               │
│                    HTTP API (localhost)                                   │
│                           │                                               │
│             ┌─────────────┴──────────────────────┐                        │
│             │                                    │                        │
│  ┌──────────▼─────────────┐      ┌──────────────▼─────────────┐          │
│  │ Analytics Server        │      │ Customer Dashboard         │          │
│  │ (analytics_server.py)   │      │ (serve_dashboard.py +      │          │
│  │ Port: 8082 (internal)   │      │  customer-dashboard.html)  │          │
│  │                         │      │ Port: 8080 (internal)      │          │
│  │ [PROTOTYPE ONLY]        │      │                            │          │
│  │                         │      │ • Customer search by phone  │          │
│  └─────────────────────────┘      │ • Account ID lookup         │          │
│                                   │ • Pagination support       │          │
│                                   │   (25 docs per request)    │          │
│                                   │ • Live customer stats      │          │
│                                   │ [PROTOTYPE - ACTIVE]       │          │
│                                   └────────────────────────────┘          │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

                           FUTURE: Operators/Admin
                           (Web-based Control Panel)
                                   ▲
                                   │
                         HTTPS Secure Connection
                                   │
┌──────────────────────────────────┼────────────────────────────────────────┐
│          DASHBOARD LAYER (Planned - Next.js)                              │
├──────────────────────────────────┼────────────────────────────────────────┤
│                                  │                                        │
│  • Kiosk Management UI           │                                        │
│  • Real-time Transaction Feed    │ API Calls to Cloud Services           │
│  • Customer Service Portal       │                                        │
│  • Analytics & Reporting         │                                        │
│  • System Health Monitoring      │                                        │
│  • OTA Firmware Management       │                                        │
│                                  │                                        │
└──────────────────────────────────┼────────────────────────────────────────┘
```

---

## System Components & Maturity Status

### 1. Hardware Layer (MATURE ✅ Production Ready)

**Kiosk Hardware (Distributed)**
- Location: `/home/jerrold/workspace/water_dispenser/` (embedded systems, on physical hardware)
- Status: **🟢 PRODUCTION READY**
- Documentation: Extensive (SYSTEM_ARCHITECTURE.md, 1400+ lines)

**Components**:
- **Server**: ESP32-S3 with SIM7670G 4G modem
  - WiFi Access Point (dual networks: Tusafishe_A, Tusafishe_B)
  - Embedded MQTT broker
  - HTTP web server for dashboard
  - OTA firmware coordinator
  - Cloud verification client
  - Transaction logger to SD card

- **Clients** (5-6 per server): ESP32 water dispensers
  - LCD display (20x4 character)
  - 4x4 keypad input
  - Solenoid valve control
  - Flow meter (pulse counter)
  - State machine for dispensing
  - WiFi + MQTT client

**Key Design Decisions**:
- TX power optimized (50 dBm) for RF stability
- Credential caching (1500 user capacity) for offline resilience
- MQTT QoS 1 for reliable message delivery
- Dual partition OTA for safe firmware updates
- 2-minute heartbeat monitoring

**Data Sources**:
- Transaction logs (SD card, CSV format)
- Customer credentials (local cache on server)
- Health metrics (MQTT topics)
- Firmware versions (via heartbeat)

---

### 2. Cloud Services Layer (SKELETON ✅ Exploration Complete, Implementation Starting)

**Current Structure**: Home server with ngrok tunnel (development phase)
- Location: `/home/jerrold/cloud_server/` and `/home/jerrold/water-kiosk-production/`
- Status: **🟡 SKELETON IN PLACE** - Ready for flesh-out
- Documentation: Moderate (ARCHITECTURE.md in water-kiosk-dashboard)

#### A. USSD/SMS Server (`at_server.py`)
- **Port**: 5000 (exposed via ngrok)
- **Status**: ✅ Working prototype
- **Responsibility**: Customer registration & account management
- **Integration Points**:
  - ← Receives: USSD/SMS from Africa's Talking (webhook)
  - → Sends: HTTP API calls to Appwrite
  - ← Returns: USSD/SMS responses to customers

**Handles**:
1. USSD registration flow (*123# → name → PIN → account created)
2. SMS commands (REGISTER, STATUS, BUY, BALANCE)
3. Mobile money integration (MTN MoMo, Airtel Money)
4. Customer account creation/updates
5. Subscription status management

**What's Needed**:
- [ ] Structured error handling with specific error codes
- [ ] Transaction logging (who registered, when, from what number)
- [ ] Rate limiting to prevent SMS spam
- [ ] Webhook signature verification (security)
- [ ] Better error messages back to customers
- [ ] Tests (unit and integration)

#### B. Hardware Server (`water_kiosk_hardware_server.py`)
- **Port**: 8080 (local, requires ngrok reconfiguration to expose)
- **Status**: ✅ Working prototype
- **Responsibility**: Kiosk dispense verification
- **Integration Points**:
  - ← Receives: HTTP POST from physical kiosks (4G modem)
  - → Sends: HTTP API calls to Appwrite
  - ← Returns: Approval/denial response to kiosk

**Handles**:
1. Credential verification (phone + PIN lookup)
2. Subscription status checking
3. PIN validation
4. Water dispense approval/denial decisions
5. Customer data queries
6. Database create/update operations

**Flow**:
```
Kiosk (4G)
  → POST /dispense-verification {kiosk_id, user_id, pin, volume_ml}
    → Hardware Server
      → Query Appwrite: SELECT * FROM customers WHERE phone_number = user_id
      → Verify PIN matches
      → Check active = true
      → Check daily limits
      → Return {approved: true/false, reason, user_data}
    ← Response back to Kiosk
  ← Kiosk dispenses or denies
```

**What's Needed**:
- [ ] Request validation (input sanitization)
- [ ] Transaction logging (all requests/responses)
- [ ] Caching layer (to reduce Appwrite queries)
- [ ] Rate limiting per kiosk
- [ ] Better error codes for different denial reasons
- [ ] Tests (unit, integration, load)

#### C. Appwrite Database
- **Location**: `/home/jerrold/appwrite` (Docker container, localhost)
- **Project ID**: `689107c288885e90c039`
- **Database ID**: `6864aed388d20c69a461`
- **Status**: ✅ Running

**Current Collections**:
- `customers` - All customer data

```json
{
  "_id": "unique_id",
  "phone_number": "+254700000102",
  "pin": "1234",
  "active": true,
  "is_registered": true,
  "credits": 5000,
  "account_id": "AQP123456",
  "full_name": "Jane Smith",
  "registration_state": "completed",
  "created_at": "2025-08-10T00:00:00Z",
  "location": "optional_location"
}
```

**What's Needed**:
- [ ] Audit logging collection (track all changes)
- [ ] Transaction logging collection (historical records)
- [ ] Daily usage tracking (per customer, per day)
- [ ] Subscription expiration dates
- [ ] Kiosk associations (which kiosks can a customer access)
- [ ] Indexing on phone_number, account_id, created_at
- [ ] Backup strategy

---

### 3. Dashboard Layer (SPEC COMPLETE ✅, IMPLEMENTATION PENDING)

**Status**: 🔴 **Prototypes exist, not production code**
- Spec: `CLOUD_DASHBOARD_SPEC.md` (740 lines, detailed)
- Proto HTML: `customer-dashboard.html` (basic)
- Proto Server: `serve_dashboard.py` + `analytics_server.py`

**What the Spec Says Should Exist**:
1. **Kiosk Management**
   - Inventory view (list all kiosks with status)
   - Kiosk detail view (server health, connected clients, config)
   - OTA firmware update coordination
   - Real-time monitoring of device connectivity

2. **Transaction Analytics**
   - Real-time transaction feed (live updates)
   - Charts (top users, volume distribution, success rates)
   - Export capabilities (CSV, PDF)

3. **Customer Service Portal**
   - Customer search & lookup
   - Account management (extend subscription, adjust limits, reset PIN)
   - Transaction dispute resolution
   - Bulk operations (import/export)

4. **System Monitoring**
   - System health dashboard (kiosks online, success rate, alerts)
   - Alert system (critical, warning, info)
   - Real-time WebSocket updates

**What Currently Exists** (Prototypes):
- Basic customer lookup page (HTML + simple API)
- CSV-based analytics (read transaction files)
- No real-time updates
- No OTA management
- No authentication/RBAC

**What's Needed**:
- [ ] Frontend: Next.js + React + Tailwind CSS setup
- [ ] Authentication: Appwrite Auth + JWT tokens
- [ ] Real-time: WebSocket server (connect to kiosk MQTT?)
- [ ] APIs: Implement all endpoints from spec (40+ endpoints)
- [ ] Charts: Recharts or D3.js integration
- [ ] State management: React Context or Redux
- [ ] Testing: Unit, integration, E2E tests
- [ ] Responsive design (mobile, tablet, desktop)

---

## Data Flow Scenarios (End-to-End)

### Scenario 1: Customer Registration (USSD)

```
Customer                    Africa's Talking        at_server.py          Appwrite
   │                               │                     │                  │
   ├─ Dials *123# ────────────────→│                     │                  │
   │                               │                     │                  │
   │                               ├─ Webhook POST ─────→│                  │
   │                               │                     ├─ Check if exists  │
   │                               │                     │ (phone_number)    │
   │                               │                     ├─ If new: create   │
   │                               │                     ├─────────────────→│
   │                               │←─ Response ────────┤                  │
   │                               │                     │← Returns _id     │
   │                               │                     │                  │
   │←─ USSD Response ──────────────┤                     │                  │
   │   "Enter your name"           │                     │                  │
   │                               │                     │                  │
   ├─ Types name ─────────────────→│                     │                  │
   │                               ├─ Webhook POST ─────→│                  │
   │                               │                     ├─ Update DB      │
   │                               │                     │ full_name = ...  │
   │                               │                     ├─────────────────→│
   │                               │←─ Response ────────┤                  │
   │                               │                     │← OK              │
   │                               │                     │                  │
   │←─ USSD Response ──────────────┤                     │                  │
   │   "Enter 4-digit PIN"         │                     │                  │
   │                               │                     │                  │
   ├─ Types PIN ──────────────────→│                     │                  │
   │                               ├─ Webhook POST ─────→│                  │
   │                               │                     ├─ Update DB      │
   │                               │                     │ pin = ...        │
   │                               │                     │ is_registered=true
   │                               │                     │ account_id = ... │
   │                               │                     ├─────────────────→│
   │                               │←─ Response ────────┤                  │
   │                               │                     │← OK, returns ID │
   │                               │                     │                  │
   │←─ USSD Response ──────────────┤                     │                  │
   │   "Account created! ID: AQP123456"                  │                  │
   │                               │                     │                  │
   ✅ Customer now registered and ready to dispense water
```

**Data persisted in Appwrite**:
```json
{
  "phone_number": "+254700000102",
  "full_name": "Jane Smith",
  "pin": "1234",
  "account_id": "AQP123456",
  "is_registered": true,
  "active": true,
  "credits": 0,
  "created_at": "2025-11-09T14:30:00Z"
}
```

---

### Scenario 2: Water Dispensing (Hardware Verification)

```
Customer at Kiosk        Kiosk Server (4G)       Hardware Server        Appwrite
       │                      │                        │                   │
       ├─ Enters phone + PIN──→│                        │                   │
       │                      │                        │                   │
       │                      ├─ HTTP POST ───────────→│                   │
       │                      │ /dispense-verification │                   │
       │                      │ {user_id, pin, vol}    │                   │
       │                      │                        ├─ Query DB ────→  │
       │                      │                        │ SELECT * FROM    │
       │                      │                        │ customers WHERE  │
       │                      │                        │ phone=user_id   │
       │                      │                        │←────────────────│
       │                      │                        │ {pin, active, ok}│
       │                      │                        │                  │
       │                      │                        ├─ Verify PIN     │
       │                      │                        ├─ Check active   │
       │                      │                        │                  │
       │                      │←───── Approved ───────┤                   │
       │                      │ {approved: true,       │                   │
       │                      │  reason: "verified"}   │                   │
       │                      │                        │                   │
       ├─ Water dispensing ───→│                        │                   │
       │ Opens valve           │                        │                   │
       │                       │ Measures flow          │                   │
       │                       │ (500 mL dispensed)     │                   │
       │                       │                        │                   │
       │ Shows completion ←────│                        │                   │
       │                       │                        │                   │
       ✅ Transaction complete, logged to SD card
```

**If cloud unavailable**:
- Kiosk checks local credential cache
- If customer in cache → auto-approve
- If customer NOT in cache → deny

---

### Scenario 3: Dashboard Monitoring (Future - Not Yet Implemented)

```
Operator (Web Browser)       Dashboard (Next.js)      Backend APIs       Cloud Services
         │                          │                      │                  │
         ├─ Opens dashboard ───────→│                      │                  │
         │                          ├─ WebSocket conn ────→│                  │
         │                          │ (real-time updates)  │                  │
         │                          │                      │                  │
         │                          │                      ├─ GET /kiosks ──→│
         │                          │←─ JSON list ────────│←─ Query DB    │
         │←─ Display kiosks ────────│                      │                │
         │   (status, count, etc)   │                      │                │
         │                          │                      │                │
         ├─ Clicks "Start OTA" ────→│                      │                │
         │                          │                      ├─ POST /ota ───→│
         │                          │                      │ /sequence/start│
         │                          │                      │←─ OK, ID ─────│
         │                          │                      │                │
         │                          │←─ WS: OTA Started ──│                │
         │←─ Progress bar ─────────│                      │                │
         │   (updating in real-time)│                      │                │
         │                          │ (10s polling)        │                │
         │                          ├─ GET /ota/status ──→│                │
         │                          │←─ {progress: 5/10}──│                │
         │                          │                      │                │
         │←─ Update progress ──────│                      │                │
         │ (5 of 10 clients done)   │                      │                │
         │                          │                      │                │
         ✅ OTA complete when all clients updated
```

---

## Integration Points & Dependencies

### Hardware → Cloud Communication

| Hardware | Cloud Service | Protocol | Direction | Purpose |
|----------|---------------|----------|-----------|---------|
| Kiosk (4G modem) | Hardware Server | HTTP POST | →← | Dispense verification |
| Kiosk (MQTT) | Kiosk Server (MQTT broker) | MQTT | →← | OTA updates, config |
| Kiosk (SD card) | Analytics (scheduled) | Manual/SSH | ← | Transaction log export |

### Cloud Services → Database

| Service | Database | Protocol | Purpose |
|---------|----------|----------|---------|
| at_server.py | Appwrite | HTTP API | Customer registration/updates |
| hardware_server.py | Appwrite | HTTP API | Customer verification/queries |
| serve_dashboard.py | Appwrite | HTTP API | Customer lookup (future) |
| analytics_server.py | CSV files | File I/O | Analytics calculations |

### External Integrations

| Service | Purpose | Current Status |
|---------|---------|-----------------|
| Africa's Talking | SMS/USSD webhook | ✅ Working |
| MTN MoMo API | Payment processing | ✅ Integrated in at_server.py |
| Airtel Money API | Payment processing | ✅ Integrated in at_server.py |
| ngrok | External tunnel | ✅ Temporary (home server only) |

---

## What Needs to Be Built Next

### Phase 1: Strengthen Cloud Services (Months 1-2)
**Priority**: HIGH - Enable simultaneous USSD/SMS and Hardware testing

1. **ngrok Limitation Fix** (Choose one approach):
   - Option A: Move to production server (data center) - eliminates ngrok
   - Option B: Docker setup with separate ngrok instances per service
   - Option C: Switch from ngrok to alternative (AWS API Gateway, Cloudflare Tunnel)

2. **Security Hardening**:
   - Move credentials to environment variables (.env)
   - Add webhook signature verification (Africa's Talking)
   - Implement rate limiting on all endpoints
   - Add input validation/sanitization

3. **Logging & Monitoring**:
   - Structured logging (JSON) to files
   - Error tracking (Sentry or similar)
   - Uptime monitoring
   - Database backup strategy

4. **Testing**:
   - Unit tests for USSD registration flow
   - Unit tests for hardware verification flow
   - Integration tests (full end-to-end)
   - Load testing (100+ concurrent requests)

### Phase 2: Build Production Dashboard (Months 3-6)
**Priority**: MEDIUM - Provide operational visibility

1. **Authentication & Authorization**:
   - Appwrite Auth integration
   - Role-based access control (admin, technician, customer_service)
   - Session management

2. **APIs** (from CLOUD_DASHBOARD_SPEC.md):
   - Kiosk management endpoints (40+ APIs)
   - Transaction analytics endpoints
   - Customer service endpoints
   - System health endpoints

3. **Frontend** (Next.js):
   - Responsive UI components
   - Real-time data updates (WebSocket)
   - Charts and visualizations
   - Mobile-friendly design

4. **Database Enhancements**:
   - Audit logging collection
   - Transaction history collection
   - Subscription tracking

### Phase 3: Production Deployment (Months 7-9)
**Priority**: MEDIUM - Prepare for scaling

1. **Infrastructure**:
   - Data center provisioning
   - Docker containerization
   - Load balancing setup
   - SSL/TLS certificates

2. **Performance & Scale**:
   - Database indexing & optimization
   - Caching layer (Redis)
   - Query optimization
   - Load test with 600+ kiosks

3. **Operations**:
   - Monitoring dashboards
   - Alert system
   - Incident response procedures
   - Runbooks for common tasks

---

## Critical Questions Before Moving Forward

1. **Simultaneous Services**: How do you want to solve the ngrok limitation?
   - Commit to data center migration timeline?
   - Docker + multiple ngrok instances?
   - Different tunnel service?

2. **Dashboard Priority**: Is the Next.js dashboard critical for your timeline?
   - If yes, prioritize Phase 2
   - If no, focus on Phase 1 (strengthen services)

3. **Scaling Timeline**: When do you expect >100 kiosks in production?
   - Affects database schema design
   - Impacts API design (pagination, filtering)
   - Determines performance requirements

4. **Data Center**: Do you have commitments/timeline for migration?
   - Impacts authentication strategy
   - Affects SSL/TLS planning
   - Determines infrastructure decisions

---

## Recommended Immediate Actions (This Week)

1. **Create `.env` file template** for credentials (at_server.py, hardware_server.py)
2. **Document all ngrok configurations** currently in use
3. **Identify data center provider** and timeline
4. **Run load test**: Can Appwrite handle 100 concurrent /dispense-verification requests?
5. **List all hardcoded values** that should be configuration (ports, API keys, timeouts)

---

**This document serves as the foundation for detailed implementation planning.**
Each phase can now be broken down into specific stories and tasks.

Last updated: November 9, 2025
