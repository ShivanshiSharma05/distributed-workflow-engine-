# ⚙️ Distributed Workflow Engine

### A Reliable Backend Platform for Dependency-Aware Workflow Orchestration

A backend workflow orchestration platform designed to manage workflows, execute dependent tasks, distribute work through Redis, and track execution reliability using retries, timeouts, worker monitoring, and dead-letter queues.

The project explores core backend and distributed-systems concepts used in modern task orchestration platforms such as workflow engines, background job systems, and distributed task processing infrastructure.

---

## 🚀 Project Overview

Modern applications frequently execute multi-step operations such as:

- Data processing pipelines
- Background jobs
- File processing workflows
- Scheduled operations
- Automated business processes
- Multi-stage backend tasks

Executing these operations reliably requires more than simply calling functions.

A workflow orchestration system must be able to:

- Define workflows and tasks
- Manage task dependencies
- Identify tasks that are ready to execute
- Distribute tasks to workers
- Track execution states
- Retry failed tasks
- Handle task timeouts
- Detect unhealthy workers
- Store permanently failed tasks
- Track the overall workflow status

The **Distributed Workflow Engine** is designed to implement these concepts through a modular FastAPI backend, PostgreSQL persistence, Redis-based task processing, and worker-oriented execution.

---

## ✨ Key Features

### 1. Workflow Management

- Create and manage workflow definitions
- Organize multiple tasks inside a workflow
- Maintain workflow-level execution information
- Track the overall status of workflow executions

### 2. Task Management

- Create tasks associated with workflows
- Store task execution information
- Track task lifecycle states
- Support task-level configuration such as priority, retry limits, and timeouts

### 3. Dependency-Aware Scheduling

- Define relationships between tasks
- Identify tasks whose dependencies have been satisfied
- Prevent dependent tasks from executing before their required dependencies
- Support dependency-based workflow progression

Example:

```text
          Task A
         /      \
        v        v
     Task B    Task C
        \      /
         v    v
          Task D
```

Task B and Task C can become eligible after Task A completes successfully.

Task D depends on the completion of both Task B and Task C.

### 4. Redis-Based Task Queue

- Use Redis for task distribution
- Push eligible tasks into a queue
- Support communication between the scheduler and workers
- Separate API operations from task execution

```text
Ready Task
    |
    v
Scheduler
    |
    v
Redis Queue
    |
    v
Worker
    |
    v
Task Execution
```

### 5. Worker Execution

- Register workers
- Process queued tasks
- Update task execution states
- Track worker activity
- Record successful and failed task executions

The worker architecture provides the foundation for distributed task processing.

### 6. Retry with Exponential Backoff

Failed tasks can be retried according to configured retry policies.

Example:

```text
Attempt 1 → Failure
     |
     v
Retry with Backoff
     |
     v
Attempt 2 → Failure
     |
     v
Longer Backoff
     |
     v
Attempt 3 → Success / Final Failure
```

The system supports retry tracking and final failure handling.

### 7. Task Timeout Handling

Tasks can be configured with execution time limits.

The system uses timeout handling to prevent tasks from remaining active indefinitely.

Timeout behavior is integrated with the task failure and retry lifecycle.

### 8. Priority-Based Scheduling

Tasks can be assigned priorities.

The scheduler can consider task priority when selecting eligible tasks while still respecting dependency requirements.

A high-priority task cannot bypass dependencies that have not yet been completed.

### 9. Worker Heartbeat Monitoring

- Register workers
- Track worker activity
- Monitor heartbeat information
- Detect unhealthy or inactive workers
- Maintain worker status information

Supported worker states include:

```text
ACTIVE
BUSY
UNHEALTHY
OFFLINE
```

### 10. Dead-Letter Queue

Tasks that permanently fail or exceed their retry limit can be moved to a dead-letter state.

The system supports:

- Dead-letter task status
- Redis-based dead-letter queue functionality
- Dead-letter task inspection through an API endpoint
- Failure isolation after retry exhaustion

```text
Task Failure
     |
     v
Retry Attempts
     |
     v
Retry Limit Reached
     |
     v
Dead-Letter Queue
```

