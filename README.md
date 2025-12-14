# 🍬 Sweet Shop Management System

A full-stack web application for managing a sweet shop, built with **Python/FastAPI** backend and **React/TypeScript** frontend following **Test-Driven Development (TDD)** principles.

## 📋 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [My AI Usage](#my-ai-usage)

## ✨ Features

### Backend API
- ✅ User authentication with JWT tokens
- ✅ Role-based access control (User/Admin)
- ✅ Complete CRUD operations for sweets
- ✅ Advanced search functionality (name, category, price range)
- ✅ Inventory management (purchase/restock)
- ✅ MongoDB database integration
- ✅ Comprehensive test suite (19 tests, 100% passing)

### Frontend Application
- ✅ Modern, responsive UI with gradient designs
- ✅ User registration and login
- ✅ Dashboard with sweets display
- ✅ Search and filter functionality
- ✅ Purchase sweets with quantity selector
- ✅ Admin panel for managing sweets
- ✅ Protected routes with authentication

## 🛠️ Technology Stack

### Backend
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: MongoDB with Motor (async driver)
- **ODM**: Beanie
- **Authentication**: JWT (python-jose + passlib)
- **Testing**: pytest + pytest-asyncio + httpx
- **Validation**: Pydantic

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Styling**: Modern CSS with gradients and animations

## 📁 Project Structure

