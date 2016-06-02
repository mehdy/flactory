FROM python:3
MAINTAINER Mehdy Khoshnoody "mehdy.Khoshnoody@gmail.com"

ENV DOCKERFILE_VERSION 0.1.0

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update
RUN apt-get install -y openssh-server
RUN apt-get install -y vim
EXPOSE 22

RUN mkdir /var/run/sshd
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN mkdir /project
WORKDIR /project/

CMD ["/usr/sbin/sshd", "-D"]