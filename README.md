# QueueCTL - Backend Developer Internship Assignment

QueueCTL is a simple background job queue system developed using **Python**, **FastAPI**, **SQLAlchemy**, and **MySQL**. The project is designed to manage background jobs, process them using worker processes, automatically retry failed jobs with exponential backoff, and move permanently failed jobs to a Dead Letter Queue (DLQ).

The main objective of this project is to simulate how production job queue systems work while keeping the implementation clean and easy to understand.

---

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Typer (CLI)
- Uvicorn

---

# Features

- Add new background jobs
- Process jobs using worker processes
- Store all jobs permanently in MySQL
- Retry failed jobs automatically
- Exponential backoff between retries
- Dead Letter Queue (DLQ) for permanently failed jobs
- Track job status
- REST API with FastAPI
- Simple and modular project structure

---

# Project Structure

```
QueueCTL/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── workers/
│   └── main.py
│
├── run_worker.py
├── requirements.txt
├── .env
└── README.md
```

---

# Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/QueueCTL.git

cd QueueCTL
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

### 4. Create MySQL Database

```sql
CREATE DATABASE queuectl;
```

---

### 5. Configure Environment Variables

Create a `.env` file in the project root.

```env
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306
DB_NAME=queuectl

MAX_RETRIES=3
BACKOFF_BASE=2
WORKER_SLEEP=2
```

Update the MySQL username and password according to your local setup.

---

### 6. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

The API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

### 7. Start the Worker

Open another terminal and run:

```bash
python run_worker.py
```

The worker will continuously check for pending jobs and execute them.

---

# Usage Examples

### Create a Job

**POST** `/jobs`

Request

```json
{
    "command":"echo Hello World",
    "max_retries":3
}
```

Response

```json
{
    "id":"6af32d...",
    "command":"echo Hello World",
    "state":"pending",
    "attempts":0,
    "max_retries":3
}
```

---

### Get All Jobs

```
GET /jobs
```

---

### Check Job Summary

```
GET /jobs/status/summary
```

Example Response

```json
{
    "pending":2,
    "processing":1,
    "completed":5,
    "failed":0,
    "dead":1
}
```

---

### View Dead Letter Queue

```
GET /dlq
```

---

### Retry a Dead Job

```
POST /dlq/{job_id}
```

---

# Architecture Overview

The project is divided into different layers so that each part has a single responsibility.

- **API Layer** handles incoming requests.
- **Service Layer** contains the business logic.
- **Database Layer** stores all job information.
- **Worker** continuously processes pending jobs.
- **Utility Layer** executes shell commands using Python's subprocess module.

The overall workflow is shown below.

```
Client

   │

   ▼

FastAPI API

   │

   ▼

Queue Service

   │

   ▼

MySQL Database

   ▲

   │

Worker Process

   │

   ▼

Execute Command
```

---

# Job Lifecycle

Every job goes through the following states.

```
Pending
    │
    ▼
Processing
    │
 ┌──┴──────────┐
 │             │
 ▼             ▼
Completed   Failed
                 │
                 ▼
          Retry Available?
             │        │
            Yes       No
             │        │
             ▼        ▼
         Pending     Dead
```

---

# Retry Mechanism

Whenever a job fails, it is retried automatically.

The delay between retries follows exponential backoff.

```
delay = BACKOFF_BASE ^ attempts
```

Example

| Attempt | Delay |
|---------|--------|
|1|2 seconds|
|2|4 seconds|
|3|8 seconds|

If the maximum retry count is reached, the job is moved to the Dead Letter Queue.

---

# Job States

| State | Description |
|-------|-------------|
|Pending|Waiting to be processed|
|Processing|Currently running|
|Completed|Executed successfully|
|Failed|Execution failed but can be retried|
|Dead|Moved to Dead Letter Queue|

---

# Assumptions & Trade-offs

- MySQL is used for storing jobs permanently.
- Workers keep polling the database for new jobs.
- Commands are executed using Python's `subprocess` module.
- Retry delay is implemented using exponential backoff.
- A failed job is moved to the Dead Letter Queue after reaching the maximum retry limit.
- The project focuses on simplicity while demonstrating the core concepts of a production job queue.

---

# Testing Instructions

### Test 1 – Successful Job

Create a job using

```json
{
    "command":"echo Hello"
}
```

Expected Result

```
Job Completed Successfully
```

---

### Test 2 – Failed Job

Create a job

```json
{
    "command":"invalidcommand"
}
```

Expected Result

```
Retry 1

Retry 2

Retry 3

Moved to Dead Letter Queue
```

---

### Test 3 – Persistence

1. Add a few jobs.
2. Stop the application.
3. Restart the server.
4. Verify that all jobs are still available in MySQL.

---

### Test 4 – Multiple Workers

Start multiple worker processes using different terminals.

Each worker should process different jobs without duplicating execution.

---

# Future Improvements

Some additional features that can be added in future versions include:

- Scheduled jobs
- Priority queues
- Docker support
- Job timeout handling
- Metrics dashboard
- Authentication
- Web dashboard
- Better logging and monitoring

---

# Conclusion

This project demonstrates the basic working of a background job queue system. It includes persistent job storage, worker-based execution, retry logic with exponential backoff, and a Dead Letter Queue. The code is organized into separate modules to make it easier to understand, maintain, and extend.

---

## Author

**Archit Awasthi**

Backend Developer Internship Assignment

Built using Python, FastAPI, SQLAlchemy, and MySQL.
