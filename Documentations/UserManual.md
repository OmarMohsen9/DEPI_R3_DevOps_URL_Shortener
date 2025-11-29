# User Manual
## 1. Introduction

DEPI_R3_DevOps_URL_Shortener is a URL-shortener web-service, designed to let users shorten long URLs, and support redirecting. In addition, it is built with a monitoring stack to track service health and usage metrics (via Prometheus and Grafana), and uses containerization (via Docker / Docker Compose) to provide consistent environments.

The project aims to be a learning-oriented DevOps exercise, but is fully functional locally. It demonstrates building, containerizing, instrumenting, monitoring, and persisting a simple URL-shortener service.

## 2. Prerequisites & Requirements
- Docker installed
- Docker Compose installed   
- (Optional) If you wish for persistent storage, ensure Docker volumes or local directories are configured

## 3. Installation & Setup
### Step 1: Clone the Repository
Open a terminal and run:
```bash
git clone https://github.com/OmarMohsen9/DEPI_R3_DevOps_URL_Shortener
```
### Step 2: Docker Installation
This deploys the full stack with monitoring.
1. Ensure Docker and Docker Compose are installed and running
```bash
docker --version
docker compose version
```
2. Build and start the containers:
```bash
docker compose up --build
```
- This builds the app image, starts the FastAPI service, Prometheus, and Grafana.
- Use `--detach` flag to run in background: `docker compose up -d --build`.
3. Verify services:
- App:  `http://localhost:9000` (should see app UI).
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (default login: admin/admin; change on first login).
### Alternative: Local Python Installation (Development Only)
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
2. Install dependencies:
```python
pip install -r requirements.txt -y
```
3. Run the app:
```bash
fastapi dev url_shortener.py --port 9000
```
**Note:** For monitoring in local mode, manually set up Prometheus and Grafana as separate processes.

## Usage
The service provides a RESTful API for URL shortening. All endpoints are accessible at `http://localhost:9000`. Interactive API documentation is available at `http://localhost:9000/docs` (Swagger UI)

## API Endpoints
| Endpoint | Method | Description | Request body  | Response |
|-------|---------|-----------------|-------------|----------|
| `/` | **GET** | UI/ Health check / Welcome | None | Static Page |
| `/shorten` | **POST** | Shorten a URL | `{"long_url": "https://example.com/" ` | ` {"long_url": "https://example.com/",  "short_url": "https://example.com/" }`|
| `/{short_code}` | **GET** | Redirect to original URL | None | 307 Redirect to original URL |
| `/metrics` | **GET** | Prometheus metrics (for monitoring) | None | Text-based metrics (e.g., redirect counts) |

### Example: Shortening a URL
using curl:
```bash
curl -X POST http://localhost:9000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.github.com/OmarMohsen9/DEPI_R3_DevOps_URL_Shortener"}'
```
Response:
```bash
{"short_url": "http://localhost:9000/abc123"}
```
Then, access the short URL:
```bash
curl -L http://localhost:9000/abc123
```
This redirects to the original GitHub page.

#### Error Handling
* 400 Bad Request: Invalid URL format.
* 404 Not Found: Unknown alias.
* 500 Internal Server Error: Database or server issue (check logs).

### Monitoring Dashboard
1. Open Grafana at `http://localhost:9000`.
2. Log in (admin/admin).
3. view pre-configured dashboards for:
   - App uptime and response times.
    - Redirect metrics (e.g., total shortens, top URLs).
    - Resource usage (CPU/Memory via Prometheus).
      
Prometheus scrapes metrics from `/metrics` every 5 seconds (configurable in `prometheus.yml`).

### Monitorting and Logging
- **Logs:** View app logs with `docker compose logs -f` or in the terminal for local runs. FastAPI logs requests and errors.
- **Metrics:** Exposed at `/metrics`. Prometheus queries examples:
  + `http_requests_total` (total API calls).
  + `url_redirects_total` (custom counter for redirects).

- **Alerts**: Configure in Grafana (e.g., alert if response time > 500ms).
- **Troubleshooting:**
  - Check Docker: `docker ps` (running containers).
  - Database issues: Inspect `urls.db` with `sqlite3 urls.db "SELECT * FROM urls;"`.
  - High load: Scale with Docker Swarm or Kubernetes.

### Maintenance
- **Updates:** Pull latest code: `git pull`. Rebuild: `docker compose up --build`.
- **Backup:** Copy `urls.db` regularly. For production, use PostgreSQL instead of SQLite.
- **Scaling:** Add replicas in `docker-compose.yml` under services or implement our k8s solution ( find more in k8s/ readme).
- **Security:**
  - Validate all URLs to prevent open redirects (use `validators` library).
  - Rate-limit endpoints (e.g., via FastAPI middleware).
  - Use HTTPS in production (Nginx reverse proxy).

- **Cleanup:** Stop services: `docker compose down`. Remove volumes: `docker compose down -v`.

## Contributing
if you'd like to contribute:
1. Fork the repo.
2. Create a feature branch:` git checkout -b feature/new-shortener`.
3. Commit changes: `git commit -m "Add rate limiting"`.
4. Push and open a PR.

## Troubleshooting
| Issue | Possible Cause | Solution | 
|-------|---------|-----------------|
|"Port already in use"|Another service on 9000|Change port in `docker-compose.yml` or kill conflicting process.|
|Database locked|Concurrent writes|Use WAL mode: `PRAGMA journal_mode=WAL;` in SQLite.|
|No metrics in Grafana|Prometheus not scraping|Verify `prometheus.yml` targets the app.|
|Invalid short URL|Collision in aliases|Increase alphabet length or use longer aliases.|
|Docker build fails|Missing dependencies|Ensure `requirements.txt` is up-to-date; run `pip freeze > requirements.txt`.|

### Support
File issues on GitHub. For Custom Features, consider forking.
