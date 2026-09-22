
# Distributed Workflow Engine

A distributed workflow orchestration engine built with **FastAPI, PostgreSQL, Redis, and Python**. The system manages workflow execution, dependency-aware task scheduling, distributed worker processing, retries, timeout handling, and failure recovery.

## Overview

Modern applications often execute workflows composed of multiple dependent tasks. These tasks may need to run sequentially or in parallel, be retried after failures, and be monitored throughout their lifecycle.

The **Distributed Workflow Engine** is a simplified workflow orchestration system inspired by concepts used in platforms such as Temporal, Airflow, and Celery.

The project focuses on implementing core distributed task-processing concepts, including:

- Workflow and task management
- Dependency-aware scheduling
- Redis-based task queuing
- Worker-based execution
- Retry and failure handling
- Worker monitoring
- Workflow-level execution tracking

> **Project scope:** This is an educational and portfolio implementation designed to explore workflow orchestration and distributed backend concepts. It is not intended to be a production replacement for established orchestration platforms.

---

## Key Features

### Workflow Management

- Create and manage workflows.
- Associate tasks with workflows.
- Create workflow executions.
- Track workflow-level execution status.

### Task Management

- Create tasks within a workflow.
- Configure task priority.
- Configure retry limits.
- Configure task timeout values.
- Track task execution states.

### Dependency-Aware Scheduling

- Define dependencies between tasks.
- Identify tasks whose dependencies are satisfied.
- Support workflow execution based on task relationships.
- Enable dependent tasks to proceed after prerequisite tasks complete.

### Distributed Task Processing

- Use Redis as a task queue.
- Dispatch tasks for worker processing.
- Execute tasks through worker services.
- Track task execution and worker assignments.

### Reliability and Failure Handling

- Retry failed tasks.
- Apply exponential backoff during retries.
- Handle task timeouts.
- Support idempotency protection in supported execution flows.
- Move tasks that exhaust retry attempts to a Dead-Letter Queue.
- Track workflow failure when tasks fail or reach the Dead-Letter Queue.

### Worker Monitoring

- Register workers.
- Track worker status.
- Support worker heartbeat handling.
- Detect worker failures through monitoring logic.

### Execution Monitoring

- Retrieve workflow execution details.
- Track task execution statuses.
- Aggregate task statuses into workflow status.
- View execution summaries and task status counts.

---

## Architecture

```text
                         Client
                           |
                           v
                    FastAPI REST API
                           |
                           v
                  Workflow Orchestrator
                           |
                           v
                       Scheduler
                           |
                           v
                     Redis Queue
                           |
             +-------------+-------------+
             |                           |
             v                           v
          Worker 1                    Worker 2
             |                           |
             +-------------+-------------+
                           |
                           v
                   Task Execution
                           |
                           v
                     PostgreSQL
                           |
                           v
               Workflow Status Tracking
```

### Main Components

| Component | Responsibility |
|---|---|
| FastAPI | Provides REST APIs and interactive Swagger documentation |
| Workflow Service | Handles workflow-related business logic |
| Task Service | Manages tasks and task configuration |
| Scheduler | Identifies and schedules executable tasks |
| Redis | Provides queue-based task communication |
| Workers | Retrieve and execute assigned tasks |
| PostgreSQL | Stores workflows, tasks, executions, and related state |
| Retry Service | Handles retry logic and backoff behavior |
| Worker Monitor | Tracks worker status and heartbeat information |
| Execution Service | Manages execution details and workflow status aggregation |

---

## Workflow Execution Lifecycle

```text
Create Workflow
      |
      v
Create Tasks
      |
      v
Define Dependencies
      |
      v
Create Workflow Execution
      |
      v
Identify Ready Tasks
      |
      v
Schedule Tasks
      |
      v
Push Tasks to Redis
      |
      v
Worker Retrieves Task
      |
      v
Execute Task
      |
      +--------------------+
      |                    |
      v                    v
   Success              Failure
      |                    |
      |                    v
      |                Retry?
      |                    |
      |             +------+------+
      |             |             |
      |             v             v
      |          Retry       Retry Limit
      |             |             |
      |             |             v
      |             |        Dead-Letter
      |             |           Queue
      |             |             |
      +-------------+-------------+
                    |
                    v
          Update Task Status
                    |
                    v
        Aggregate Workflow Status
```

### Task Status Lifecycle

Tasks can move through states such as:

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
   +--------------------+
   |                    |
   v                    v
SUCCESS              RETRYING
                         |
                         v
                      RUNNING

Failure after retry limit
          |
          v
     DEAD_LETTER
```

The exact transition depends on the scheduler, worker execution, retry, and failure-handling logic.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| FastAPI | REST API development |
| Uvicorn | ASGI application server |
| PostgreSQL | Persistent data storage |
| SQLAlchemy | Database ORM |
| Redis | Task queue and worker communication |
| Pydantic | Request and response validation |
| Pydantic Settings | Application configuration |
| Docker | Infrastructure and Redis container execution |
| Pytest | Automated testing where configured |

---

## Project Structure

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
│   ├── scheduler/
│   ├── services/
│   ├── workers/
│   └── main.py
│
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── venv/
```

> The structure above represents the major application components. Keep the structure synchronized with the actual repository.

