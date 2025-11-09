# Tusafishe Water Kiosk Cloud Server - Architecture Documentation

## Executive Summary

The Tusafishe Water Kiosk system is a three-tier architecture consisting of:
1. **Customer Interaction Layer** - USSD/SMS and Hardware Verification
2. **Backend Services** - Flask-based HTTP servers
3. **Database Layer** - Appwrite for customer data management

Currently deployed on a home-based server with internet access restrictions. Will be migrated to a data center for production deployment.

---

## Current Architecture (Home Server)

### System Constraints

- **Single ngrok tunnel** (free tier limitation)
- Only one external port can be exposed at a time
- Current configuration: Port 5000 (USSD/SMS server)
- Appwrite runs locally (no external access needed)

### Current Operating Mode

**When SMS/USSD Testing is Active:**

```
┌─────────────────────────────────────────────────────────┐
│                    External Network                      │
│  Africa's Talking SMS Platform                          │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ SMS Webhook
                         ▼
                    ┌─────────────┐
                    │   ngrok     │
                    │ Port 5000   │
                    │ Tunnel      │
                    └────────┬────┘
                             │
        ┌────────────────────▼────────────────────┐
        │         Home Server Network             │
        │                                          │
        │  ┌──────────────────────────────────┐   │
        │  │  at_server.py                    │   │
        │  │  (USSD/SMS Server)               │   │
        │  │  - USSD Handler (main_callback)  │   │
        │  │  - SMS Handler (sms_callback)    │   │
        │  │  - Payment Processing (MTN/Airtel)  │   │
        │  │  - Customer Registration         │   │
        │  │  - Port: 5000                    │   │
        │  └──────────────┬───────────────────┘   │
        │                 │                        │
        │                 │ HTTP API Calls         │
        │                 ▼                        │
        │  ┌──────────────────────────────────┐   │
        │  │  Appwrite (localhost)            │   │
        │  │  - Project ID: 689107c288885e... │   │
        │  │  - customers collection          │   │
        │  │  - Stores all customer data      │   │
        │  └──────────────────────────────────┘   │
        └─────────────────────────────────────────┘
```

**When Kiosk Hardware Testing is Active:**

```
┌─────────────────────────────────────────────────────────┐
│                    External Network                      │
│  Physical Water Kiosks (in field)                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ HTTP Request (Verification)
                         ▼
                    ┌─────────────┐
                    │   ngrok     │
                    │ Port 5000   │
                    │ Tunnel      │
                    └────────┬────┘
                             │
        ┌────────────────────▼────────────────────┐
        │         Home Server Network             │
        │                                          │
        │  ┌──────────────────────────────────┐   │
        │  │  water_kiosk_hardware_server.py  │   │
        │  │  (Hardware Verification Server)  │   │
        │  │  - Dispense Verification         │   │
        │  │  - PIN Validation                │   │
        │  │  - Subscription Check            │   │
        │  │  - Database Operations           │   │
        │  │  - Port: 8080 (local)            │   │
        │  └──────────────┬───────────────────┘   │
        │                 │                        │
        │                 │ HTTP API Calls         │
        │                 ▼                        │
        │  ┌──────────────────────────────────┐   │
        │  │  Appwrite (localhost)            │   │
        │  │  - Project ID: 689107c288885e... │   │
        │  │  - customers collection          │   │
        │  │  - Retrieves customer data       │   │
        │  └──────────────────────────────────┘   │
        └─────────────────────────────────────────┘
```

### Important Limitation

**⚠️  CANNOT RUN BOTH SIMULTANEOUSLY:**
- Only one of these can be externally accessible at a time
- Switching requires:
  1. Stopping ngrok
  2. Reconfiguring to different port
  3. Restarting ngrok
  4. Restarting the appropriate server

---

## Active Services (Currently Deployed)

