# Topic 5: Capstone - Journal API

Welcome to your Python capstone project! You'll be working with a **FastAPI + PostgreSQL** application that helps people track their daily learning journey. This will prepare you for deploying to the cloud in the next phase.

By the end of this capstone, your API should be working locally and ready for cloud deployment.

## 🚀 Getting Started

### Prerequisites

- Git installed on your machine
- Docker Desktop installed and running
- VS Code with the Dev Containers extension

### 1. Fork and Clone the Repository

1. **Fork this repository** to your GitHub account by clicking the "Fork" button
2. **Clone your fork** to your local machine:

   ```bash
   git clone https://github.com/YOUR_USERNAME/journal-starter.git
   cd journal-starter
   ```

3. **Open in VS Code**:

   ```bash
   code .
   ```

### 2. Set Up Your Development Environment

1. **Install the Dev Containers extension** in VS Code (if not already installed)
2. **Reopen in container**: When VS Code detects the `.devcontainer` folder, click "Reopen in Container"
   - Or use Command Palette (`Cmd/Ctrl + Shift + P`): `Dev Containers: Reopen in Container`
3. **Wait for setup**: The container will automatically install Python, dependencies, and configure your environment

### 3. Start PostgreSQL Database

1. **Start the database** (run this in the VS Code terminal inside the dev container):

   ```bash
   docker-compose up -d postgres
   ```

2. **Verify it's running**:

   ```bash
   docker-compose ps
   ```

   You should see the postgres service running.

### 4. Verify Environment Configuration

The `.env` file is already provided and configured for you! It contains:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/career_journal
```

This connects to the PostgreSQL container you just started.

### 5. Run the API

```bash
# From the project root (should already be your current directory)
./start.sh
```

### 6. Test Everything Works! 🎉

1. **Visit the API docs**: http://localhost:8000/docs
2. **Try the working endpoints**:
   - POST `/entries` - Create a new journal entry
   - GET `/entries` - View all your journal entries
   - PATCH `/entries/{id}` - Update an entry
   - DELETE `/entries` - Delete all entries

3. **Create your first entry** using the docs interface to make sure everything is connected!
4. **View your entries** using the GET `/entries` endpoint to see what you've created!

**🎯 Once you can create and see entries, you're ready to start implementing the missing endpoints!**

## 🔧 Troubleshooting

**If the API won't start:**
- Make sure the PostgreSQL container is running: `docker-compose ps`
- Check the container logs: `docker-compose logs postgres`
- Restart the database: `docker-compose restart postgres`

**If you can't connect to the database:**
- Verify the `.env` file exists and has the correct DATABASE_URL
- Make sure Docker Desktop is running
- Try restarting the dev container: `Dev Containers: Rebuild Container`

**If the dev container won't open:**
- Ensure Docker Desktop is running
- Install the "Dev Containers" extension in VS Code
- Try: `Dev Containers: Rebuild and Reopen in Container`

## 🗄️ Explore Your Database (Optional)

Want to see your data directly in the database? You can connect to PostgreSQL using VS Code's PostgreSQL extension:

### 1. Install PostgreSQL Extension

1. **Install the PostgreSQL extension** in VS Code (search for "PostgreSQL" by Chris Kolkman)
2. **Restart VS Code** after installation

### 2. Connect to Your Database
1. **Open the PostgreSQL extension** (click the PostgreSQL icon in the sidebar)
2. **Click "Add Connection"** or the "+" button
3. **Enter these connection details**:
   - **Server name**: `localhost`
   - **Authentication Type**: `Password`
   - **User name**: `postgres`
   - **Password**: `postgres`
   - **Database name**: `career_journal`
   - **Connection Name**: `Journal Starter DB` (or any name you prefer)
   - **Save Password**: ✅ Check this for convenience

4. **Click "Test Connection"** to verify it works
5. **Click "Save & Connect"**

### 3. Explore Your Data
1. **Expand your connection** in the PostgreSQL panel
2. **Right-click on "Journal Starter DB"** → **Expand**
3. **Right-click on "career_journal"** database
4. **Select "New Query"**
5. **Type this query** to see all your entries:
   ```sql
   SELECT * FROM entries;
   ```
6. **Run the query** (Ctrl/Cmd + Enter) to see all your journal data!

You can now explore the database structure, see exactly how your data is stored, and run custom queries to understand PostgreSQL better.

## Project Structure

This project uses a clean FastAPI architecture with PostgreSQL:

```
api/
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Python dependencies  
├── models/
│   └── entry.py              # Pydantic data models
├── repositories/
│   ├── interface_repository.py    # Database interface
│   └── postgres_repository.py     # PostgreSQL implementation
├── routers/
│   └── journal_router.py     # API endpoints (YOUR MAIN WORK HERE)
└── services/
    └── entry_service.py      # Business logic layer
