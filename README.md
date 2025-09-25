# URL Shortner Webservice
DevOps Project for Devops Track under the supervision of Digital Egypt Pioneers Initiative
---
## Team members
- [Omar Mohsen Emam](https://github.com/OmarMohsen9)
- [Ahmed Anas ElSayed Daba](https://github.com/ahmedanasdev)
- [Marwa Abdullah Ouf Elzoghby](https://github.com/marwa-elzoghby)
- [Marwan Ayman Ismail](https://github.com/marwanaymann23)
- [Sara Darwish](https://github.com/SaraDrwish)
---
## Project Overview
This project involves building a simple URL shortener webservice, containerizing it, and implementing monitoring and visualization using Prometheus and Grafana. The entire stack will run locally with Docker and Docker Compose. The aim is not only to create a functional service but also to gain hands-on experience with instrumentation, metrics, dashboards, and alerting.
---
## Project Objectives
* Develop a functional, simple URL shortener web application with REST API endpoints.
* Containerize the application and its dependencies using Docker for consistent environments.
* Implement Monitoring by instrumenting the application code to expose custom Prometheus metrics.
* Visualize Data by building a comprehensive Grafana dashboard to monitor service health and usage patterns in real-time.
* Ensure Resilience by adding data persistence with Docker volumes and configuring meaningful alerts for operational awareness.
--- 
## Project Scope
* Build a local URL shortener service with SQLite.
* Containerize with Docker & Docker Compose.
* Expose metrics with Prometheus and visualize in Grafana.
* Add alerts, persistence, and basic documentation.
---
## Project Plan
The project will be executed in 4 weekly phases.
### Week 1 — Build & Containerize
+ Tasks:
  - Implement shorten (POST) and redirect (GET) endpoints.
  - Add SQLite storage for URL mappings.
  - Write Dockerfile for the service.
  - Create initial docker-compose.yml.
+ Deliverables:
  - Functional URL shortener webservice.
  - Docker image and compose file to run locally
### Week 2 — Prometheus Instrumentation
+ Tasks:
  - Add custom Prometheus metrics (counters, latency, errors).
  - Configure prometheus.yml to scrape metrics.
  - Integrate Prometheus service into docker-compose.yml.
+ Deliverables:
  - Webservice exposing /metrics endpoint.
  - Prometheus stack running and scraping metrics.
### Week 3 — Grafana Visualization
+ Tasks:
  - Add Grafana service to the stack.
  - Configure Prometheus as Grafana’s data source.
  - Build dashboards (rates, total counts, latency, errors).
+ Deliverables:
  - Grafana dashboard visualizing service health & usage.
  - Updated compose stack including Grafana.
### Week 4 — Alerting, Persistence & Documentation
+ Tasks:
  - Configure alerts in Grafana (error rate, latency thresholds).
  - Enable persistence with Docker volumes (SQLite, Prometheus, Grafana).
  - Perform restart testing for data persistence.
  - Write README with setup instructions and API guide.
+ Deliverables:
  - Persistent monitoring stack with alerts.
  - Comprehensive documentation.
---