---

## Getting Started

### Prerequisites

Install the following before running the application:

- Python 3.10 or a compatible supported Python version
- PostgreSQL
- Docker Desktop
- Redis
- Git

Check your installed versions:

```bash
python --version
docker --version
git --version
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd distributed-workflow-engine
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a local `.env` file using `.env.example` as a reference.

Configure the database and Redis settings required by the application.

Do not commit actual credentials or secrets to the repository.

---

## Running the Application

### 1. Start Redis

Start the Redis container configured for your local environment.

For the existing Redis container:

```powershell
docker start workflow-redis
```

Verify the Redis connection:

```powershell
docker exec workflow-redis redis-cli ping
```

Expected output:

```text
PONG
```

### 2. Start the FastAPI Server

```powershell
uvicorn app.main:app --reload
```

### 3. Open API Documentation

Open the following URL in your browser:

```text
http://127.0.0.1:8000/docs
```

FastAPI Swagger UI provides interactive documentation for exploring and testing the available API endpoints.

---

## API Areas

The application contains API routes for the following areas:

| API Area | Purpose |
|---|---|
| Workflows | Create and manage workflows |
| Tasks | Create and manage workflow tasks |
| Dependencies | Define relationships between tasks |
| Executions | Create and inspect workflow executions |
| Scheduler | Manage scheduling-related operations |
| Task Executions | Track individual task execution states |
| Workers | Worker registration and monitoring |
| Dead-Letter Queue | Inspect tasks that exhausted retry attempts |

The exact endpoints, request bodies, and response schemas are available through Swagger UI.

---

## Reliability Design

### Retry Handling

Failed tasks can be retried according to their configured retry limit.

The retry service supports exponential backoff to avoid repeatedly retrying failed tasks without delay.

### Timeout Handling

Tasks can be configured with a timeout value. When a task exceeds its configured execution limit, the worker execution logic handles the timeout according to the retry and failure-management flow.

### Dead-Letter Queue

When a task exhausts its permitted retry attempts, it can be moved to the Dead-Letter Queue.

This allows failed task executions to be inspected separately from normally completed tasks.

### Worker Monitoring

Worker monitoring functionality supports registration, heartbeat handling, and worker status tracking.

The system also includes failure-detection logic for workers that become unavailable.

### Idempotency

The project includes idempotency protection in supported execution flows to reduce duplicate processing.

The implementation should not be interpreted as a universal guarantee of exactly-once execution.

---

## Execution Status Tracking

### Workflow Statuses

The workflow execution model supports statuses such as:

- `PENDING`
- `RUNNING`
- `SUCCESS`
- `FAILED`

### Task Statuses

Task execution supports statuses such as:

- `PENDING`
- `READY`
- `QUEUED`
- `RUNNING`
- `SUCCESS`
- `FAILED`
- `RETRYING`
- `DEAD_LETTER`

The workflow status is aggregated from the statuses of its associated task executions.

---

## Testing and Validation

The workflow execution lifecycle and API functionality have been manually validated through FastAPI Swagger UI.

Validation areas include:

- Workflow creation
- Task creation
- Dependency configuration
- Workflow execution
- Task scheduling
- Redis queue processing
- Worker execution
- Retry behavior
- Timeout handling
- Dead-Letter Queue processing
- Worker monitoring
- Workflow status aggregation
- Execution summary APIs

Automated test coverage should be evaluated separately based on the test files available in the repository.

---

## Design Considerations

The project was developed to explore the following backend and distributed-systems concepts:

- Task scheduling
- Dependency management
- Queue-based communication
- Worker-based processing
- Retry and failure recovery
- Execution state management
- Workflow-level aggregation
- Service separation
- Persistent execution tracking

The implementation prioritizes learning and demonstrating these concepts through a working backend system.

---

## Limitations

This is a portfolio-level workflow orchestration implementation.

It does not claim to provide every production capability of systems such as Temporal, Airflow, or Celery.

Potential production-level improvements include:

- More comprehensive automated integration testing
- Advanced metrics and observability
- Stronger task cancellation guarantees
- Improved scheduler durability
- Horizontal worker scaling
- More advanced failure recovery
- Deployment automation
- Security hardening
- Distributed coordination mechanisms

---

## Future Improvements

- Docker Compose-based complete application deployment
- Monitoring dashboard
- Metrics and observability integration
- Workflow pause and resume
- Task cancellation
- Improved integration testing
- Horizontal worker scaling
- Scheduler persistence improvements
- Execution history and audit enhancements

---

## Learning Outcomes

Through this project, I explored:

- Backend API development using FastAPI
- Relational database design using PostgreSQL
- ORM-based persistence with SQLAlchemy
- Redis-based task queue architecture
- Dependency-aware scheduling
- Distributed worker execution
- Retry and timeout handling
- Failure recovery patterns
- Workflow status aggregation
- Service-oriented backend organization

---

## Project Status

**Status: Core MVP Completed**

The core workflow orchestration, task execution, queue processing, retry, timeout, worker monitoring, and failure-handling functionality has been implemented and manually validated through Swagger UI.

The project can be extended further with production-oriented observability, deployment, and testing improvements.

---

## License

Add an appropriate license if you decide to open-source the project.