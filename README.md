
# Distributed Workflow Engine

A backend workflow orchestration system for defining, scheduling, dispatching, and monitoring dependent tasks with retry handling, execution timeouts, worker monitoring, and dead-letter queue processing.

Built to explore the core engineering concepts behind distributed task execution platforms such as workflow engines, job schedulers, and background processing systems.

## Overview

The Distributed Workflow Engine allows users to define workflows composed of multiple tasks and execute them according to their dependencies.

The system separates workflow management, task scheduling, message dispatching, and task execution into distinct components.

It supports execution tracking and failure-handling mechanisms designed to improve reliability during task processing.

### Core capabilities

- Workflow and task management
- Dependency-based task scheduling
- Task priority handling
- Redis-backed task dispatching
- Worker registration and heartbeat monitoring
- Retry handling with exponential backoff
- Task timeout detection
- Dead-letter queue processing
- Basic idempotency protection
- Workflow-level execution status tracking
- Execution summaries and task status aggregation

---

## Architecture

```text
                    ┌────────────────────┐
                    │       Client       │
                    │  Swagger / HTTP    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │    Workflow API    │
                    │      FastAPI       │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   Orchestrator     │
                    │ Workflow Execution │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │     Scheduler      │
                    │ Dependencies/Prior │
                    │      itization     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │    Redis Queue     │
                    │   Task Dispatch    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │      Workers       │
                    │   Task Execution   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ PostgreSQL Storage │
                    │ Execution Metadata │
                    └────────────────────┘
```

The architecture separates API requests from task scheduling and worker execution.

Redis is used for task dispatching, while PostgreSQL stores workflow, task, dependency, worker, and execution-related data.

---

## Workflow Execution Lifecycle

A typical workflow execution follows these stages:

1. A workflow is created with its associated tasks.
2. Dependencies are defined between tasks.
3. A workflow execution is created.
4. The scheduler identifies tasks that are ready to run.
5. Ready tasks are dispatched through Redis.
6. Workers retrieve and execute assigned tasks.
7. Task execution states are updated in the database.
8. Failed tasks may be retried using exponential backoff.
9. Tasks that exhaust their retries can be moved to the dead-letter queue.
10. The workflow status is updated based on task execution results.

---

## Reliability Features

### Retry Handling

Failed tasks can be retried according to their configured retry limit.

The retry mechanism uses exponential backoff to delay subsequent attempts.

This helps avoid repeatedly retrying failed tasks without a delay.

### Timeout Handling

Tasks support configurable execution timeouts.

Tasks that exceed their allowed execution time are marked as failed and can enter the retry flow according to the configured retry policy.

### Dead-Letter Queue

Tasks that continue failing after exhausting their retry attempts can be moved to a dead-letter queue.

This separates repeatedly failing tasks from the normal execution path for further inspection or recovery.

### Worker Monitoring

Workers register with the system and provide heartbeat information.

The monitoring mechanism can identify workers that become inactive or unhealthy.

### Idempotency

The system includes basic idempotency protection to reduce duplicate workflow execution under supported conditions.

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Application and execution logic |
| FastAPI | REST API development |
| PostgreSQL | Persistent application and execution data |
| SQLAlchemy | Database ORM |
| Redis | Task queue and dispatching |
| Docker | Infrastructure service management |
| Pydantic | Request validation and configuration |

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
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## API Modules

The application exposes API endpoints for:

- Workflow creation and management
- Task creation and management
- Task dependency configuration
- Workflow execution creation
- Execution detail and summary retrieval
- Scheduler operations
- Worker registration and monitoring
- Dead-letter queue inspection

Interactive API documentation is available through FastAPI Swagger UI.

---

## Local Setup

### Prerequisites

Install the following:

- Python 3.10 or later
- PostgreSQL
- Redis
- Docker Desktop (for running infrastructure services)
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd distributed-workflow-engine
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Configure the required PostgreSQL and Redis connection settings.

Do not commit credentials or private environment variables to the repository.

### 5. Start PostgreSQL and Redis

Ensure that PostgreSQL and Redis are running and accessible using the connection settings in `.env`.

If Redis is running in Docker, verify the container is active before starting the application.

### 6. Start the API

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Validation

The project was validated through API testing using FastAPI Swagger UI.

Validation scenarios include:

- Creating workflows and tasks
- Defining task dependencies
- Creating workflow executions
- Checking task readiness
- Dispatching tasks through Redis
- Processing task execution
- Testing retry behavior
- Testing timeout handling
- Testing dead-letter queue behavior
- Checking worker monitoring endpoints
- Reviewing workflow execution summaries

The current implementation is an MVP designed to demonstrate workflow orchestration and distributed execution concepts.

---

## Engineering Considerations

The project explores several practical challenges involved in distributed task execution:

- Separating task scheduling from task execution
- Managing task dependencies
- Handling transient task failures
- Tracking task and workflow state
- Monitoring worker availability
- Preventing uncontrolled retry loops
- Isolating repeatedly failing tasks
- Maintaining execution metadata in persistent storage

The implementation prioritizes clear architecture and core functionality over production-scale deployment.

---

## Current Limitations

This project is a simplified workflow orchestration engine and is not intended to replace production platforms such as Temporal, Airflow, or Celery.

Potential areas for future improvement include:

- Distributed scheduler coordination
- Stronger task leasing and duplicate-execution prevention
- Persistent queue recovery
- More comprehensive automated testing
- Metrics and observability
- Authentication and authorization
- Horizontal worker scaling
- Containerized end-to-end deployment
- Advanced workflow recovery and compensation strategies

---

## Future Improvements

- Add a complete automated integration test suite.
- Introduce metrics and execution dashboards.
- Improve distributed worker coordination.
- Add stronger task locking and lease expiration.
- Support workflow cancellation and recovery.
- Add configurable concurrency limits.
- Improve queue durability and recovery mechanisms.

---

## Learning Outcomes

Through this project, I explored:

- Backend API architecture
- Workflow and task orchestration
- Dependency-based scheduling
- Redis-based task dispatch
- Worker execution models
- Retry and timeout strategies
- Dead-letter queue design
- Database-backed execution tracking
- Reliability considerations in distributed systems

---

## Project Status

**Status:** Functional MVP

The project implements the core workflow orchestration, task execution, retry, monitoring, and failure-handling features described above.

---

## License

This project is available for educational and portfolio purposes.
