# Dstack test task

The program creates a Docker container using the given Docker image name, and the given bash command.
The program handles the output logs of the container and send them to the given AWS CloudWatch group/stream
using the given AWS credentials. If the corresponding AWS CloudWatch group or stream does not exist,
it creates it using the given AWS credentials

## Setup

1. Install Python
2. Install Docker
3. Run `pip install -r requirements.txt` 

## Run

Run script with following command:

`python main.py --docker-image python --aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1 --aws-access-key-id ... --aws-secret-access-key ... --aws-region us-west-2 --bash-command "pip install pip -U && pip install tqdm && python -c "python -c 'import time;print(123);time.sleep(5)'""`

**Notice 1:** There are problems with escaping, so it’s better to use `;` instead of `\n` and spaces instead of `\t`

**Notice 2:** In some cases there are problems with pulling the docker image, in which case you need to download 
it manually: `docker pull python`

**Notice 3:** The script supports creating new groups and streams, but apparently due to access restrictions, recording 
only works in test-task-group-1 and test-task-stream-1

## Args

| Argument                  | Description                                     |
|---------------------------|-------------------------------------------------|
| `--docker-image`          | A name of a Docker image                        |
| `--bash-command`          | A bash command (to run inside the Docker image) |
| `--aws-cloudwatch-group`  | A name of an AWS CloudWatch group               |
| `--aws-cloudwatch-stream` | A name of an AWS CloudWatch stream              |
| `--aws-access-key-id`     | An AWS access key ID                            |
| `--aws-secret-access-key` | An AWS secret access key                        |
| `--aws-region`            | A name of an AWS region                         |


## Notice

I used python library `boto3` instead of docker default log driver,
because on Windows AWS CloudWatch doesn't work well.