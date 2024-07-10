# Dstack test task

The program creates a Docker container using the given Docker image name, and the given bash command.
The program handles the output logs of the container and send them to the given AWS CloudWatch group/stream
using the given AWS credentials. If the corresponding AWS CloudWatch group or stream does not exist,
it creates it using the given AWS credentials

## Setup

1. Install python
2. Install Docker
3. Run `pip install -r requirments` 

## Run

* MacOS/Linux

`python main.py --docker-image python --aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1 --aws-access-key-id ... --aws-secret-access-key ... --aws-region us-west-2 --bash-command "pip install pip -U && pip install tqdm && python -c $'import time\nprint(123)'"`

* Windows

`python main.py --docker-image python --aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1 --aws-access-key-id ... --aws-secret-access-key ... --aws-region us-west-2 --bash-command "pip install pip -U && pip install tqdm && python -c 'import time;print(123)'"`

*Notice:* On Windows there are problems with escaping, so it’s better to use `;` instead of `\n` and spaces instead of `\t`

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