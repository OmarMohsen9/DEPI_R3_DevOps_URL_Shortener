### GitHub Actions Pipeline Documentation

#### File Name

`.github/workflows/deploy.yaml`

#### Purpose

Automate the build and deployment of the Dockerized application to an EC2 instance whenever code is pushed to the `main` branch.

#### Workflow Overview

```yaml
name: Deploy to EC2

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set up Docker
        uses: docker/setup-buildx-action@v3

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and Push Docker Image
        run: |
          docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/url-shortener:latest .
          docker push ${{ secrets.DOCKERHUB_USERNAME }}/url-shortener:latest

      - name: SSH to EC2 and Deploy
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            docker pull ${{ secrets.DOCKERHUB_USERNAME }}/url-shortener:latest
            docker stop url-shortener || true
            docker rm url-shortener || true
            docker run -d --name url-shortener -p 9000:9000 \
              -e BASE_URL=http://<EC2-PUBLIC-IP>:9000 \
              -v /data/url-shortener:/app/data \
              ${{ secrets.DOCKERHUB_USERNAME }}/url-shortener:latest
```

#### Required GitHub Secrets

| Secret Name          | Description                                               |
| -------------------- | --------------------------------------------------------- |
| `DOCKERHUB_USERNAME` | DockerHub account username (e.g., `ahmedanas04`).         |
| `DOCKERHUB_TOKEN`    | DockerHub access token (generated from account settings). |
| `EC2_HOST`           | Public IP or DNS of your EC2 instance.                    |
| `EC2_USER`           | SSH username for EC2 (e.g., `ubuntu`).                    |
| `EC2_SSH_KEY`        | Private SSH key used to connect to EC2 securely.          |

#### Notes

* The pipeline automatically builds and pushes the Docker image when pushing to `main`.
* It then connects to the EC2 instance via SSH and redeploys the container.
* Make sure Docker is installed and configured on the EC2 instance.
* Optionally, you can extend the script to also start Prometheus and Grafana containers if needed.

---

This file provides a CI/CD pipeline setup to automate deployment of your application on EC2 using GitHub Actions and Docker.
