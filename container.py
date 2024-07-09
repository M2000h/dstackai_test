import docker


class Container:
    client = docker.from_env()
    container = None

    def __init__(self, image):
        self.image = image
        self.client.images.pull(image)

    def run(self, command):
        self.container = self.client.containers.run(
            self.image,
            command=f"/bin/sh -c \"{command}\"",
            detach=True,
        )
