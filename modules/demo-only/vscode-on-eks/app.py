# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import os

import aws_cdk
import boto3
from aws_cdk import App

from stack import VSCodeOnEKS

account = os.environ["CDK_DEFAULT_ACCOUNT"]
region = os.environ["CDK_DEFAULT_REGION"]
partition = os.getenv("AWS_PARTITION", "aws")


deployment_name = os.getenv("ADDF_DEPLOYMENT_NAME", "")
module_name = os.getenv("ADDF_MODULE_NAME", "")


def _param(name: str) -> str:
    return f"ADDF_PARAMETER_{name}"


eks_cluster_name = os.getenv(_param("EKS_CLUSTER_NAME"), "")
eks_admin_role_arn = os.getenv(_param("EKS_CLUSTER_ADMIN_ROLE_ARN"), "")
eks_oidc_arn = os.getenv(_param("EKS_OIDC_ARN"), "")

secrets_manager_name = os.getenv(_param("SECRETS_MANAGER_NAME"), "")

client = boto3.client("secretsmanager")
secret_arn = f"arn:{partition}:secretsmanager:{region}:{account}:secret:{secrets_manager_name}"
secrets_json = json.loads(client.get_secret_value(SecretId=secret_arn).get("SecretString"))
vscode_password = secrets_json["password"]

app = App()

stack = VSCodeOnEKS(
    scope=app,
    id=f"addf-{deployment_name}-{module_name}",
    env=aws_cdk.Environment(
        account=account,
        region=region,
    ),
    deployment=deployment_name,
    module=module_name,
    eks_admin_role_arn=eks_admin_role_arn,
    eks_oidc_arn=eks_oidc_arn,
    eks_cluster_name=eks_cluster_name,
    vscode_password=vscode_password,
)


app.synth(force=True)
