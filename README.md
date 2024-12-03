# sports-api-system
Sports API Management System

Project Overview
This project demonstrates building a containerized API management system for querying sports data. It leverages Amazon ECS (Fargate) for running containers, Amazon API Gateway for exposing REST endpoints, and an external Sports API for real-time sports data. The project showcases advanced cloud computing practices, including API management, container orchestration, and secure AWS integrations.

Features
Exposes a REST API for querying real-time sports data.
Runs a containerized backend using Amazon ECS with Fargate.
Scalable and serverless architecture.
API management and routing using Amazon API Gateway.
Monitored using Amazon CloudWatch for performance and logging.
Designed with IAM least privilege security principles.
Prerequisites
Sports API Key: Sign up for a free account and subscription at sportsdata.io.
AWS Account: With basic understanding of ECS, API Gateway, and Docker.
Docker Installed: To build and push container images.
Technical Architecture
Cloud Provider: AWS
Core Services: Amazon ECS (Fargate), API Gateway, CloudWatch
Programming Language: Python 3.x
Containerization: Docker
IAM Security: Custom least privilege policies for ECS task execution and API Gateway.
Project Structure
bash
Copy code
sports-api-management/
├── src/
│   ├── app.py                  # Flask application for querying sports data
├── Dockerfile                  # Dockerfile to containerize the Flask app
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
Setup Instructions
1. Clone the Repository
bash
Copy code
git clone https://github.com/<your-github-username>/sports-api-management.git
cd sports-api-management
2. Create and Push the Docker Image
Write the Application Code:

src/app.py:

python
Copy code
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

SPORTS_API_URL = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDateFinal/"
SPORTS_API_KEY = os.environ.get("SPORTS_API_KEY")

@app.route('/sports', methods=['GET'])
def get_sports_data():
    try:
        # Replace with dynamic date handling as needed
        today_date = "2024-11-26"  # Example date
        response = requests.get(f"{SPORTS_API_URL}{today_date}", headers={"Ocp-Apim-Subscription-Key": SPORTS_API_KEY})
        response.raise_for_status()
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
Create a Dockerfile:

dockerfile
Copy code
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8080
CMD ["python", "app.py"]
Build and Push the Docker Image:

bash
Copy code
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker build -t sports-api .
docker tag sports-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest
3. Set Up ECS Cluster with Fargate
Create an ECS Cluster:

Go to the ECS Console → Clusters → Create Cluster.
Select Networking Only (Fargate) and name the cluster sports-api-cluster.
Create a Task Definition:

Go to Task Definitions → Create New Task Definition → Fargate.
Add the container:
Image: <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest.
Port Mapping: 8080.
Define environment variables:
SPORTS_API_KEY: Your Sports API key.
Run the Service:

Go to Clusters → Create Service.
Launch type: Fargate.
Assign subnets and a security group that allows inbound traffic on port 8080.
4. Configure API Gateway
Create a New REST API:

Go to API Gateway Console → Create API → REST API.
Name the API (e.g., Sports API Gateway).
Set Up Integration:

Create a resource /sports.
Create a GET method.
Choose HTTP Proxy as the integration type.
Enter the public URL of your ECS service (ALB or Fargate IP).
Deploy the API:

Deploy the API to a stage (e.g., prod).
Note the endpoint URL.
5. Test the System
Use curl or a browser to test:
bash
Copy code
curl https://<api-gateway-id>.execute-api.us-east-1.amazonaws.com/prod/sports
Monitor logs in CloudWatch Logs for both API Gateway and ECS tasks.
What We Learned
Setting up a scalable, containerized application with ECS.
Managing APIs securely and efficiently using API Gateway.
Monitoring and debugging with CloudWatch Logs.
Future Enhancements
Add caching for frequent API requests using Amazon ElastiCache.
Add DynamoDB to store user-specific queries and preferences.
Secure the API Gateway using an API key or IAM-based authentication.
Implement CI/CD for automating container deployments.
