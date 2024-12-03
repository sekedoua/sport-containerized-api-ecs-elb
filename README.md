# Sports API Management System

## **Project Overview**
This project demonstrates building a containerized API management system for querying sports data. It leverages **Amazon ECS (Fargate)** for running containers, **Amazon API Gateway** for exposing REST endpoints, and an external **Sports API** for real-time sports data. The project showcases advanced cloud computing practices, including API management, container orchestration, and secure AWS integrations.

---

## **Features**
- Exposes a REST API for querying real-time sports data.
- Runs a containerized backend using Amazon ECS with Fargate.
- Scalable and serverless architecture.
- API management and routing using Amazon API Gateway.
- Monitored using Amazon CloudWatch for performance and logging.
- Designed with **IAM least privilege** security principles.

---

## **Prerequisites**
- **Sports API Key**: Sign up for a free account and subscription at [sportsdata.io](https://sportsdata.io).
- **AWS Account**: With basic understanding of ECS, API Gateway, and Docker.
- **Docker Installed**: To build and push container images.

---

## **Technical Architecture**


---

## **Technologies**
- **Cloud Provider**: AWS
- **Core Services**: Amazon ECS (Fargate), API Gateway, CloudWatch
- **Programming Language**: Python 3.x
- **Containerization**: Docker
- **IAM Security**: Custom least privilege policies for ECS task execution and API Gateway.

---

## **Project Structure**

```bash
sports-api-management/
├── src/
│ ├── app.py # Flask application for querying sports data
├── Dockerfile # Dockerfile to containerize the Flask app
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md # Project documentation
```

---

## **Setup Instructions**

### Clone the Repository**
```bash
git clone https://github.com/ifeanyiro9/containerized-sports-api.git
cd containerized-sports-api
```

### Build and Push the Docker Image**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker build -t sports-api .
docker tag sports-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest
```

### Set Up ECS Cluster with Fargate**
1. Create an ECS Cluster:
- Go to the ECS Console → Clusters → Create Cluster.
- Select Networking Only (Fargate) and name the cluster sports-api-cluster

2. Create a Task Definition:
- Go to Task Definitions → Create New Task Definition → Fargate.
- Add the container:
  - Image: <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest.
  - Port Mapping: 8080
- Define environment variables:
  - SPORTS_API_KEY: "Your Sports API key".
3. Run the Service:
- Go to Clusters → Create Service.
- Launch type: Fargate.
- Assign subnets and a security group that allows inbound traffic on port 8080.


### Configure API Gateway
1. Create a New REST API:
- Go to API Gateway Console → Create API → REST API.
- Name the API (e.g., Sports API Gateway).

2. Set Up Integration:
- Create a resource /sports.
- Create a GET method.
- Choose HTTP Proxy as the integration type.
- Enter the public URL of your ECS service (ALB or Fargate IP).

3. Deploy the API:
- Deploy the API to a stage (e.g., prod).
- Note the endpoint URL.

### Test the System
- Use curl or a browser to test:
```bash
curl https://<api-gateway-id>.execute-api.us-east-1.amazonaws.com/prod/sports
```
- Monitor logs in CloudWatch Logs for both API Gateway and ECS tasks.


### What We Learned
Setting up a scalable, containerized application with ECS.
Managing APIs securely and efficiently using API Gateway.
Monitoring and debugging with CloudWatch Logs.

### Future Enhancements
Add caching for frequent API requests using Amazon ElastiCache.
Add DynamoDB to store user-specific queries and preferences.
Secure the API Gateway using an API key or IAM-based authentication.
Implement CI/CD for automating container deployments.


