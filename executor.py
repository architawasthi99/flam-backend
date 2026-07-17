import subprocess

def execute_command(command: str):

    try:

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }

    except Exception as e:

        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "code": -1
        }
