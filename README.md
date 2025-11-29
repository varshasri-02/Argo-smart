# AgroSmart

A Django-based agricultural system featuring ML-powered crop recommendation.

## Features

- **Crop Recommendation**: Uses Random Forest classifier trained on agricultural data to recommend optimal crops based on soil parameters (N, P, K, temperature, humidity, pH, rainfall)
- **User Management**: Admin panel for managing visitors, visitor registration and profiles
- **ML Evaluation**: Comprehensive model evaluation with 99.55% accuracy, 5-fold cross-validation, and comparison of multiple algorithms

## Local Development

1. Clone the repository
2. Create a `.env` file with your environment variables (see `.env` example)
3. Run `docker-compose up --build` to start the application and database

## Deployment

### Prerequisites

- AWS Account
- GitHub Repository
- Docker

### AWS Setup

1. **Create ECR Repository:**
   ```bash
   aws ecr create-repository --repository-name agrosmart-repo --region us-east-1
   ```

2. **Create ECS Cluster:**
   ```bash
   aws ecs create-cluster --cluster-name agrosmart-cluster
   ```

3. **Create ECS Task Definition:**
   Use the AWS Console or CLI to create a task definition with:
   - Task family: agrosmart-service
   - Container name: agrosmart-container
   - Image: Your ECR repository URI
   - Port mappings: 8000
   - Environment variables: Set production values

4. **Create ECS Service:**
   Create a service in the cluster using the task definition.

### GitHub Secrets

Add the following secrets to your GitHub repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Deployment

Push to the `main` branch to trigger automatic deployment via GitHub Actions.

## Environment Variables

- `DEBUG`: Set to `True` for development, `False` for production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`: Database configuration
