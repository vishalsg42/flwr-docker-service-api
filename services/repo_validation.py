import os
import tempfile
import subprocess
import asyncio

async def clone_and_validate_repo(github_url):
    temp_dir = tempfile.mkdtemp()

    try:
        # Clone the repository using git (non-blocking)
        proc = await asyncio.create_subprocess_exec(
            'git', 'clone', github_url, temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            return False, stderr.decode().strip()

        # Check if required files exist
        required_files = ['client.py', 'server.py', 'requirements.txt']
        missing_files = [file for file in required_files if not os.path.exists(os.path.join(temp_dir, file))]

        if missing_files:
            return False, f"Missing files in the repository: {', '.join(missing_files)}"
        
        return True, None

    finally:
        # Clean up the temporary directory asynchronously
        await asyncio.to_thread(subprocess.check_call, ['rm', '-rf', temp_dir])
