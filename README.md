# Metrics Collection Pipeline

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Database Schema](#database-schema)
- [Maintaining and Extending the Pipeline](#maintaining-and-extending-the-pipeline)
- [Assumptions](#assumptions)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

## Overview
This project is a metrics collection pipeline designed to gather, store, and analyze various user metrics. The application is built using Flask and PostgreSQL, with Docker used to containerize the application for easy deployment and scalability. The pipeline is designed to be extendable and maintainable, providing a robust solution for metrics collection.

## Project Structure

```
project/
│
├── app/
│   ├── Dockerfile
│   ├── ingest.py
│   ├── requirements.txt
│   └── ...
├── db/
│   ├── init.sql
│   └── ...
├── db_config/
│   └── pg_hba.conf
├── docker-compose.yml
└── README.md
```

## Setup and Installation

### Prerequisites
- Docker
- Docker Compose

### Installation

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/yourusername/project.git
   cd project
   \`\`\`

2. **Build the Docker images:**
   \`\`\`bash
   docker-compose build
   \`\`\`

3. **Run the containers:**
   \`\`\`bash
   docker-compose up -d
   \`\`\`

   This command will start up the PostgreSQL database and the Flask application.

## Running the Application

1. **Check the status of the containers:**
   \`\`\`bash
   docker-compose ps
   \`\`\`

2. **View the logs of the containers:**
   \`\`\`bash
   docker-compose logs
   \`\`\`

3. **Access the Flask application:**
   The application will be running at `http://localhost:5000`. You can interact with the API using tools like Postman or cURL.

## Database Schema

The database schema is initialized using the `init.sql` script located in the `db/` directory. The database contains a single table named `user_metrics`:

\`\`\`sql
CREATE TABLE user_metrics (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    session_id INT NOT NULL,
    talked_time INT,
    microphone_used BOOLEAN,
    speaker_used BOOLEAN,
    voice_sentiment TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    device_type TEXT
);

CREATE INDEX idx_user_id ON user_metrics(user_id);
CREATE INDEX idx_session_id ON user_metrics(session_id);
CREATE INDEX idx_timestamp ON user_metrics(timestamp);
\`\`\`

### Schema Explanation
- **user_metrics**: This table stores metrics related to user sessions.
  - `id`: Auto-incrementing primary key.
  - `user_id`: ID of the user.
  - `session_id`: ID of the session.
  - `talked_time`: The amount of time the user spent talking.
  - `microphone_used`: Boolean indicating if the microphone was used.
  - `speaker_used`: Boolean indicating if the speaker was used.
  - `voice_sentiment`: Sentiment analysis of the user's voice (e.g., "positive", "negative").
  - `timestamp`: The timestamp when the metric was recorded.
  - `device_type`: The type of device used (e.g., "mobile", "desktop").

## Maintaining and Extending the Pipeline

### Maintaining

- **Database Backups**: Regularly back up the database to avoid data loss. You can use PostgreSQL tools or Docker volumes to manage backups.
- **Monitoring**: Implement monitoring to ensure the pipeline is running smoothly. Consider using tools like Prometheus and Grafana for real-time metrics.

### Extending

- **New Metrics**: To add new metrics, update the `user_metrics` table by adding new columns and modifying the ingestion logic in `ingest.py`.
- **Additional Services**: You can add new services to the pipeline (e.g., a data processing service) by updating the `docker-compose.yml` file.

## Assumptions

- **Time Zone Handling**: It is assumed that all timestamps are stored in UTC to avoid issues with time zone conversions.
- **Data Integrity**: It is assumed that data is correctly validated before being sent to the API. No extensive validation is performed within the database.

## Limitations

- **Single Table Schema**: The current design uses a single table to store all metrics. This may not scale well with a large volume of data.
- **Lack of Authentication**: The API currently does not implement any authentication, which might be a security concern in production environments.

## Future Improvements

- **Authentication and Authorization**: Implement OAuth or another authentication mechanism to secure the API.
- **Data Partitioning**: Consider partitioning the `user_metrics` table based on time or user ID to improve query performance.
- **Automated Tests**: Add unit tests and integration tests to ensure the pipeline remains reliable as it evolves.
