from aiohttp import web
from services.repo_validation import clone_and_validate_repo
from services.dockerfile_generator import generate_server_dockerfile

async def server_endpoint(request):
    data = await request.json()
    github_url = data.get('github_url')
    monitoring_tool = data.get('monitoring_tool')
    server_ip = data.get('server_ip')
    server_port = data.get('server_port')

    # Validate the GitHub repository
    is_valid, error_message = await clone_and_validate_repo(github_url)
    if not is_valid:
        return web.json_response({"error": error_message}, status=400)

    dockerfile = ""

    if monitoring_tool == "prometheus":
        prometheus_ip = data.get('prometheus_ip')
        prometheus_port = data.get('prometheus_port')

        dockerfile = await generate_server_dockerfile(
            github_url, 
            monitoring_tool, 
            prometheus_ip=prometheus_ip, 
            prometheus_port=prometheus_port,
            server_ip=server_ip,
            server_port=server_port
        )
    elif monitoring_tool == "wandb":
        wandb_api_key = data.get('wandb_api_key')
        wandb_base_url = data.get('wandb_base_url')
        wandb_project_name = data.get('wandb_project_name')
        dockerfile = await generate_server_dockerfile(
            github_url, 
            monitoring_tool, 
            wandb_api_key=wandb_api_key, 
            wandb_base_url=wandb_base_url, 
            wandb_project_name=wandb_project_name,
            server_ip=server_ip,
            server_port=server_port
        )
    else:
        dockerfile = await generate_server_dockerfile(github_url, monitoring_tool)

    # return web.json_response({"dockerfile": dockerfile})
    return web.Response(text=dockerfile, content_type='text/plain')
