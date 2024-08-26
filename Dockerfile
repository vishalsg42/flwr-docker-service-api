# FROM python:3.8-slim

# # Install git
# RUN apt-get update && apt-get install -y git && apt-get clean

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set the working directory
# WORKDIR /app

# # Clone the GitHub repository
# RUN git clone https://github.com/vishalsg42/flwr-monitioring-sample-app.git /app

# # Install Python dependencies
# RUN pip install -r requirements.txt
    
# ENV SERVER_IP=0.0.0.0
# ENV SERVER_PORT=8080
# ENV PROMETHEUS_IP=0.0.0.0
# ENV PROMETHEUS_PORT=8000

# ENTRYPOINT ["python", "server.py"]
# CMD ["--server-ip", "0.0.0.0", "--server-port", "8080", "--prometheus-ip", "0.0.0.0", "--prometheus-port", "8000"]

FROM python:3.8-slim

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Clone the GitHub repository
RUN git clone https://github.com/vishalsg42/flwr-monitioring-sample-app.git /app

# Install Python dependencies
RUN pip install -r requirements.txt
    
ENV WANDB_API_KEY="f59537fb3f2c0637963296163cda8ab11147405a"
ENV WANDB_BASE_URL="https://api.wandb.ai"
ENV WANDB_PROJECT_NAME="wandb-project"

ENTRYPOINT ["python", "server.py"]
CMD ["python", "server.py", "--project-name", "wandb-project", "--server-ip", "0.0.0.0"]