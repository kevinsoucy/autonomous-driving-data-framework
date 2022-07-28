# SageMaker PyTorch image - https://github.com/aws/deep-learning-containers/blob/master/available_images.md
FROM 763104351884.dkr.ecr.eu-central-1.amazonaws.com/pytorch-inference:1.8.1-gpu-py36-cu111-ubuntu18.04


WORKDIR /
RUN git clone https://github.com/turoad/lanedet.git
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN wget https://github.com/Turoad/lanedet/releases/download/1.0/laneatt_r18_tusimple.zip
RUN unzip laneatt_r18_tusimple.zip
RUN python tools/detect.py configs/laneatt/resnet18_tusimple.py --img images\
          --load_from laneatt_r18_tusimple.pth --savedir ./vis

#ENV PYTHONUNBUFFERED=TRUE
#ENV PYTHONDONTWRITEBYTECODE=TRUE
#ENV PATH="/opt/program:${PATH}"
#ENV MODEL_PATH="/opt/ml/model"
#
## Set up the program in the image
#COPY algorithm_code /opt/program
#WORKDIR /opt/program
# /opt/ml and all subdirectories are utilized by SageMaker, use the /code subdirectory to store your user code.
ENTRYPOINT ["python3", "detect_lanes.py"]