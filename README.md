# Secure Authentication System (Flask + PostgreSQL)

This backend implements:
- Secure user registration with `bcrypt` password hashing
- JWT-based authentication using `PyJWT`
- Session invalidation via token blacklist (`logout`)
- PostgreSQL persistence with connection pooling
- Controlled CORS for frontend integration

## 1. Project Structure

```text
D:\Authentication System
|-- app
|   |-- __init__.py
|   |-- auth.py
|   |-- config.py
|   |-- db.py
|   `-- security.py
|-- .env.example
|-- requirements.txt
|-- run.py
`-- schema.sql
```

## 2. PostgreSQL Setup (Detailed)

1. Install PostgreSQL and ensure server is running on `localhost:5432`.
2. Open `psql` and run:

```sql
CREATE DATABASE auth_system;
\c auth_system
\i schema.sql
```

3. Confirm tables:

```sql
\dt
SELECT * FROM users;
SELECT * FROM token_blacklist;
```

4. Copy `.env.example` to `.env` and update DB credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_system
DB_USER=postgres
DB_PASSWORD=your_password
```

## 3. Backend Setup (Anaconda)

1. Open **Anaconda Prompt** in project folder and create the environment:

```powershell
conda env create -f environment.yml
```

2. Activate environment:

```powershell
conda activate secure-auth-system
```

3. Create `.env` from `.env.example`, then set:
- `JWT_SECRET_KEY` to a strong random string
- `CORS_ALLOWED_ORIGINS` to your frontend URL(s)
- `HOST=0.0.0.0` (already in example) so backend is reachable on your network

4. Run server:

```powershell
python run.py
```

API base URL: `http://localhost:5000`

## 3.1 React Frontend Setup

1. Open a second terminal and move to frontend:

```powershell
cd frontend
```

2. Install node packages:

```powershell
npm install
```

3. Create frontend `.env` from `frontend/.env.example`:

```env
VITE_API_BASE_URL=http://127.0.0.1:5000
```

4. Start React app:

```powershell
npm run dev
```

Frontend URL: `http://localhost:5173`

## 4. API Endpoints

### Health Check
- `GET /api/health`

### Register
- `POST /api/auth/register`
- Body:

```json
{
  "email": "user@example.com",
  "password": "StrongPass123"
}
```

### Login
- `POST /api/auth/login`
- Body:

```json
{
  "email": "user@example.com",
  "password": "StrongPass123"
}
```

Returns JWT access token.

### Get Current User
- `GET /api/auth/me`
- Header:

```text
Authorization: Bearer <access_token>
```

### Logout (Token Revocation)
- `POST /api/auth/logout`
- Header:

```text
Authorization: Bearer <access_token>
```

## 5. CORS Policy (Important)

Configured in `app/__init__.py`:
- Only routes matching `/api/*` allow CORS.
- Allowed origins come from `CORS_ALLOWED_ORIGINS`.
- Only headers: `Authorization`, `Content-Type`.
- Only methods: `GET`, `POST`, `OPTIONS`.

For multiple frontend clients:

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000
```

## 6. Networking Protocols for Seamless Experience

- Use `HTTPS` in production so JWT tokens and credentials are encrypted in transit (TLS).
- API communication pattern:
  - Browser sends CORS preflight `OPTIONS` when required.
  - Backend responds with allowed origin/method/headers.
  - Browser proceeds with actual `POST`/`GET`.
- Keep JWT short-lived (`JWT_ACCESS_TOKEN_MINUTES=15`) to reduce risk.
- Use reverse proxy (Nginx) for:
  - TLS termination
  - Rate limiting
  - Request timeout control
- Recommended HTTP status usage:
  - `200` success
  - `201` created
  - `400` bad request
  - `401` unauthorized
  - `404` not found
  - `409` conflict (duplicate email)
  - `500` internal server error

## 6.1 Make It "Global" (Reachable Outside Your Machine)

- Current code already supports this by binding Flask host via `.env`:

```env
HOST=0.0.0.0
PORT=5000
```

- For same Wi-Fi/LAN devices, use your machine IP:
  - Example: `http://192.168.1.20:5000`
- Allow inbound firewall rule for port `5000` on Windows.
- Keep CORS strict with exact frontend origins. Do not use `*` for authenticated APIs.
- For internet-wide access, place app behind reverse proxy + HTTPS and deploy to cloud VM/container.

## 7. Quick Test with curl

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"StrongPass123"}'
```

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"StrongPass123"}'
```

Use returned token:

```bash
curl http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer <token>"
```

## 8. Security Notes for Internship Demo

- Passwords are never stored in plain text (`bcrypt` hash only).
- JWT signature prevents token tampering.
- Blacklist table revokes used tokens on logout.
- CORS whitelist reduces cross-origin abuse.
- Database queries use parameterized SQL to prevent injection.

---

If you want, next we can add:
1. Refresh tokens
2. Email verification
3. Rate limiting and login lockout
4. Docker setup for Flask + PostgreSQL
