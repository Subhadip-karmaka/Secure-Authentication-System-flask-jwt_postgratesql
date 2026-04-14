# Secure Authentication System 🔐

A secure user authentication system built using Flask, JWT, bcrypt, and PostgreSQL.  
This project provides secure user registration, login, token-based authentication, and session management for modern web applications.

---

## 🚀 Features

- User Registration with Password Hashing (bcrypt)
- Secure Login Authentication
- JWT Token Generation & Verification
- Protected Routes using JWT Authentication
- PostgreSQL Database Integration
- Password Encryption & Secure Storage
- Session Management with Token Expiry
- RESTful API Structure

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Authentication:** PyJWT / Flask-JWT-Extended
- **Security:** bcrypt
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (if used)

---

## 📂 Project Structure

```bash
secure-auth-system-flask-jwt/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── models/
│   └── user_model.py
├── routes/
│   └── auth_routes.py
├── utils/
│   └── jwt_handler.py
└── README.md
```

## 🔐 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | /register | Register New User |
| POST | /login | User Login |
| GET | /protected | Protected Route |
| POST | /logout | Logout User |

---

## 📸 Sample JWT Authentication Flow

1. User Registers  
2. Password Stored as bcrypt Hash  
3. User Logs In  
4. JWT Token Generated  
5. Token Used to Access Protected Routes  

---

## 🎯 Learning Outcomes

- Implemented secure authentication best practices  
- Learned JWT-based stateless authentication  
- Applied password hashing & encryption  
- Integrated PostgreSQL with Flask backend  
- Built secure REST APIs  

---

## 📌 Future Improvements

- Refresh Tokens
- Role-Based Access Control
- Email Verification
- Password Reset Functionality
- Docker Deployment

---

## 👨‍💻 Author

**SUBHADIP KARMAKAR**

## ⭐ If you found this project useful, give it a star!
