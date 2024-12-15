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
- **Docker CLI and Desktop Installed**: To build and push container images.
- **AWS CLI Installed and Configured**: To programatically interact with AWS

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

### **Clone the Repository**
```bash
git clone https://github.com/ifeanyiro9/containerized-sports-api.git
cd containerized-sports-api
```
### **Create ECR Repo**
```bash
aws ecr create-repository --repository-name sports-api --region us-east-1
```

### **Build and Push the Docker Image**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker build -t sports-api .
docker tag sports-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest
```

### **Set Up ECS Cluster with Fargate**
1. Create an ECS Cluster:
- Go to the ECS Console → Clusters → Create Cluster.
- For Infrastructure, select Fargate and name the cluster sports-api-cluster
- Select "Create"

2. Create a Task Definition:
- Go to Task Definitions → Create New Task Definition → Fargate.
- Add the container:
  - Image: <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/sports-api:latest.
  - Port Mapping: 8080
- Define environment variables:
  - SPORTS_API_KEY: <YOUR_SPORTSDATA.IO_API_KEY>
3. Run the Service with an ALB
- Go to Clusters → Create Service.
- Launch type: Fargate.
- Load Balancer: Select Application Load Balancer (ALB).
- ALB Configuration:
 - Create a new ALB:
 - Name: sports-api-alb.
 - Scheme: Internet-facing.
 - Attach it to the same VPC and subnets as your ECS service.
- Create a Target Group:
  - Target Type: IP (for Fargate).
  - Port: 8080 (to match your container).
  - Register your ECS tasks in the target group.
- Security Group:
  - Allow inbound traffic on port 80 (for HTTP) and/or port 443 (for HTTPS if using SSL).
- Set Auto Scaling (Optional):
  - Configure ECS to scale tasks based on metrics like CPU or memory usage.
4. Test the ALB:
- After deploying the ECS service, note the DNS name of the ALB (e.g., sports-api-alb-<AWS_ACCOUNT_ID>.us-east-1.elb.amazonaws.com).
- Confirm the API is accessible by visiting the ALB DNS name in your browser

### **Configure API Gateway**
1. Create a New REST API:
- Go to API Gateway Console → Create API → REST API.
- Name the API (e.g., Sports API Gateway).

2. Set Up Integration:
- Create a resource /sports.
- Create a GET method.
- Choose HTTP Proxy as the integration type.
- Enter the DNS name of the ALB (ALB's public URL) of your ECS service.

3. Deploy the API:
- Deploy the API to a stage (e.g., prod).
- Note the endpoint URL.

### **Test the System**
- Use curl or a browser to test:
```bash
curl https://<api-gateway-id>.execute-api.us-east-1.amazonaws.com/prod/sports
```

### **What We Learned**
Setting up a scalable, containerized application with ECS.
Creating public APIs using API Gateway.

### **Future Enhancements**
Add caching for frequent API requests using Amazon ElastiCache.
Add DynamoDB to store user-specific queries and preferences.
Secure the API Gateway using an API key or IAM-based authentication.
Implement CI/CD for automating container deployments.