### 11. Idempotency Protection

The system includes basic protection against unintended duplicate task processing.

The implementation focuses on task execution identity and preventing repeated processing of an execution that has already reached a terminal state.

This is a limited application-level idempotency mechanism and is not intended to claim complete distributed exactly-once execution.

### 12. Workflow Execution Tracking

- Create workflow execution records
- Track execution start and completion
- Maintain workflow execution status
- View execution information
- Generate workflow execution summaries
- Track task counts by execution state

Supported workflow states include:

```text
PENDING
RUNNING
SUCCESS
FAILED
```

Supported task states include:

```text
PENDING
READY
QUEUED
RUNNING
SUCCESS
FAILED
RETRYING
DEAD_LETTER
```

---

## 🏗️ System Architecture

```text
                  ┌───────────────────────┐
                  │        Client         │
                  └───────────┬───────────┘
                              |
                              v
                  ┌───────────────────────┐
                  │      FastAPI API      │
                  └───────────┬───────────┘
                              |
                              v
                  ┌───────────────────────┐
                  │ Workflow Management   │
                  └───────────┬───────────┘
                              |
                              v
                  ┌───────────────────────┐
                  │ Task & Dependency     │
                  │ Management            │
                  └───────────┬───────────┘
                              |
                              v
                  ┌───────────────────────┐
                  │ Execution Management  │
                  └───────────┬───────────┘
                              |
                              v
                  ┌───────────────────────┐
                  │ Dependency Resolver   │
                  └───────────┬───────────┘
                              |
                              v
                  ┌───────────────────────┐
                  │ Scheduler / Dispatcher│
                  └───────────┬───────────┘
                              |
                              v
                  ┌───────────────────────┐
                  │     Redis Queue       │
                  └───────────┬───────────┘
                              |
                              v
                  ┌───────────────────────┐
                  │       Workers         │
                  └───────────┬───────────┘
                              |
                 ┌────────────┴────────────┐
                 v                         v
       ┌───────────────────┐    ┌───────────────────┐
       │    PostgreSQL     │    │    Dead-Letter     │
       │ Execution State   │    │      Queue         │
       └───────────────────┘    └───────────────────┘
```

---

## 🔄 Workflow Execution Lifecycle

```text
1. Create Workflow
        |
        v
2. Create Tasks
        |
        v
3. Configure Dependencies
        |
        v
4. Create Workflow Execution
        |
        v
5. Identify Ready Tasks
        |
        v
6. Dispatch Tasks to Redis
        |
        v
7. Worker Processes Task
        |
        v
8. Update Task Execution State
        |
        v
9. Retry or Complete Task
        |
        v
10. Resolve Newly Available Tasks
        |
        v
11. Update Workflow Status
```

---

## 🧩 Task Execution Lifecycle

```text
PENDING
   |
   v
READY
   |
   v
QUEUED
   |
   v
RUNNING
   |
   ├───────────────> SUCCESS
   |
   ├───────────────> RETRYING
   |                      |
   |                      v
   |                  RUNNING
   |
   └───────────────> FAILED
                          |
                          v
                    DEAD_LETTER
```

The exact transition depends on dependency conditions, execution results, retry configuration, and failure-handling logic.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Task Queue | Redis |
| API Documentation | OpenAPI / Swagger |
| Data Validation | Pydantic |
| Database Driver | psycopg2-binary |
| Application Server | Uvicorn |
| Containerization | Docker |
| Development Environment | Python Virtual Environment |

---

## 📂 Project Structure

```text
distributed-workflow-engine/
│
├── app/
│   ├── api/
│   │   ├── workflow.py
│   │   ├── task.py
│   │   ├── dependency.py
│   │   ├── execution.py
│   │   ├── scheduler.py
│   │   ├── task_execution.py
│   │   └── worker.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── redis.py
│   │
│   ├── models/
│   ├── schemas/
│   │
│   ├── scheduler/
│   │   └── scheduler.py
│   │
│   ├── services/
│   │   ├── workflow_service.py
│   │   ├── task_service.py
│   │   ├── dependency_service.py
│   │   ├── execution_service.py
│   │   ├── queue_service.py
│   │   ├── dispatch_service.py
│   │   ├── retry_service.py
│   │   ├── worker_service.py
│   │   └── worker_monitor.py
│   │
│   ├── workers/
│   │   └── worker.py
│   │
│   └── main.py
│
├── tests/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ShivanshiSharma05/distributed-workflow-engine-.git
cd distributed-workflow-engine-
```

