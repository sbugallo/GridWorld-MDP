FROM continuumio/miniconda3:4.7.10

LABEL maintainer="Sergio Bugallo <sergiobugalloenjamio@gmail.com>"

RUN bash -c 'mkdir -p /gridworld/envs'
WORKDIR /gridworld

COPY ./envs/prod.yml /gridworld/envs/prod.yml
RUN conda env create -f /gridworld/envs/prod.yml
RUN echo '. activate gridworld' >> ~/.bashrc

COPY . /gridworld
RUN bash -c '/opt/conda/envs/gridworld/bin/python /gridworld/setup.py install'

CMD [ "/bin/bash" ]