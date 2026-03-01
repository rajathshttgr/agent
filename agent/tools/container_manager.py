import docker
import os

client = docker.from_env()

IMAGE_NAME = "demo-app:latest"
CONTAINER_NAME = "demo-container"


def run_container():
    try:
        old = client.containers.get(CONTAINER_NAME)
        old.stop()
        old.remove()
    except docker.errors.NotFound:
        pass

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOGS_DIR = os.path.abspath(os.path.join(BASE_DIR, "../logs"))

    container = client.containers.run(
        IMAGE_NAME,
        name=CONTAINER_NAME,
        ports={"8000/tcp": 8000},
        mem_limit="500m",
        nano_cpus=500_000_000,
        environment={"LOG_DIR": "/app/logs"},
        volumes={
            LOGS_DIR: {
                "bind": "/app/logs",
                "mode": "rw",
            }
        },
        detach=True,
    )

    print("Started container:", container.id)


def stop_container():
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.stop()
        print("Stopped container:", container.id)
    except docker.errors.NotFound:
        print("Container not found")

    print("Stopped container:", container.id)


def remove_container():
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.remove()
        print("Removed container:", container.id)
    except docker.errors.NotFound:
        print("Container not found")


if __name__ == "__main__":
    stop_container()
    remove_container()
    run_container()
