# Water Kiosk Customer Dashboard

A working example dashboard that demonstrates the **Appwrite Proxy Server Pattern** - perfect for learning how to access Appwrite databases securely without exposing API keys.

## What Makes This Special 🎯

This dashboard shows you exactly how to:
- Access Appwrite without using the Appwrite SDK
- Use simple `fetch()` calls instead
- Never handle or see the API key
- Filter data on the client side
- Build a real dashboard that works with the proxy server

It's ready to use and fully functional!

## Quick Start

### For Students (What You Need to Do)

If Jerrold is hosting the proxy server, you just need to:

```bash
git clone https://github.com/JerroldMitchell/water-kiosk-dashboard.git
cd water-kiosk-dashboard
python3 serve_dashboard.py
```

Then visit: **http://localhost:8080/customer-dashboard.html**

Done! The dashboard automatically connects to Jerrold's proxy server via ngrok.

### For Jerrold (Full Setup if Running Everything)

If you're setting this up from scratch:

**1. Start the Proxy Server**
```bash
cd /home/jerrold/cloud_server/proxy_server
./start_proxy.sh
```

**2. Start ngrok**
```bash
ngrok start proxy
```

**3. Start the Dashboard Server**
```bash
cd /home/jerrold/cloud_server/water-kiosk-dashboard
python3 serve_dashboard.py
```

Visit: **http://localhost:8080/customer-dashboard.html**

## How It Works (The Proxy Pattern)

```
┌─────────────────┐
│   Your Browser  │
│   (Dashboard)   │
└────────┬────────┘
         │ fetch()
         ↓
┌─────────────────────────┐
│   Proxy Server (3000)   │ ← Adds X-Appwrite-Key
│   (Flask app)           │   Restricts collections
└────────┬────────────────┘
         │ HTTP
         ↓
┌─────────────────┐
│    Appwrite     │
│   (Database)    │
└─────────────────┘
```

## The Key Code Pattern

This is the core pattern used throughout the dashboard:

```javascript
// Configuration
const PROXY_ENDPOINT = 'https://first-many-snake.ngrok-free.app';
const DATABASE_ID = '6864aed388d20c69a461';
const COLLECTION_ID = 'customers';

// Fetch function - NO authentication headers needed!
async function fetchAllCustomers() {
    const url = `${PROXY_ENDPOINT}/v1/databases/${DATABASE_ID}/collections/${COLLECTION_ID}/documents`;
    const response = await fetch(url);
    const data = await response.json();
    return data.documents; // Array of customer objects
}

// Filter on client side (proxy doesn't support queries)
async function searchByPhone(phone) {
    const allCustomers = await fetchAllCustomers();
    return allCustomers.filter(c => c.phone_number === phone);
}
```

## File Structure

```
water-kiosk-dashboard/
├── customer-dashboard.html      # Main dashboard (this is what you see)
├── serve_dashboard.py           # HTTP server to serve the dashboard
├── DASHBOARD_README.md          # This file
└── ARCHITECTURE.md              # System architecture docs
```

## Features Shown

✅ **Statistics Display** - Shows total, active, registered, unregistered customers
✅ **Search by Phone** - Exact match or wildcard search (*suffix)
✅ **Search by Account ID** - Find customers by their account ID
✅ **Real Data** - Connected to the actual Appwrite database via proxy
✅ **Clean UI** - Responsive dashboard with nice styling
✅ **Error Handling** - Graceful errors and loading states

## Adapting For Your Own Project

Want to use this pattern in your own project? Here's what to change:

### 1. Change the Proxy Endpoint

```javascript
// Instead of: https://first-many-snake.ngrok-free.app
// Use: https://your-ngrok-domain.ngrok-free.app
const PROXY_ENDPOINT = 'https://your-domain.ngrok-free.app';
```

### 2. Change the Database/Collection IDs

```javascript
const DATABASE_ID = 'your-database-id';
const COLLECTION_ID = 'your-collection-name';
```

### 3. Fetch from Your Collections

```javascript
// Same pattern - fetch from proxy!
const url = `${PROXY_ENDPOINT}/v1/databases/${DATABASE_ID}/collections/${COLLECTION_ID}/documents`;
const response = await fetch(url);
const data = await response.json();
```

## Performance Notes

⚠️ **Client-Side Filtering**

The current implementation fetches ALL documents and filters on the client side. This works great for small datasets (100-1000 items) but for larger databases, consider:

1. Adding query support to the proxy server
2. Implementing pagination
3. Adding search/filter endpoints to the proxy

For now, this approach keeps things simple and demonstrates the core pattern!

## Troubleshooting

### "Connection refused"
- Make sure proxy server is running on port 3000
- Check ngrok is active and the URL is correct

### "CORS errors"
- The proxy server should handle CORS automatically
- If you're getting CORS errors, check the proxy server logs

### "No customers showing"
- Make sure Appwrite is running
- Check that the ngrok tunnel is active
- Verify the database and collection IDs are correct

### "Dashboard is slow"
- You're probably fetching many documents
- Consider implementing pagination in the proxy

## Student Project Ideas

Now that you have a working example, try building:

- 📱 A customer support chat interface
- 📊 Advanced analytics dashboard
- 🔍 A CRM system for managing customers
- 💰 A billing/payments dashboard
- 📞 A call log management system

All using the same proxy pattern!

## Learning Resources

- **STUDENT_GUIDE.md** - How to use the proxy from curl/code
- **proxy_server/README.md** - How the proxy works
- **This file** - How to build dashboards with the proxy pattern

## Questions?

- Review the comments in `customer-dashboard.html` - they explain the proxy pattern
- Check the proxy server documentation
- Look at the STUDENT_GUIDE for API examples

Happy building! 🚀
