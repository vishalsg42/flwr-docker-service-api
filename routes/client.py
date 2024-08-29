from aiohttp import web
from services.repo_validation import clone_and_validate_repo
from services.dockerfile_generator import generate_client_dockerfile, generate_client_compose_file

async def client_endpoint(request):
    data = await request.json()
    github_url = data.get('github_url')
    server_ip = data.get('server_ip')
    server_port = data.get('server_port')

    # Validate the GitHub repository
    is_valid, error_message = await clone_and_validate_repo(github_url)
    if not is_valid:
        return web.json_response({"error": error_message}, status=400)

    # Generate the Dockerfile with the correct parameters    
    dockerfile = await generate_client_dockerfile(github_url, server_ip, server_port)

    # Return the Dockerfile content as plain text
    return web.Response(text=dockerfile, content_type='text/plain')

async def client_compose_endpoint(request):
    data = await request.json()
    github_url = data.get('github_url')
    server_ip = data.get('server_ip')
    server_port = data.get('server_port')

    # Validate the GitHub repository
    is_valid, error_message = await clone_and_validate_repo(github_url)
    if not is_valid:
        return web.json_response({"error": error_message}, status=400)

    compose_file = await generate_client_compose_file(
        github_url, server_ip=server_ip, server_port=server_port
    )

    return web.Response(text=compose_file, content_type='text/plain')
