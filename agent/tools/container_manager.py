import docker
import os
from docker.errors import NotFound, APIError

client = docker.from_env()

IMAGE_NAME = "demo-app:latest"
CONTAINER_NAME = "demo-container"


def get_container():
    """Safely get container or return None"""
    try:
        return client.containers.get(CONTAINER_NAME)
    except NotFound:
        return None


def run_container():
    """Run container safely (replace old if exists)"""
    try:
        container = get_container()

        if container:
            print("Container already exists. Recreating...")
            safe_remove(container)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.abspath(os.path.join(base_dir, "../logs"))

        container = client.containers.run(
            IMAGE_NAME,
            name=CONTAINER_NAME,
            ports={"8000/tcp": 8000},
            mem_limit="500m",
            nano_cpus=500_000_000,
            environment={"LOG_DIR": "/app/logs"},
            volumes={
                logs_dir: {
                    "bind": "/app/logs",
                    "mode": "rw",
                }
            },
            detach=True,
        )

        print(f"Started container: {container.id}")

    except APIError as e:
        print(f"Failed to start container: {e}")


def safe_stop(container):
    """Stop only if running"""
    try:
        container.reload()
        if container.status == "running":
            container.stop()
            print(f"Stopped container: {container.id}")
        else:
            print("Container already stopped")
    except APIError as e:
        print(f"Error stopping container: {e}")


def safe_remove(container):
    """Remove container safely (stop first if needed)"""
    try:
        container.reload()
        if container.status == "running":
            print("Stopping running container before removal...")
            container.stop()

        container.remove()
        print(f"Removed container: {container.id}")

    except APIError as e:
        print(f"Error removing container: {e}")


def stop_container():
    container = get_container()
    if not container:
        print("Container not found")
        return

    safe_stop(container)


def remove_container():
    container = get_container()
    if not container:
        print("Container not found")
        return

    safe_remove(container)


def restart_container():
    print("Restarting container...")
    remove_container()
    run_container()
    return True


def clear_cache():
    """
    Clear cache = remove container (fresh next run)
    """
    print("Clearing container cache...")
    remove_container()
    return True


if __name__ == "__main__":
    restart_container()
