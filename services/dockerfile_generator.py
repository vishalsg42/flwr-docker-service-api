async def generate_server_dockerfile(github_url, monitoring_tool, prometheus_ip=None, prometheus_port=None, wandb_api_key=None, wandb_base_url=None, wandb_project_name=None, server_ip=None, server_port=None):
    dockerfile = f"""
FROM python:3.8-slim

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Clone the GitHub repository
RUN git clone {github_url} /app

# Install Python dependencies
RUN pip install -r requirements.txt
    """

    if monitoring_tool == "prometheus":
        # Add Prometheus specific environment variables
        dockerfile += f"""
ENV SERVER_IP={server_ip}
ENV SERVER_PORT={server_port}
ENV PROMETHEUS_IP={prometheus_ip}
ENV PROMETHEUS_PORT={prometheus_port}

ENTRYPOINT ["python", "server.py"]
CMD ["--server-ip", "{server_ip}", "--server-port", "{server_port}", "--prometheus-ip", "{prometheus_ip}", "--prometheus-port", "{prometheus_port}"]
        """
    elif monitoring_tool == "wandb":
        # Add WandB specific environment variables and command
        dockerfile += f"""
ENV WANDB_API_KEY="{wandb_api_key}"
ENV WANDB_BASE_URL="{wandb_base_url}"
ENV WANDB_PROJECT_NAME="{wandb_project_name}"
ENV SERVER_IP={server_ip}
ENV SERVER_PORT={server_port}

ENTRYPOINT ["python", "server.py"]
CMD ["--project-name", "{wandb_project_name}", "--server-ip", "{server_ip}",  "--server-port", "{server_port}"]
        """
    else:

        # Default server command without additional monitoring tools
        dockerfile += f"""
ENTRYPOINT ["python", "server.py"]

CMD ["--server-ip", "${{SERVER_IP}}", "--server-port", "${{SERVER_PORT}}"]
        """

    return dockerfile.strip()


async def generate_client_dockerfile(github_url, server_ip, server_port):
    dockerfile = f"""
FROM python:3.8-slim

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Clone the GitHub repository
RUN git clone {github_url} /app

# Install Python dependencies
RUN pip install -r requirements.txt
    """

    # Set the environment variables and command for the client
    dockerfile += f"""
ENV SERVER_IP={server_ip}
ENV SERVER_PORT={server_port}

# Set the entry point to run client.py
ENTRYPOINT ["python", "client.py"]

CMD ["--server-ip", "{server_ip}", "--server-port", "{server_port}"]
    """

    return dockerfile.strip()
