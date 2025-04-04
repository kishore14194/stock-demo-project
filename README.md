# Stock Symbol Lookup App

## Project Overview

This project is a stock application that fetches stock ticker symbols based on relevant company names. For example, searching for "Marvel" will fetch Disney's ticker symbol (DIS) since Disney owns Marvel.

The repository also implements a complete CI/CD pipeline to automate building, testing, and deployment of the application.

## Current Progress

The project is currently in the initial infrastructure setup phase:

- Created project architecture and CI/CD pipeline plan
- Established two repositories:
  - [Terraform Repository](https://github.com/kishore14194/terraform-jenkins-infra) - Infrastructure as Code for provisioning
  - [Ansible Repository](https://github.com/kishore14194/cicd-ansible) - Configuration management

- Configured infrastructure provisioning with Terraform:
  - Set up three machines:
    - Jenkins master server
    - Worker/build node
    - Ansible control server
  - Integrated with Terraform Cloud for remote state management
  - Stored AWS access credentials securely in Terraform Cloud

## CI/CD Pipeline Architecture

The CI/CD pipeline is designed with the following components:

1. **Infrastructure**: AWS EC2 instances provisioned using Terraform
2. **Configuration Management**: Ansible for consistent server setup
3. **CI/CD Server**: Jenkins with master/worker node configuration
4. **Code Quality**: SonarQube for static code analysis
5. **Artifact Repository**: Nexus for storing Docker images
6. **Deployment Platform**: Kubernetes cluster for container orchestration
7. **Monitoring**: Prometheus and Grafana for observability

## Implementation Plan

### Phase 1: Infrastructure Provisioning
- [x] Set up Terraform configuration
- [x] Provision Jenkins Master, Build Node, and Ansible Server
- [ ] Configure Ansible Server

### Phase 2: Configuration and Initial Pipeline Setup 
- [ ] Configure Jenkins Master and Build Node using Ansible
- [ ] Create initial Jenkins Pipeline Job
- [ ] Develop Jenkinsfile with core stages
- [ ] Implement Multi-branch Pipeline
- [ ] Configure GitHub webhook integration

### Phase 3: Integrating Quality Checks and Artifact Management
- [ ] Set up SonarQube and Sonar Scanner
- [ ] Add SonarQube Analysis to pipeline
- [ ] Configure Nexus Repository Manager
- [ ] Create application Dockerfile
- [ ] Configure pipeline to publish Docker images to Nexus

### Phase 4: Kubernetes Deployment and Monitoring
- [ ] Provision Kubernetes Cluster using Terraform
- [ ] Create Kubernetes manifests
- [ ] Implement Helm charts for deployment
- [ ] Set up Prometheus and Grafana
- [ ] Configure monitoring dashboards

## Daily Progress Log

### April 3, 2025
- Completed project architecture planning
- Set up Terraform configuration in Terraform Cloud
- Successfully provisioned infrastructure for Jenkins master, build node, and Ansible server
### April 4, 2025
- Verified the triggers from terraform cloud
- Found an API to fetch the outputs of Jenkins master, build node, and Ansible servers dynamically
- Partially configured ansible
- How to automatically trigger ansible after terraform infra creation ?
- How to store the .pem file to access EC2 instance from ansible ?
