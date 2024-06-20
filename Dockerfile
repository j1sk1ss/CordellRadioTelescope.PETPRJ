FROM fedora:38

LABEL author=j1sk1ss

WORKDIR /home

RUN dnf -y update
RUN dnf -y install python3 python3-pip rtl-sdr
RUN pip3 install pip pyrtlsdr numpy overrides pyfiglet serial

RUN mkdir /home/CordellRSA

COPY .. /home/CordellRSA