```

## Your Learning Goals

Complete a Journal API that allows users to:
- ✅ **Store journal entries** (already implemented)
- ✅ **Retrieve all journal entries** (already implemented) 
- ❌ **Retrieve single journal entry** (you need to implement)  
- ❌ **Delete specific journal entries** (you need to implement)
- ✅ **Update journal entries** (already implemented)
- ✅ **Delete all entries** (already implemented)
- ❌ **Setup logging** (you need to implement)

## 🎯 Development Tasks (Your Work!)

### 1. API Implementation (Required)
**File: `api/routers/journal_router.py`**

Implement these missing endpoints:
- [ ] **GET /entries/{entry_id}** - Get single entry by ID  
- [ ] **DELETE /entries/{entry_id}** - Delete specific entry

Each endpoint has detailed TODO comments with step-by-step guidance!

### 2. Logging Setup (Required)
**File: `api/main.py`**

- [ ] Configure basic logging using `logging.basicConfig()`
- [ ] Set logging level to INFO
- [ ] Add console handler
- [ ] Test with a startup log message

### 3. Data Model Improvements (Optional)
**File: `api/models/entry.py`**

- [ ] Add custom field validators (e.g., minimum length)
- [ ] Add data sanitization methods
- [ ] Add schema version tracking

### 4. Cloud CLI Setup (Required for Deployment)
**File: `.devcontainer/devcontainer.json`**

- [ ] Choose and uncomment ONE cloud CLI tool:
  - Azure CLI: `"ghcr.io/devcontainers/features/azure-cli:1": {}`
  - AWS CLI: `"ghcr.io/devcontainers/features/aws-cli:1": {}`  
  - Google Cloud CLI: `"ghcr.io/devcontainers/features/gcloud:1": {}`

## 📊 Data Schema

Each journal entry follows this structure:

| Field       | Type      | Description                                | Validation                   |
|-------------|-----------|--------------------------------------------|------------------------------|
| id          | string    | Unique identifier (UUID)                   | Auto-generated               |
| work        | string    | What did you work on today?                | Required, max 256 characters |
| struggle    | string    | What's one thing you struggled with today? | Required, max 256 characters |
| intention   | string    | What will you study/work on tomorrow?      | Required, max 256 characters |
| created_at  | datetime  | When entry was created                     | Auto-generated UTC           |
| updated_at  | datetime  | When entry was last updated                | Auto-updated UTC             |

## 🔌 API Endpoints

| Method | Endpoint           | Status | Description                    |
|--------|--------------------|--------|--------------------------------|
| POST   | /entries           | ✅ Done | Create new journal entry       |
| GET    | /entries           | ✅ Done | List all journal entries       |
| GET    | /entries/{id}      | ❌ TODO | Get single entry by ID         |
| PATCH  | /entries/{id}      | ✅ Done | Update existing entry          |
| DELETE | /entries/{id}      | ❌ TODO | Delete specific entry          |
| DELETE | /entries           | ✅ Done | Delete all entries             |

## ✅ How to Complete This Project

1. **Start by running the existing API** - make sure it works
2. **Study the working endpoints** - understand the patterns
3. **Implement missing endpoints one by one** - follow the TODO comments
4. **Test each endpoint** - use the /docs page to test
5. **Add logging** - see your API in action
6. **Choose a cloud CLI** - prepare for deployment

## 🎓 Skills You'll Practice

### FastAPI & Python
- **RESTful API design** - HTTP methods, status codes, JSON responses
- **Async programming** - using `async`/`await` with databases
- **Dependency injection** - using FastAPI's `Depends()` 
- **Error handling** - proper HTTP exceptions and status codes
- **Data validation** - Pydantic models and field validation
- **Project structure** - organizing code with routers, services, repositories

### Database Integration  
- **PostgreSQL** - connecting and querying with asyncpg
- **Repository pattern** - abstracting database operations
- **JSON storage** - storing structured data in JSONB fields

### Development Practices
- **Environment configuration** - using .env files
- **Logging** - tracking application behavior
- **API documentation** - FastAPI's automatic OpenAPI docs
- **Error handling** - graceful failure and user feedback
