from sagemaker.pytorch.processing import PyTorchProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker import get_execution_role

role = get_execution_role()

BUCKET='dgraeberaws-sagemaker'
S3_INPUT_PATH ='images'
S3_OUTPUT_PATH='output'
LOCAL_INPUT = '/opt/ml/processing/input/image'
LOCAL_OUTPUT='/opt/ml/processing/output/image'
pytorch_processor = PyTorchProcessor(
    framework_version='1.8',
    role=role,
    instance_type='ml.g4dn.xlarge', #ml.m4.xlarge ml.g4dn.xlarge
    instance_count=1,
    base_job_name='Lanedet-testing',
    image_uri='616260033377.dkr.ecr.us-east-1.amazonaws.com/lanedet:20220725',
)

#Run the processing job
pytorch_processor.run(
    code='tools/detect_sm3.py',
    source_dir='s3://dgraeberaws-sagemaker/lanedet/configs',
    inputs=[
        ProcessingInput(
            input_name='images',
            source=f's3://{BUCKET}/{S3_INPUT_PATH}',
            destination=LOCAL_INPUT
        )
    ],
    outputs=[
        ProcessingOutput(
            output_name='out', 
            source=LOCAL_OUTPUT,
            destination=f's3://{BUCKET}/{S3_OUTPUT_PATH}')
        
    ]
)