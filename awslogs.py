import boto3


class LogsUploader:
    """AWS CloudWatch wrapper."""

    def __init__(
            self,
            region: str,
            aws_access_key_id: str,
            aws_secret_access_key: str,
            log_group: str,
            log_stream: str
    ):
        """
        Init AWS CloudWatch logger.
        Args:
            region: reg
            aws_access_key_id: AWS access key ID.
            aws_secret_access_key: AWS secret access key.
            log_group: A name of an AWS CloudWatch group.
            log_stream: A name of an AWS CloudWatch stream.
        """
        self.region = region
        self.log_group = log_group
        self.log_stream = log_stream
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region
        )
        self.logs_client = self.session.client('logs')
        self.create_group()
        self.create_stream()
        self.response = self.logs_client.describe_log_streams(
            logGroupName=self.log_group,
            logStreamNamePrefix=self.log_stream
        )
        self.sequence_token = self.response['logStreams'][0].get('uploadSequenceToken')

    def create_group(self):
        try:
            self.logs_client.create_log_group(
                logGroupName=self.log_group
            )
            print(f'Log group "{self.log_group}" created successfully')
        except Exception:
            pass

    def create_stream(self):
        try:
            self.logs_client.create_log_stream(
                logGroupName=self.log_group,
                logStreamName=self.log_stream
            )
            print(f'Log stream "{self.log_stream}" created successfully in log group "{self.log_group}"')
        except Exception:
            pass

    def upload_logs(self, logs: str, timestamp: int):
        """
        AWS CloudWatch logger uploader.
        Args:
            logs: Log text.
            timestamp: Log timestamp.
        """
        log_events = [
            {
                'timestamp': timestamp * 1000,
                'message': logs
            }
        ]
        self.logs_client.put_log_events(
            logGroupName=self.log_group,
            logStreamName=self.log_stream,
            logEvents=log_events,
            sequenceToken=self.sequence_token
        )
