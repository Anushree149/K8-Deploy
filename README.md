# Kubernetes DevOps Project

This repository contains a Kubernetes DevOps project that demonstrates how to deploy a Django application using Kubernetes.

## Prerequisites

Before you begin, ensure that you have the following prerequisites installed:

- Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- Kubernetes: [https://kubernetes.io/docs/setup/](https://kubernetes.io/docs/setup/)

## Getting Started

To get started with this project, follow the steps below:

1. Clone the repository:

   ```bash
   git clone https://github.com/Ab-D-ev/kubernetes-devops-project.git
   ```

2. Change into the project directory:

   ```bash
   cd kubernetes-devops-project
   ```

3. Build the Docker image:

   ```bash
   docker build -t django-app .
   ```

4. Deploy the Django application to Kubernetes:

   ```bash
   kubectl apply -f kubernetes
   ```

5. Monitor the deployment:

   ```bash
   kubectl get pods
   ```

   Once the pods are running, you can access the Django application by using the exposed service.

## Structure

The repository has the following structure:

- `django-app/`: Contains the Django application source code.
- `kubernetes/`: Contains the Kubernetes deployment configuration files.

## Configuration

The configuration files for Kubernetes deployment are located in the `kubernetes/` directory. Modify these files according to your requirements.

- `deployment.yaml`: Defines the Kubernetes Deployment for the Django application.
- `service.yaml`: Defines the Kubernetes Service for the Django application.

## Contributing

Contributions to this project are welcome. If you find any issues or want to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
