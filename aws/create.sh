#!/bin/bash

aws cloudformation create-stack --stack-name social-vpc --template-body file://./vpc.yaml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-vpc --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-vpc --profile=econstrucao

aws cloudformation create-stack --stack-name social-roles  --capabilities CAPABILITY_NAMED_IAM --template-body file://./roles.yaml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-roles --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-roles --profile=econstrucao

aws cloudformation create-stack --stack-name social-zone --template-body file://./zone.yaml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-zone --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-zone --profile=econstrucao

aws cloudformation create-stack --stack-name social-cluster --template-body file://./cluster.yaml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-cluster --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-cluster --profile=econstrucao

aws cloudformation create-stack --stack-name social-loadbalancer --template-body file://./loadbalancer.yaml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-loadbalancer --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-loadbalancer --profile=econstrucao

aws cloudformation create-stack --stack-name social-rds-aurora --template-body file://./aurora.yaml \
    --parameters ParameterKey=AuroraPassword,ParameterValue=$(openssl rand -base64 16) \
    --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-rds-aurora --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-rds-aurora --profile=econstrucao

aws cloudformation create-stack --stack-name social-cache --template-body file://./cache.yaml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-cache --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-cache --profile=econstrucao

aws cloudformation create-stack --stack-name social-api-domain --template-body file://./services/api-domain.yml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-api-domain --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-api-domain --profile=econstrucao

aws cloudformation create-stack --stack-name social-secrets --template-body file://./secrets.yaml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-secrets --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-secrets --profile=econstrucao

aws cloudformation create-stack --stack-name social-api-service --template-body file://./services/api-service.yaml \
    --parameters ParameterKey=ImageTag,ParameterValue=master \
    --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-api-service --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-api-service --profile=econstrucao


aws cloudformation create-stack --stack-name social-bastion --capabilities CAPABILITY_NAMED_IAM \
    --template-body file://./services/bastion.yaml --profile=econstrucao
aws cloudformation wait stack-create-complete --stack-name social-bastion --profile=econstrucao
aws cloudformation describe-stacks --stack-name social-bastion --profile=econstrucao