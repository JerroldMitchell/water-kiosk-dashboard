# Appwrite Database Access Guide 🚀

Hey team! Welcome to the Water Kiosk project! This guide will get you up and running with the database in about 2 minutes.

## Quick Start

### 1. You're All Set!

Here's your endpoint URL:
```
https://first-many-snake.ngrok-free.app
```

(Yes, that weird ngrok URL is actually how we tunnel through the ISP restrictions. It's working though!)

### 2. Test Your Connection

Open a terminal and run this to make sure you can access the database:
```bash
curl https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents
```

You should get back a bunch of customer data in JSON. If it works, you're good to go! 🎉

## CRUD Operations

Here are some real examples you can copy-paste directly. Just replace `DOCUMENT_ID` with an actual customer ID from your data.

### 1. CREATE - Add a New Customer

```bash
curl -X POST https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents \
  -H "Content-Type: application/json" \
  -d '{
    "documentId": "unique()",
    "data": {
      "phone_number": "+254700000123",
      "pin": "1234",
      "full_name": "Jane Smith",
      "is_registered": true,
      "active": true,
      "credits": 100,
      "account_id": "TSF123456"
    }
  }'
```

**Response:** You'll get back the new customer with a unique ID assigned.

### 2. READ - Get All Customers

```bash
curl https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents
```

**Response:** A JSON list with all your customers.

⚠️ **Important: Appwrite Pagination Limit**

Appwrite returns a **maximum of 25 documents per request**, even if you have more in the database. The response includes a `total` field showing the actual total count, but only 25 documents in the `documents` array.

**Check total count:**
```bash
curl https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents \
  | jq '.total'  # Shows actual total, e.g., 50
```

**Fetch all customers using pagination:**

```bash
# Fetch batch 1 (documents 0-24)
curl 'https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents?limit=25&offset=0'

# Fetch batch 2 (documents 25-49)
curl 'https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents?limit=25&offset=25'

# Fetch batch 3 (documents 50-74)
curl 'https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents?limit=25&offset=50'
```

**JavaScript example with pagination:**
```javascript
async function fetchAllCustomers() {
  const endpoint = 'https://first-many-snake.ngrok-free.app';
  const dbId = '6864aed388d20c69a461';
  const collectionId = 'customers';

  let allDocuments = [];
  let offset = 0;
  const limit = 25;
  let total = null;

  while (true) {
    const url = `${endpoint}/v1/databases/${dbId}/collections/${collectionId}/documents?limit=${limit}&offset=${offset}`;
    const response = await fetch(url);
    const data = await response.json();

    // Store total on first request
    if (total === null) total = data.total;

    // Add this batch to our collection
    allDocuments = allDocuments.concat(data.documents || []);

    // Stop if we have all documents
    if (allDocuments.length >= total || (data.documents || []).length === 0) break;

    offset += limit;
  }

  return allDocuments; // Now contains ALL customers
}
```

### 3. READ - Get a Specific Customer

Already have a customer ID? Grab just that one:

```bash
curl https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID
```

Just swap in the actual ID. For example:
```bash
curl https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents/66a1234567890abcdef123
```

### 4. UPDATE - Modify a Customer

Change whatever you want - credits, name, status, whatever:

```bash
curl -X PATCH https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "credits": 50,
      "active": false,
      "full_name": "Jane Doe Updated"
    }
  }'
```

Pro tip: You only need to include the fields you actually want to change. Leave out the rest!

### 5. DELETE - Remove a Customer

```bash
curl -X DELETE https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID
```

## Customer Fields Reference

When creating or updating customers, you can use these fields:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `phone_number` | String | `"+254700000123"` | **Required for creation** |
| `pin` | String | `"1234"` | 4-digit PIN for kiosk access |
| `full_name` | String | `"John Doe"` | Customer's name |
| `is_registered` | Boolean | `true` | Registration completion status |
| `active` | Boolean | `true` | Current subscription status |
| `credits` | Integer | `100` | Water credits balance |
| `account_id` | String | `"TSF123456"` | Generated account identifier |
| `created_at` | String | ISO timestamp | Auto-generated |
| `registration_state` | String | `"completed"` | Current registration step |

## Using in Your Code

Copy-paste friendly examples for your favorite language:

### JavaScript/Node.js Example

```javascript
const endpoint = 'https://first-many-snake.ngrok-free.app';
const dbId = '6864aed388d20c69a461';
const collectionId = 'customers';

// Get all customers
fetch(`${endpoint}/v1/databases/${dbId}/collections/${collectionId}/documents`)
  .then(response => response.json())
  .then(data => console.log(data));

// Create a customer
fetch(`${endpoint}/v1/databases/${dbId}/collections/${collectionId}/documents`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    documentId: 'unique()',
    data: {
      phone_number: '+254700000123',
      pin: '1234',
      full_name: 'Student Test',
      is_registered: true,
      active: true
    }
  })
})
.then(response => response.json())
.then(data => console.log('Created:', data));
```

### Python Example

```python
import requests
import json

endpoint = 'https://first-many-snake.ngrok-free.app'
db_id = '6864aed388d20c69a461'
collection_id = 'customers'

# Get all customers
url = f'{endpoint}/v1/databases/{db_id}/collections/{collection_id}/documents'
response = requests.get(url)
print(response.json())

# Create a customer
headers = {'Content-Type': 'application/json'}
data = {
    'documentId': 'unique()',
    'data': {
        'phone_number': '+254700000456',
        'pin': '5678',
        'full_name': 'Another Student',
        'is_registered': True,
        'active': True
    }
}
response = requests.post(url, headers=headers, json=data)
print('Created:', response.json())
```

### React Example

Perfect for building the dashboard UI:

```javascript
import { useState, useEffect } from 'react';

function CustomerDashboard() {
  const [customers, setCustomers] = useState([]);
  const endpoint = 'https://first-many-snake.ngrok-free.app';
  const dbId = '6864aed388d20c69a461';
  const collectionId = 'customers';

  useEffect(() => {
    fetch(`${endpoint}/v1/databases/${dbId}/collections/${collectionId}/documents`)
      .then(res => res.json())
      .then(data => setCustomers(data.documents));
  }, []);

  return (
    <div>
      <h1>Customers: {customers.length}</h1>
      <ul>
        {customers.map(customer => (
          <li key={customer.$id}>
            {customer.full_name} ({customer.phone_number})
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Important Notes

### ✅ What You Have

- ✅ Full read/write access to the `customers` collection
- ✅ No API key needed - the proxy handles authentication
- ✅ Complete CRUD capability for database testing
- ✅ Real data that reflects actual dashboard usage

### ⚠️ What You Cannot Do

- ❌ Access other collections (only `customers` is allowed)
- ❌ Delete the database
- ❌ Access other Appwrite services
- ❌ See the actual API key (it's hidden by the proxy)

### 🔒 Security

- Your requests are proxied through a secure server
- The API key is never exposed
- All changes are logged
- The connection is encrypted (HTTPS)

## Troubleshooting

### "Connection refused"
- Make sure you're using the right endpoint: `https://first-many-snake.ngrok-free.app`
- If that still doesn't work, ngrok might have restarted and changed the URL (check with Jerrold)
- Try visiting the endpoint in your browser first to test

### "Invalid request"
- Double-check your HTTP method (GET for reading, POST for creating, PATCH for updating, DELETE for removing)
- Validate your JSON syntax - use `echo` or a JSON validator if unsure
- Make sure you're including all required fields

### "Collection not found"
- You should be using these exact values:
  - Database: `6864aed388d20c69a461`
  - Collection: `customers`
- Copy-paste them from this guide to avoid typos

### "Document not found" (when getting/updating/deleting)
- The ID you're using might not exist anymore
- Run a GET request first to see all documents and their IDs
- Document IDs show up in the `$id` field of responses

## Need Help?

- Review the CRUD operations and code examples above - most questions get answered there
- Check the DASHBOARD_README.md for more technical details
- Reach out to Jerrold on Slack or email if you hit something weird

## Common Workflows

### Workflow 1: Create Test Data

Need a bunch of fake customers to test with? This creates 3 at once:

```bash
# Create 3 test customers
for i in {1..3}; do
  curl -X POST https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents \
    -H "Content-Type: application/json" \
    -d "{
      \"documentId\": \"unique()\",
      \"data\": {
        \"phone_number\": \"+2547000001$i\",
        \"pin\": \"1234\",
        \"full_name\": \"Test Customer $i\",
        \"is_registered\": true,
        \"active\": true,
        \"credits\": 100
      }
    }"
done
```

### Workflow 2: Update Customer Status

Maybe you need to mark someone as inactive or adjust their credits:

```bash
# First, grab all customers to get an ID
curl https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents

# Then update one (copy the $id from above)
CUSTOMER_ID="66a1234567890abcdef123"
curl -X PATCH https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents/$CUSTOMER_ID \
  -H "Content-Type: application/json" \
  -d '{"data": {"active": false, "credits": 25}}'
```

### Workflow 3: Export Customer List to CSV

Want to analyze data in Excel? This downloads everything as CSV:

```bash
curl https://first-many-snake.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents \
  | jq -r '.documents[] | [.phone_number, .full_name, .credits, .active] | @csv' \
  > customers.csv
```

## You're Ready! 🎉

You've got everything you need to start building the dashboard. If anything feels unclear:
- Ping someone on the team (we're all in the same Slack)
- Check if the endpoint URL has changed (ngrok can update it sometimes)
- Review the examples above - they cover 90% of what you'll need

Happy coding! 🚀
