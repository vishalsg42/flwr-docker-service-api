async def generate_server_dockerfile(
    github_url,
    monitoring_tool,
    prometheus_ip=None,
    prometheus_port=None,
    wandb_api_key=None,
    wandb_base_url=None,
    wandb_project_name=None,
    server_ip=None,
    server_port=None
):
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

    # Adjust the Dockerfile based on the monitoring tool
    if monitoring_tool == "prometheus":
        dockerfile += f"""
ENTRYPOINT ["python", "server.py"]
CMD ["--server-ip", "$SERVER_IP", "--server-port", "$SERVER_PORT", "--prometheus-ip", "$PROMETHEUS_IP", "--prometheus-port", "$PROMETHEUS_PORT"]
        """
    elif monitoring_tool == "wandb":
        dockerfile += f"""
ENTRYPOINT ["python", "server.py"]
CMD ["--server-ip", "$SERVER_IP", "--server-port", "$SERVER_PORT", "--project-name", "$WANDB_PROJECT_NAME"]
        """
    return dockerfile.strip()


async def generate_server_compose_file(
    github_url,
    monitoring_tool,
    prometheus_ip=None,
    prometheus_port=None,
    wandb_api_key=None,
    wandb_base_url=None,
    wandb_project_name=None,
    server_ip="0.0.0.0",
    server_port=8080
):
    # Generate the Dockerfile content inline
    dockerfile_content = await generate_server_dockerfile(
        github_url,
        monitoring_tool,
        prometheus_ip,
        prometheus_port,
        wandb_api_key=wandb_api_key,
        wandb_base_url=wandb_base_url,
        wandb_project_name=wandb_project_name,
        server_ip=server_ip,
        server_port=server_port
    )

    # Properly indent the Dockerfile content for the dockerfile_inline
    indented_dockerfile_content = '\n'.join([f"        {line}" for line in dockerfile_content.splitlines()])

    compose_file = f"""
services:
  server:
    build:
      context: .
      dockerfile_inline: |
{indented_dockerfile_content}
    environment:
      SERVER_IP: "{server_ip}"
      SERVER_PORT: "{server_port}"
    """

    # Add environment variables and command based on the monitoring tool
    if monitoring_tool == "prometheus":
        compose_file += f"""
      PROMETHEUS_IP: "{prometheus_ip}"
      PROMETHEUS_PORT: "{prometheus_port}"
    command: ["--server-ip", "{server_ip}", "--server-port", "{server_port}", "--prometheus-ip", "{prometheus_ip}", "--prometheus-port", "{prometheus_port}"]
    ports:
      - "{server_port}:{server_port}"
      - "{prometheus_port}:{prometheus_port}"
    """
    elif monitoring_tool == "wandb":
        compose_file += f"""
      WANDB_API_KEY: "{wandb_api_key}"
      WANDB_BASE_URL: "{wandb_base_url}"
      WANDB_PROJECT_NAME: "{wandb_project_name}"
    command: ["--server-ip", "{server_ip}", "--server-port", "{server_port}"]
    ports:
      - "{server_port}:{server_port}"
    """

    compose_file += """
    networks:
      - app_network

networks:
  app_network:
    driver: bridge
    """

    return compose_file.strip()


async def generate_client_dockerfile(github_url, monitoring_tool="prometheus",server_ip=None, server_port=None):
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

# Set the entry point to run client.py"""
 # Add environment variables and command based on the monitoring tool
  # Set the entry point to run client.py
  if monitoring_tool == "prometheus":
        dockerfile += f"""
ENTRYPOINT ["python", "client.py"]
CMD ["--server-ip", "$SERVER_IP", "--server-port", "$SERVER_PORT"]
        """
  elif monitoring_tool == "wandb":
        dockerfile += f"""
ENTRYPOINT ["python", "client.py"]
CMD ["--server-ip", "$SERVER_IP", "--server-port", "$SERVER_PORT"]
        """

  return dockerfile.strip()

async def generate_client_compose_file(github_url, server_ip=None, server_port=None):
    # Generate the Dockerfile content inline
    dockerfile_content = await generate_client_dockerfile(github_url, server_ip, server_port)

    # Properly indent the Dockerfile content for the dockerfile_inline
    indented_dockerfile_content = '\n'.join([f"        {line}" for line in dockerfile_content.splitlines()])

    compose_file = f"""
services:
  client:
    build:
      context: .
      dockerfile_inline: |
{indented_dockerfile_content}
    environment:
      - SERVER_IP={server_ip if server_ip else "0.0.0.0"}
      - SERVER_PORT={server_port if server_port else "8080"}
    networks:
      - app_network
networks:
  app_network:
    driver: bridge
    """

    return compose_file.strip()
