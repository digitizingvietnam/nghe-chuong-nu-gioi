# API Documentation

## Base URL

```
http://localhost:7070
```

## Endpoints

### 1. Get Homepage

```http
GET /
```

**Description**: Serves the chatbot web interface

**Response**: HTML page (index.html)

---

### 2. Query RAG System

```http
POST /api/query
```

**Description**: Send a query to the RAG chatbot and get a response

**Request Body**:

```json
{
  "query_text": "Giáo dục phụ nữ quan trọng như thế nào?"
}
```

**Success Response** (200):

```json
{
  "response": "Giáo dục phụ nữ giữ vai trò vô cùng quan trọng. Trước hết, như tác giả Nữ-sanh Thu-cúc đã nhấn mạnh..."
}
```

**Error Response** (400):

```json
{
  "error": "Missing 'query_text' in request body"
}
```

---

### 3. Health Check

```http
GET /health
```

**Description**: Check if the server is running

**Response** (200):

```json
{
  "status": "healthy",
  "message": "Server is running fine!"
}
```

---

### 4. Get Sample Quotes

```http
GET /api/quotes
```

**Description**: Retrieve sample historical quotes from Nữ Giới Chung for frontend display/animation

**Response** (200):

```json
["..."]
```

**Note**: Returns first 10 entries from the CSV file
