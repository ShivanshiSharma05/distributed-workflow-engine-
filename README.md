# Distributed Workflow Engine

A backend workflow orchestration system for defining, scheduling, dispatching, and monitoring dependent tasks with retry handling, execution timeouts, worker monitoring, and dead-letter queue processing.

Built with **FastAPI, PostgreSQL, Redis, and Python** to explore the core engineering concepts behind distributed task execution platforms.

## Overview

The Distributed Workflow Engine allows users to define workflows containing multiple tasks and execute those tasks according to their dependencies, priorities, and execution states.

The system manages the workflow execution lifecycle through a scheduler, Redis-backed task dispatching, workers, retry handling, and execution monitoring.

The project is designed as a learning-focused functional MVP that demonstrates backend architecture and distributed systems fundamentals.

## Core Features

- Workflow creation and management
- Task creation and workflow association
- Task dependency management
- Workflow execution tracking
- Dependency-aware task scheduling
- Priority-based task scheduling
- Redis-backed task dispatching
- Worker registration and heartbeat monitoring
- Task execution and status tracking
- Retry handling with exponential backoff
- Task execution timeouts
- Idempotency protection
- Dead-letter queue handling
- Workflow-level status tracking
- Execution summary and monitoring endpoints

## Architecture

```text
                    Client
                      |
                      v
                FastAPI API
                      |
          +-----------+-----------+
          |                       |
          v                       v
      PostgreSQL              Scheduler
          |                       |
          |                       v
          |                 Redis Queue
          |                       |
          |                       v
          |                    Workers
          |                       |
          +-----------+-----------+
                      |
                      v
              Execution Status
              Retry / Recovery
              Dead-Letter Queue
```

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
Scheduler Identifies Ready Tasks
       |
       v
Tasks Dispatched to Redis
       |
       v
Workers Execute Tasks
       |
       +--------------------+
       |                    |
       v                    v
    Success             Failure
       |                    |
       |                    v
       |              Retry with
       |            Exponential Backoff
       |                    |
       |          +---------+---------+
       |          |                   |
       |          v                   v
       |       Retry Limit        Retry Limit
       |       Not Reached         Exceeded
       |          |                   |
       |          v                   v
       |       Requeue            Dead-Letter
       |                              Queue
       |
       v
Update Task and Workflow Status
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API framework |
| PostgreSQL | Persistent data storage |
| SQLAlchemy | ORM and database interaction |
| Redis | Task queue and dispatching |
| Pydantic | Data validation and schemas |
| Uvicorn | ASGI application server |
| Docker | Infrastructure and service execution |

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

## API Modules

The application provides API endpoints for:

- Workflows
- Tasks
- Task dependencies
- Workflow executions
- Task executions
- Scheduler operations
- Worker registration and monitoring
- Dead-letter queue operations

Interactive API documentation is available through FastAPI Swagger UI.

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ShivanshiSharma05/distributed-workflow-engine-.git
cd distributed-workflow-engine-
```

### 2. Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Configure the required PostgreSQL and Redis connection settings according to your local environment.

Do not commit `.env` or other files containing credentials or secrets.

### 5. Start Required Services

Start PostgreSQL and Redis using your local setup or Docker configuration.

Verify that Redis is available before starting the application.

### 6. Start the FastAPI Application

From the project root:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Example Execution Flow

A typical workflow execution consists of:

1. Create a workflow.
2. Add tasks to the workflow.
3. Define dependencies between tasks.
4. Create a workflow execution.
5. Allow the scheduler to identify ready tasks.
6. Dispatch ready tasks through Redis.
7. Execute tasks using workers.
8. Track task and workflow statuses.
9. Retry failed tasks when retry attempts remain.
10. Move tasks to the dead-letter queue when retry attempts are exhausted.
11. Review the execution summary.

## Reliability and Failure Handling

The project implements several reliability-related mechanisms:

- Configurable task retry limits
- Exponential backoff for retries
- Task timeout handling
- Worker heartbeat monitoring
- Worker failure status tracking
- Dead-letter queue processing
- Basic idempotency protection
- Workflow-level execution status tracking

These features are implemented as part of a learning-focused orchestration system and are not intended to provide production-scale guarantees.

## Engineering Considerations

The project explores the following engineering concepts:

- Separation of API, service, scheduling, and worker responsibilities
- Database-backed workflow and task state
- Queue-based task dispatching
- Dependency-aware execution
- Failure recovery and retry behavior
- Worker health monitoring
- Execution lifecycle management
- Persistent execution records

## Current Scope and Limitations

This project is a functional MVP intended for learning and demonstrating distributed systems fundamentals.

It does not currently claim to provide:

- Production-scale horizontal orchestration
- Guaranteed exactly-once task execution
- Multi-node consensus
- Advanced distributed locking
- High-availability control-plane deployment
- Comprehensive authentication and authorization
- Full production-grade observability
- Guaranteed delivery under every infrastructure failure scenario

These areas would require additional design, testing, and operational infrastructure.

## Future Improvements

Potential future improvements include:

- Improved authentication and authorization
- Advanced distributed locking
- Workflow versioning
- More comprehensive automated testing
- Metrics and observability dashboards
- Persistent event logging
- Improved worker coordination
- Containerized multi-worker deployment
- More advanced failure recovery mechanisms

## Learning Outcomes

Through this project, I explored:

- Backend API development with FastAPI
- Relational database modeling
- Redis-based task dispatching
- Workflow and dependency management
- Scheduling and priority handling
- Retry and timeout mechanisms
- Worker lifecycle monitoring
- Dead-letter queue processing
- Distributed systems design considerations

## Project Status

**Status:** Functional MVP

The project demonstrates the fundamental components of a workflow orchestration system, including workflow management, dependency-aware scheduling, task dispatching, worker execution, retries, timeout handling, and failure tracking.

## License

This project is intended for educational and portfolio purposes.
