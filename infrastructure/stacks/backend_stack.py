from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    BundlingOptions,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam,
)
from constructs import Construct
import os


class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        events_table = dynamodb.Table(
            self,
            "EventsTable",
            partition_key=dynamodb.Attribute(
                name="eventId", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Lambda Function
        backend_lambda = lambda_.Function(
            self,
            "EventsAPIFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="lambda_handler.handler",
            architecture=lambda_.Architecture.ARM_64,
            code=lambda_.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "../../backend"),
                bundling=BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_11.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -r *.py /asset-output/",
                    ],
                ),
            ),
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                "DYNAMODB_TABLE_NAME": events_table.table_name,
            },
        )

        # Grant Lambda permissions to access DynamoDB
        events_table.grant_read_write_data(backend_lambda)

        # API Gateway
        api = apigateway.LambdaRestApi(
            self,
            "EventsAPI",
            handler=backend_lambda,
            proxy=True,
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=[
                    "Content-Type",
                    "X-Amz-Date",
                    "Authorization",
                    "X-Api-Key",
                    "X-Amz-Security-Token",
                ],
            ),
            deploy_options=apigateway.StageOptions(
                stage_name="prod",
                throttling_rate_limit=100,
                throttling_burst_limit=200,
            ),
        )

        # Outputs
        CfnOutput(
            self,
            "APIEndpoint",
            value=api.url,
            description="API Gateway endpoint URL",
        )

        CfnOutput(
            self,
            "DynamoDBTableName",
            value=events_table.table_name,
            description="DynamoDB table name",
        )

        CfnOutput(
            self,
            "LambdaFunctionName",
            value=backend_lambda.function_name,
            description="Lambda function name",
        )