```
sweet-shop/
├── backend/
│   ├── app/
│   │   ├── config/         # Database configuration
│   │   ├── models/         # MongoDB document models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic
│   │   ├── middleware/     # Authentication middleware
│   │   └── utils/          # Utility functions
│   ├── tests/              # Test suite
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service layer
│   │   └── App.tsx         # Main application
│   └── package.json        # Node dependencies
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- MongoDB (running locally or remotely)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file** (copy from `.env.example`):
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=sweet_shop
   SECRET_KEY=your-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Ensure MongoDB is running** on `localhost:27017`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

## 🎯 Running the Application

### Start Backend Server

```bash
cd backend
.\venv\Scripts\python -m uvicorn app.main:app --reload
```

The backend API will be available at: **http://localhost:8000**

Interactive API documentation: **http://localhost:8000/docs**

### Start Frontend Server

```bash
cd frontend
npm run dev
```

The frontend application will be available at: **http://localhost:5173**

## 🧪 Testing

### Backend Tests

Run the complete test suite:

```bash
cd backend
.\venv\Scripts\python -m pytest tests/ -v
```

Run tests with coverage report:

```bash
.\venv\Scripts\python -m pytest tests/ --cov=app --cov-report=html --cov-report=term
```

**Test Results**: ✅ 19 tests passing

Coverage report will be generated in `backend/htmlcov/index.html`

### Test Coverage
- Authentication endpoints (register, login)
- Sweets CRUD operations
- Search functionality
- Inventory management (purchase, restock)
- Authorization (admin-only endpoints)
- Input validation

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Sweets Endpoints (Protected)

All sweets endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

#### Create Sweet
```http
POST /api/sweets
{
  "name": "Chocolate Bar",
  "category": "Chocolate",
  "price": 2.99,
  "quantity": 100,
  "description": "Delicious milk chocolate"
}
```

#### Get All Sweets
```http
GET /api/sweets
```

#### Search Sweets
```http
GET /api/sweets/search?name=Chocolate&category=Chocolate&min_price=1.0&max_price=5.0
```

#### Update Sweet
```http
PUT /api/sweets/{id}
{
  "price": 3.49,
  "quantity": 150
}
```

#### Delete Sweet (Admin Only)
```http
DELETE /api/sweets/{id}
```

#### Purchase Sweet
```http
POST /api/sweets/{id}/purchase
{
  "quantity": 10
}
```

#### Restock Sweet (Admin Only)
```http
POST /api/sweets/{id}/restock
{
  "quantity": 50
}
```

## 📸 Screenshots

### Login Page
![Login Page](screenshots/login_page.png)

### Register Page
![Register Page](screenshots/register_page.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Admin Panel
![Admin Panel](screenshots/admin_panel.png)

## 🤖 My AI Usage

### AI Tools Used
I used **Google Gemini AI** (Antigravity Agent) extensively throughout this project to accelerate development while maintaining code quality and following best practices.

### How AI Was Leveraged

#### 1. **Project Planning & Architecture**
- **What AI Did**: Helped design the overall system architecture, database schema, and API endpoint structure
- **My Role**: Reviewed and approved the architecture, ensuring it met all kata requirements
- **Impact**: Saved significant time in planning phase while ensuring a solid foundation

#### 2. **Test-Driven Development**
- **What AI Did**: Generated comprehensive test cases following the RED-GREEN-REFACTOR pattern
- **My Role**: Verified test coverage and ensured tests were meaningful, not just achieving coverage numbers
- **Impact**: Achieved 100% test pass rate with 19 comprehensive tests covering all functionality

#### 3. **Backend Implementation**
- **What AI Did**: 
  - Created FastAPI application structure with proper separation of concerns
  - Implemented MongoDB models using Beanie ODM
  - Built authentication system with JWT
  - Developed all CRUD endpoints with proper validation
  - Created search functionality with MongoDB queries
- **My Role**: Reviewed code for security issues, validated business logic, ensured proper error handling
- **Impact**: Rapid development of a production-ready backend with clean, maintainable code

#### 4. **Frontend Development**
- **What AI Did**:
  - Built React components with TypeScript
  - Created modern, responsive UI with CSS gradients and animations
  - Implemented React Router with protected routes
  - Developed AuthContext for state management
  - Created API service layer with axios interceptors
- **My Role**: Ensured UI/UX met modern standards, validated accessibility, tested user flows
- **Impact**: Professional-looking application with smooth user experience

#### 5. **Debugging & Problem Solving**
- **What AI Did**: Identified and fixed issues like:
  - bcrypt compatibility problems (downgraded to v4.x)
  - pytest async configuration issues
  - HTTP status code mismatches in tests
- **My Role**: Verified fixes worked correctly, understood root causes
- **Impact**: Quick resolution of technical issues that could have taken hours to debug manually

#### 6. **Documentation**
- **What AI Did**: Generated comprehensive README, API documentation, and code comments
- **My Role**: Reviewed for accuracy, added project-specific details
- **Impact**: Professional documentation ready for review

### Reflection on AI Impact

**Positive Impacts**:
- **Speed**: What would typically take 2-3 days was completed in a few hours
- **Quality**: AI helped maintain consistent code style and best practices
- **Learning**: Exposed me to modern patterns and libraries I might not have discovered
- **Testing**: Comprehensive test coverage from the start, not as an afterthought

**Challenges**:
- **Verification**: Had to carefully review all AI-generated code for correctness
- **Understanding**: Needed to understand every line of code, not just copy-paste
- **Customization**: Some AI suggestions needed modification to fit specific requirements

**Best Practices I Followed**:
1. ✅ Always reviewed and understood AI-generated code
2. ✅ Tested everything thoroughly (all 19 tests passing)
3. ✅ Made modifications where AI suggestions weren't optimal
4. ✅ Used AI as a tool to accelerate, not replace, my development process
5. ✅ Documented AI usage transparently in commits and this README

### Commit History with AI Co-authorship

All commits where AI was used include proper co-authorship attribution:
```
Co-authored-by: Gemini AI <gemini@users.noreply.github.com>
```

This can be verified in the git history:
```bash
git log --pretty=format:"%h %s %b"
```

## 🎓 Learning Outcomes

Through this project with AI assistance, I:
- Deepened understanding of TDD principles and their practical application
- Learned FastAPI and its async capabilities
- Gained experience with MongoDB and Beanie ODM
- Improved React/TypeScript skills
- Understood the importance of proper authentication and authorization
- Learned to effectively collaborate with AI tools while maintaining code ownership

## 📝 License

This project was created as part of a technical assessment kata.

---

**Built with ❤️ using TDD principles and AI assistance**
