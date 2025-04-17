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
- [x] Configure Ansible Server

### Phase 2: Configuration and Initial Pipeline Setup 
- [x] Configure Jenkins Master and Build Node using Ansible
- [x] Create initial Jenkins Pipeline Job
- [x] Develop Jenkinsfile with core stages
- [x] Implement Multi-branch Pipeline
- [x] Configure GitHub webhook integration

### Phase 3: Integrating Quality Checks and Artifact Management
- [ ] Set up SonarQube and Sonar Scanner
- [ ] Add SonarQube Analysis to pipeline
- [x] Configure Nexus Repository Manager
- [x] Create application Dockerfile
- [x] Configure pipeline to publish Docker images to Nexus

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
### April 5, 2025
- Configured ansible for jenkins
- Resolved issue with installing jenkins plugins by creating an admin user
- How to automatically trigger ansible after terraform infra creation ? - Use github actions. I created a webhook to trigger when the terraform infra is complete
- Configured Jenkins Master and Build Node
### April 8, 2025
- Bottleneck - Terraform cloud doesn't support Authorisation so can't trigger Ansible machine from Github
- Have to SSH to ansible machine manually
- Configured multibranch pipeline
- Test pipeline trigger when a new change is pushed
- Made the mistake of installing nexus in t2.micro. Wasted a day figuring it out why it is not working
### April 9, 2025
- Installed nexus, configured Jenkins multipipeline to build when a change is pushed to github
- Configured Nexus Repo
- Sometimes EC2 stops connecting - Why ?
- Issue with accessing docker when I build jenkins
### April 10, 2025
- Spent time debugging Jenkins agent connection. The issue was due to configuring the wrong IP for the agent.
- Added EC2's public IP as an insecure registry in the Docker daemon to allow image pushes to Nexus.
- Confirmed that Nexus is accessible on port 8081 (UI) and 8083 (Docker HTTP connector).
- Docker image was successfully built via Jenkins pipeline and tagged correctly.
- Configured Jenkins to push Docker images to the Nexus hosted Docker registry.
- Next step: Set up Kubernetes and deploy the Docker image pulled from Nexus.
### April 11,15,16 2025
- Kubernetics was driving me crazy.
- Errors Faced
  - When I ran the command "_kubectl get nodes_," I encountered a connection error to the port <private-ip>. Upon investigation, I discovered that several Kubernetes system containers were crashing, including etcd and api-server. The connection error occurred because the api-server was down. To debug the issue, I used the command _crictl ps -a_ to list all containerd pods and their status. I then examined the logs of specific containers using _crictl logs <container-id>_. Although this debugging approach didn't immediately reveal the solution, the system eventually started working after several restarts of the affected containers.
  - I faced another issue where the worker-node status showed as "NotReady." Initially, I suspected this was because I hadn't installed a network plugin. However, further investigation revealed there was also a memory issue on the worker node.I resolved the problem by freeing up memory and increasing the memory allocation for the machines. This ultimately fixed the issue. The _kubectl describe node_ command was particularly helpful during the debugging process, as it provided detailed information about the node's status and conditions.
  - I created deployment.yaml and server.yaml in which I gave the image name incorrectly at first then it turned out to be an issue where image is trying to pull from https but the image is avaliable in http
- I am going to start everything from the scratch again and see how long does it take for me to complete since I am familiar with most of the steps.
- Memorised the command as I kept writing it over and over again.

## Point to Remember when starting out a CI/CD again:
  - Be clear on how many machines to spin up.
  - Use alias to connect to machines
  - look for the correct-ip
  - Analyse and Determine the system size beforehand.
  - Automate as much as possible. 
