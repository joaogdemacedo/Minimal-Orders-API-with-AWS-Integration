from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from pathlib import Path
from constructs import Construct

class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the Orders table
        orders_table = dynamodb.Table(
            self,
            "OrdersTable",
            table_name="Orders",  # This name is what your FastAPI app uses
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # Good for dev/testing
            removal_policy=RemovalPolicy.DESTROY  # Auto-delete on `cdk destroy`
        )
        
        
        # Lambda function for FastAPI app
        fastapi_lambda = PythonFunction(
            self,
            "FastApiHandler",
            entry = str((Path(__file__).resolve().parents[2] / "orders_api" / "app")),  # path to app folder containing main.py
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="main_lambda.py",        # Your FastAPI entry file
            handler="handler",      # The variable name in main.py: `handler = Mangum(app)`
        )
        
        orders_table.grant_read_write_data(fastapi_lambda)

        # API Gateway to expose the Lambda publicly
        api = apigateway.LambdaRestApi(
            self,
            "FastApiEndpoint",
            handler=fastapi_lambda,
            proxy=True,
        )