### 1. USSD/SMS Server
- **Project**: `water-kiosk-ussd-server`
- **File**: `at_server.py`
- **Port**: 5000
- **Exposed via**: ngrok tunnel to `first-many-snake.ngrok-free.app`
- **Features**:
  - USSD Registration (*123#)
  - SMS Commands (REGISTER, STATUS, BUY)
  - MTN Mobile Money payments
  - Airtel Money payments
  - Customer account management
  - Auto-detects USSD vs SMS requests
- **Database**: Direct HTTP API to local Appwrite
- **Status**: ✅ ACTIVE

### 2. Hardware Verification Server
- **Project**: `water-kiosk-hardware-server` (in water-kiosk-production)
- **File**: `water_kiosk_hardware_server.py`
- **Port**: 8080
- **External Access**: Requires ngrok reconfiguration
- **Features**:
  - Customer credential verification (phone + PIN)
  - Subscription status checking
  - Water dispensing approval/denial
  - Database query/create/update operations
- **Database**: Direct HTTP API to local Appwrite
- **Status**: ✅ ACTIVE (requires ngrok switch to test)

### 3. Appwrite Backend
- **Location**: `/home/jerrold/appwrite`
- **Access**: `http://localhost/v1` (local only)
- **Project ID**: `689107c288885e90c039`
- **Database ID**: `6864aed388d20c69a461`
- **Key Collections**:
  - `customers` - All customer data (phone, PIN, registration status, subscription, credits, etc.)
- **Launch**: `cd ~/appwrite && docker-compose up -d`
- **Status**: ✅ ACTIVE

### 4. Analytics Dashboard
- **Project**: `water-kiosk-analytics`
- **File**: `analytics_server.py`
- **Port**: 8082
- **Features**:
  - CSV transaction analysis
  - User consumption patterns
  - Kiosk activity breakdown
  - Visual charts and statistics
- **No external access needed**
- **Status**: ✅ ACTIVE (internal use)

### 5. Customer Service Dashboard
- **Project**: `water-kiosk-dashboard`
- **File**: `customer-dashboard.html` + `serve_dashboard.py`
- **Port**: 8080
- **Features**:
  - Web interface for customer lookup
  - Account status checking
  - Customer data management
  - Requires Appwrite running
- **Launch**: `./start_dashboard.sh`
- **Status**: ✅ ACTIVE (internal use)

---

## Legacy/Archived Services

### ⚠️ Appwrite Functions (NOT IN USE)

Two Appwrite functions exist but are **NOT deployed or used**:

1. **water-kiosk-hardware-function**
   - Location: `~/Tusafishe/functions/water-kiosk-hardware-function`
   - Status: 🔴 ARCHIVED - Flask server handles this functionality
   - Reason: Flask server provides same functionality with direct HTTP API

2. **water-kiosk-sms-function**
   - Location: `~/Tusafishe/functions/water-kiosk-sms-function`
   - Status: 🔴 ARCHIVED - at_server.py includes SMS handling
   - Reason: at_server.py consolidated SMS and USSD in one application

### Why Functions Were Replaced

Appwrite Functions required:
- Deployment within Appwrite instance
- Function-specific ngrok tunneling (adds complexity)
- Extra processing overhead
- Ngrok free tier can't handle multiple endpoints

Flask servers are:
- Simpler to develop/test
- Can be run locally or remotely
- Better control over dependencies
- More flexible for ngrok tunneling

**Recommendation**: Archive/delete these function projects

---

## Data Flow Overview

### Customer Registration Flow (USSD/SMS)

```
1. User dials *123# or sends SMS
        ↓
2. Africa's Talking receives request
        ↓
3. Sends webhook to ngrok tunnel
        ↓
4. at_server.py processes request
        ↓
5. Makes HTTP API call to Appwrite
        ↓
6. Customer created/updated in database
        ↓
7. Response sent back through tunnel
        ↓
8. User receives USSD/SMS response
```

### Water Dispensing Flow (Hardware)

```
1. User enters phone + PIN at kiosk
        ↓
2. Kiosk sends HTTP request
        ↓
3. Request reaches server via ngrok
        ↓
4. hardware_server.py processes verification
        ↓
5. Queries Appwrite for customer data
        ↓
6. Validates PIN and subscription status
        ↓
7. Returns approval/denial
        ↓
8. Kiosk dispenses water or denies access
```

---

## Future Architecture (Data Center)

### System Capabilities

Once moved to a proper data center:
- ✅ Multiple simultaneous ports (no ngrok needed)
- ✅ Direct internet access
- ✅ Proper SSL/TLS certificates
- ✅ Scalable infrastructure
- ✅ Both USSD/SMS and Hardware servers running simultaneously

### Proposed Data Center Setup

```
┌──────────────────────────────────────────────────────────────┐
│                   Internet / External Network                 │
│                                                                │
│  Africa's Talking ──────────┐                                │
│                             │ SMS Webhooks                    │
│  Physical Kiosks ──────────┐│                                │
│                            ││                                │
└────────────────────────────┼┼────────────────────────────────┘
                             ││
                    ┌────────┘│
                    │         │
          ┌─────────▼─────────▼────────────┐
          │   Data Center Server/Load      │
          │   Balancer                     │
          └─────────┬──────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │ Port   │  │ Port   │  │ Port   │
   │ 5000   │  │ 8080   │  │ 443    │
   └────┬───┘  └────┬───┘  └───┬────┘
        │           │          │
   ┌────▼──────┐┌───▼────────┐ │
   │ USSD/SMS  ││ Hardware   │ │ SSL/TLS
   │ Server    ││ Server     │ │ API
   │ (at_server││(hardware_  │ │
   │ .py)      ││ server.py) │ │
   └────┬──────┘└───┬────────┘ │
        │           │          │
        └─────────┬─┴──────────┘
                  │
        ┌─────────▼──────────┐
        │ Appwrite Database  │
        │ - customers        │
        │ - transactions     │
        │ - audit logs       │
        └────────────────────┘

        ┌─────────────────────┐
        │ Analytics & Storage │
        │ - CSV files         │
        │ - Reports           │
        └─────────────────────┘
```

### Production Deployment Checklist

- [ ] Procure data center server/hosting
- [ ] Configure multiple ports (5000, 8080, 443)
- [ ] Set up SSL/TLS certificates
- [ ] Deploy Appwrite to data center
- [ ] Deploy at_server.py to production
- [ ] Deploy hardware_server.py to production
- [ ] Configure Africa's Talking webhook to new domain
- [ ] Update kiosk endpoints to new server
- [ ] Set up monitoring and logging
- [ ] Implement load balancing if needed
- [ ] Database backups and disaster recovery
- [ ] Performance testing under load

---

## Project Structure

```
/home/jerrold/cloud_server/
├── water-kiosk-ussd-server/          [ACTIVE]
│   ├── at_server.py                  ← Main USSD/SMS server
│   ├── ussd_server.py                (Basic version, not used)
│   ├── setup_mtn_user.py
│   ├── start_server_with_mtn.sh
│   ├── requirements.txt
│   └── README.md
│
├── water-kiosk-analytics/             [ACTIVE - Internal]
│   ├── analytics_server.py
│   ├── start_analytics.sh
│   ├── templates/
│   └── transactions*.csv (sample data)
│
├── water-kiosk-dashboard/             [ACTIVE - Internal]
│   ├── customer-dashboard.html
│   ├── serve_dashboard.py
│   └── start_dashboard.sh
│
└── support/                           [UTILITY]
    ├── generate_test_users.py
    ├── export_test_users.py
    └── test_users*.csv

/home/jerrold/water-kiosk-production/
├── water-kiosk-hardware-server/       [ACTIVE - Requires ngrok switch]
│   ├── water_kiosk_hardware_server.py
│   └── README.md
│
└── water-kiosk-sms-server/            [ARCHIVED - Functionality in at_server.py]
    ├── water_kiosk_sms_server.py
    └── README.md

/home/jerrold/Tusafishe/functions/
├── water-kiosk-hardware-function/     [ARCHIVED - Not deployed]
│   └── src/main.py
│
└── water-kiosk-sms-function/          [ARCHIVED - Not deployed]
    └── src/main.py
```

---

## Development vs Production Comparison

| Aspect | Current (Home) | Production (Data Center) |
|--------|---|---|
| **USSD/SMS Server** | Port 5000, ngrok tunnel | Port 5000, public IP |
| **Hardware Server** | Port 8080, requires ngrok switch | Port 8080, public IP (simultaneous) |
| **Appwrite** | Local docker-compose | Dedicated instance/service |
| **SSL/TLS** | None (ngrok handled) | Required |
| **Simultaneous Services** | Only one external | Both services at once |
| **Scalability** | Single home server | Can scale horizontally |
| **Backup** | Manual | Automated |
| **Monitoring** | None | Required |

---

## Key Dependencies & Credentials

⚠️ **All servers use the same Appwrite project:**
- Project ID: `689107c288885e90c039`
- Database ID: `6864aed388d20c69a461`
- API Key: (hardcoded in servers, should be environment variables)

⚠️ **SMS/Payment Services:**
- Africa's Talking API Key (in at_server.py)
- MTN MoMo credentials (in start_server_with_mtn.sh)
- Airtel Money credentials (in at_server.py)

**Security Note**: Credentials should be moved to environment variables before production deployment.

---

## Quick Start Guide

### Launch Full System (Home Server)

```bash
# 1. Start Appwrite
cd ~/appwrite
./start.sh  # or: docker-compose up -d

# 2. Start USSD/SMS Server
cd ~/cloud_server/water-kiosk-ussd-server
./start_server_with_mtn.sh

# 3. Start ngrok tunnel
ngrok start ussd  # Configured in ~/.config/ngrok/ngrok.yml

# 4. (Optional) Start Analytics Dashboard
cd ~/cloud_server/water-kiosk-analytics
./start_analytics.sh

# 5. (Optional) Start Customer Dashboard
cd ~/cloud_server/water-kiosk-dashboard
./start_dashboard.sh
```

### Test USSD/SMS
```bash
curl -X POST https://first-many-snake.ngrok-free.app/ \
  -d "sessionId=123&serviceCode=*123#&phoneNumber=+254700000000&text="
```

### Test Hardware Server (Requires ngrok switch)
```bash
# Stop current ngrok tunnel
# Update ngrok.yml to expose port 8080
# Restart ngrok

curl -X POST https://first-many-snake.ngrok-free.app/dispense-verification \
  -H "Content-Type: application/json" \
  -d '{"kiosk_id":"KIOSK001","user_id":"+254700000000","pin":"1234","volume_ml":500}'
```

### ngrok Commands Reference

#### Start ngrok with configured tunnel (Recommended)
```bash
# Starts the 'ussd' tunnel configured in ~/.config/ngrok/ngrok.yml
# This exposes port 5000 to first-many-snake.ngrok-free.app
ngrok start ussd
```

#### Start ngrok with quick tunnel (Alternative)
```bash
# Starts an unnamed tunnel on port 5000
# Generates a random ngrok URL
ngrok http 5000
```

#### Switch to Hardware Server Testing
```bash
# 1. Stop current ngrok tunnel (Ctrl+C in ngrok terminal)
# 2. Edit ngrok configuration
nano ~/.config/ngrok/ngrok.yml

# 3. Change the tunnel configuration:
# From:
#   addr: 5000
# To:
#   addr: 8080

# 4. Restart ngrok
ngrok start ussd

# 5. Note the new ngrok URL and update any external configurations
```

#### Verify ngrok is working
```bash
# Test the tunnel from another terminal
curl https://first-many-snake.ngrok-free.app/

# Expected response: Status page from your running server (JSON)
```

#### ngrok Configuration File
Located at: `~/.config/ngrok/ngrok.yml`

Current configuration:
```yaml
version: "2"
authtoken: 31ZHaP8AMQieC1bVwW163tByBaq_3nu7JYfVeYszkcFaodspw

tunnels:
  ussd:
    proto: http
    addr: 5000                    # Currently: USSD/SMS Server
    domain: first-many-snake.ngrok-free.app
```

To switch to hardware testing, change `addr: 5000` to `addr: 8080`

#### Troubleshooting ngrok

**"ngrok command not found"**
- Install ngrok: Download from https://ngrok.com
- Make sure it's in your PATH

**"Port already in use"**
- Check what's using port 5000: `lsof -i :5000`
- Kill the process: `kill -9 <PID>`
- Or use a different port

**"Auth token expired"**
- Get new token from ngrok dashboard
- Update authtoken in `~/.config/ngrok/ngrok.yml`

**No external access to server**
- Verify ngrok is running: `ngrok start ussd`
- Check ngrok status at: https://localhost:4040 (local dashboard)
- Verify backend server is running on correct port

---

## Recommendations

### Immediate Actions
1. ✅ Archive Appwrite Functions (not needed)
2. ✅ Move credentials to environment variables
3. ✅ Document all ngrok tunnel configurations
4. ✅ Create backup of customer database

### Before Data Center Migration
1. Implement proper logging/monitoring
2. Set up automated backups
3. Add SSL/TLS certificates
4. Performance test at scale (600+ kiosks)
5. Implement rate limiting/API throttling
6. Add comprehensive error handling
7. Create deployment automation (Docker)

### Long-term
1. Microservices architecture (if needed)
2. Caching layer (Redis)
3. Message queue (for async operations)
4. CDN for static assets
5. Advanced analytics/reporting

---

## Contact & Support

For questions about this architecture:
- Review the individual README.md files in each project
- Check git history for development decisions
- Reference the PDF documentation files in the function folders

---

**Last Updated**: November 9, 2024
**Status**: Home Server with ngrok (development/testing phase)
**Next Phase**: Data Center Migration