> Verify the repository URL and folder name before publishing this README.

### 2. Create a Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment

```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Configure the required PostgreSQL and Redis connection settings.

Do not commit real passwords, credentials, or private configuration values.

### 6. Start Required Services

Ensure PostgreSQL and Redis are running.

If you use Docker for Redis, start the configured Redis container before launching the application.

### 7. Start the FastAPI Application

Use the application entry point configured in your project.

Example:

```powershell
uvicorn app.main:app --reload
```

> Confirm the entry point against your current `app/main.py` file before using this command.

### 8. Open API Documentation

```text
http://127.0.0.1:8000/docs
```

The Swagger interface can be used to explore and test the available API endpoints.

---

## 🔍 API Capabilities

The application provides API functionality for areas such as:

- Workflow creation and management
- Task creation and management
- Dependency configuration
- Workflow execution
- Ready-task identification
- Task execution tracking
- Scheduler operations
- Worker operations
- Dead-letter queue inspection
- Workflow execution summaries

The available endpoints should be verified through the current Swagger documentation.

---

## 🧠 Distributed Systems Concepts

This project demonstrates practical exploration of:

- Workflow orchestration
- Dependency-aware scheduling
- Task queues
- Worker-based execution
- Retry policies
- Exponential backoff
- Task timeouts
- Idempotency
- Dead-letter queues
- Worker heartbeat monitoring
- Failure detection
- Execution state management
- Relational database modeling
- Backend service modularization
- Asynchronous task processing

---

## ⚠️ Project Scope and Limitations

This project is an educational and portfolio-focused workflow orchestration platform.

It is not intended to be a production replacement for systems such as Temporal, Apache Airflow, or Celery.

The current implementation provides a foundation for reliable workflow execution, but production-grade systems may require additional capabilities such as:

- Strong distributed coordination
- Durable event sourcing
- Advanced leader election
- Exactly-once business-side effects
- Distributed locking guarantees
- Comprehensive observability
- Multi-node deployment testing
- Security hardening
- High-availability database configuration

The implemented reliability guarantees should be understood from the actual code and execution tests.

---

## 🔮 Potential Future Improvements

Possible future improvements include:

- Advanced workflow visualization
- More configurable task types
- Scheduled workflow execution
- Improved worker recovery policies
- Metrics and monitoring dashboards
- Distributed locking
- Authentication and authorization
- Automated integration tests
- Docker Compose orchestration
- CI/CD pipeline
- Horizontal worker scaling
- Persistent event history
- Improved failure recovery

---

## 🎯 Project Objective

The primary objective of this project is to understand how reliable backend workflow orchestration systems are designed and implemented.

The project focuses on:

1. Defining workflows and tasks.
2. Managing task dependencies.
3. Identifying executable tasks.
4. Distributing tasks through a queue.
5. Processing tasks using workers.
6. Handling retries and failures.
7. Monitoring worker activity.
8. Tracking workflow execution state.

---

## 👩‍💻 Author

**Shivanshi Sharma**

B.Tech Computer Science Engineering

Aspiring Software Engineer | Backend Development | Distributed Systems | Machine Learning

- GitHub: https://github.com/ShivanshiSharma05
- LinkedIn: https://linkedin.com/in/shivanshi-sharma-563610327

---

## ⭐ Summary

The Distributed Workflow Engine is a backend orchestration project that combines:

```text
FastAPI
   +
PostgreSQL
   +
Redis
   +
Dependency-Aware Scheduling
   +
Worker Execution
   +
Retry Handling
   +
Failure Recovery Foundations
```

The project demonstrates the design and implementation of a modular workflow execution platform with a focus on backend reliability and distributed task-processing concepts.
