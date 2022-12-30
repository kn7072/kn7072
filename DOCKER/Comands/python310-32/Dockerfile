FROM centos

LABEL maintainer="sg.chernov"
WORKDIR /temp

RUN echo $(pwd)
COPY ./requirements.txt requirements.txt

WORKDIR /etc/yum.repos.d/
# RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

RUN yum update -y && yum -y install libffi-devel vim wget make yum-utils gcc openssl-devel bzip2-devel 
RUN yum -y groupinstall "Development Tools"
RUN yum install -y libgcc.i686 glibc-devel.i686 glibc.i686 zlib-devel.i686 readline-devel.i686 gdbm-devel.i686 openssl-devel.i686 ncurses-devel.i686 tcl-devel.i686 bzip2-devel.i686 libxslt-devel libxml2-devel


WORKDIR /temp
RUN wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz
RUN tar xzf Python-3.11.1.tgz
RUN cd Python-3.11.1

WORKDIR /temp/Python-3.11.1
RUN echo $(pwd)

RUN BASECFLAGS=-m32 LDFLAGS=-m32 CFLAGS=-m32 ./configure --prefix=/opt/python32 --enable-optimizations --enable-shared 
# LD_RUN_PATH=/opt/python32/lib
RUN make -j "$(nproc)"
RUN make altinstall

RUN echo "/opt/python32/lib/" >> /etc/ld.so.conf.d/python.conf && ldconfig

CMD /bin/bash