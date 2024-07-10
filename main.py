import argparse
import logging
import docker
import time

from awslogs import LogsUploader
from container import Container

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Arguments")
parser.add_argument('--docker-image', type=str, required=True, help="A name of a Docker image")
parser.add_argument('--bash-command', type=str, required=True, help="A bash command (to run inside the Docker image)")
parser.add_argument('--aws-cloudwatch-group', type=str, required=True, help="A name of an AWS CloudWatch group")
parser.add_argument('--aws-cloudwatch-stream', type=str, required=True, help="A name of an AWS CloudWatch stream")
parser.add_argument('--aws-access-key-id', type=str, required=True, help="An AWS access key ID")
parser.add_argument('--aws-secret-access-key', type=str, required=True, help="An AWS secret access key")
parser.add_argument('--aws-region', type=str, required=True, help="A name of an AWS region")
args = parser.parse_args()


def run():
    container = Container(args.docker_image)
    container.run(args.bash_command)

    logger.info(f"Container {container.container.id} is running")

    logsUploader = LogsUploader(
        args.aws_region,
        args.aws_access_key_id,
        args.aws_secret_access_key,
        args.aws_cloudwatch_group,
        args.aws_cloudwatch_stream
    )

    last_ts = int(time.time())
    while True:
        container.container.reload()
        container_status = container.container.status
        try:
            now = int(time.time())
            logs = container.container.logs(since=last_ts, until=now).decode("utf-8")
            last_ts = now
            if logs:
                logsUploader.upload_logs(logs, now)
                logger.info(logs)
        except docker.errors.APIError as e:
            if "500 Server Error" in str(e):
                # Container is starting
                continue
            if "409 Client Error" in str(e):
                # Container has stopped
                break
        time.sleep(1)
        if container_status == "exited":
            break
    logger.info(f"Container {container.container.id} has stopped")


if __name__ == "__main__":
    run()
