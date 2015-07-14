#FROM centos:centos6
FROM centos:centos7
#MAINTAINER Naoya Murakami <naoya@createfield.com>
MAINTAINER Kensuke Mitsuzawa <kensuke.mit@gmail.com>

# set root user setting
RUN echo 'root:docker' | chpasswd
RUN echo "root    ALL=(ALL)       ALL" >> /etc/sudoers
RUN echo "#Defaults      requiretty" >> /etc/sudoers


#CMD "sh" "-c" "echo nameserver 8.8.8.8 > /etc/resolv.conf"
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

RUN yum install -y wget tar vi bzip2
RUN yum install -y gcc make gcc-c++
RUN yum install -y perl perl-devel

# dev tools
RUN yum -y install git vim
RUN yum -y install passwd openssh openssh-server openssh-clients sudo
RUN yum -y install zip
RUN yum -y install unzip
RUN yum -y install curl xz
RUN yum -y install python-devel.x86_64 

#RUN yum install -y nkf
RUN yum localinstall -y http://mirror.centos.org/centos/6/os/x86_64/Packages/nkf-2.0.8b-6.2.el6.x86_64.rpm

# for debian
#RUN apt-get update
#RUN apt-get install locales
#RUN apt-get install -y wget tar vim nkf bzip2
#RUN apt-get install -y gcc make g++
#RUN apt-get install -y perl libperl-dev

# Mecab
RUN wget http://mecab.googlecode.com/files/mecab-0.996.tar.gz
RUN tar -xzf mecab-0.996.tar.gz
RUN cd mecab-0.996; ./configure --enable-utf8-only; make; make install; ldconfig

# Ipadic
RUN wget http://mecab.googlecode.com/files/mecab-ipadic-2.7.0-20070801.tar.gz
RUN tar -xzf mecab-ipadic-2.7.0-20070801.tar.gz
RUN cd mecab-ipadic-2.7.0-20070801; ./configure --with-charset=utf8; make; make install
RUN echo "dicdir = /usr/local/lib/mecab/dic/ipadic" > /usr/local/etc/mecabrc

# Ipadic_model
RUN wget http://mecab.googlecode.com/files/mecab-ipadic-2.7.0-20070801.model.bz2
RUN bzip2 -d mecab-ipadic-2.7.0-20070801.model.bz2
#RUN iconv -f EUCJP -t UTF-8 mecab-ipadic-2.7.0-20070801.model -o mecab-ipadic-2.7.0-20070801.model
RUN nkf --overwrite -Ew mecab-ipadic-2.7.0-20070801.model
RUN sed -i -e "s/euc-jp/utf-8/g" mecab-ipadic-2.7.0-20070801.model

# MeCab python binding
COPY ./dockerfiles/mecab-python-0.996.tar.gz /
RUN tar -xvf /mecab-python-0.996.tar.gz
WORKDIR mecab-python-0.996
RUN python2.7 setup.py build
RUN python2.7 setup.py install
WORKDIR /
RUN rm -rf mecab-python-0.996.tar.gz

# Mecab-perl
RUN wget http://mecab.googlecode.com/files/mecab-perl-0.996.tar.gz
RUN tar -xzf mecab-perl-0.996.tar.gz
RUN cd mecab-perl-0.996 ;perl Makefile.PL; make ;make install;
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/mecab.conf
RUN ldconfig

# TermExtract
RUN wget http://gensen.dl.itc.u-tokyo.ac.jp/soft/TermExtract-4_10.tar.gz
RUN tar -xzf TermExtract-4_10.tar.gz
RUN nkf --overwrite -Ew /TermExtract-4_10/TermExtract/MeCab.pm
RUN cd TermExtract-4_10 ;perl Makefile.PL; make ;make install;

# Add perl script
ADD ./dockerfiles/termextract_mecab_custom.pl /usr/local/bin/termextract_mecab.pl
RUN chmod 755 /usr/local/bin/termextract_mecab.pl

VOLUME ["/var/lib/termextract"]

COPY ./dockerfiles/pre_filter.txt /var/lib/termextract/
COPY ./dockerfiles/post_filter.txt /var/lib/termextract/

# Clean up
RUN rm -rf mecab-0.996.tar.gz*
RUN rm -rf mecab-ipadic-2.7.0-20070801.tar.gz*
RUN rm -rf mecab-perl-0.996.tar.gz* 
RUN rm -rf TermExtract-4_10.tar.gz*

# neologd dictionary
RUN wget --no-check-certificate https://github.com/neologd/mecab-ipadic-neologd/tarball/master -O mecab-ipadic-neologd.tar
RUN tar -xvf mecab-ipadic-neologd.tar
RUN rm mecab-ipadic-neologd.tar
RUN mv neologd-mecab-ipadic-neologd-* neologd-mecab-ipadic-neologd
RUN cd neologd-mecab-ipadic-neologd && ( echo yes | ./bin/install-mecab-ipadic-neologd )
RUN echo "探偵ナイトスクープはおもしろい" | mecab -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/

# set new directories
RUN mkdir /analysis_data
RUN chmod 777 /analysis_data

RUN mkdir /testFiles
COPY ./dockerfiles/resources/* /testFiles/
RUN chmod 777 -R /testFiles

# copy python modules
RUN mkdir /analysis_code
COPY ./dockerfiles/python_modules/*py /analysis_code/
RUN touch /analysis_data/termExtractDict.csv
RUN chmod 777 -R /analysis_code

# make settings directory
RUN mkdir /settings
COPY ./dockerfiles/settings/* /settings/
RUN chmod 777 /settings

# -----------------------------------------------------
# if you need ssh connection please execute without comment
# Add script for ssh
#RUN yum -y install initscripts MAKEDEV
#RUN yum check
#RUN yum -y update
#RUN yum -y install openssh-server

#RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
#RUN sed -ri 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config

#RUN useradd docker
#RUN echo 'docker:docker' | chpasswd
#RUN echo "docker    ALL=(ALL)       ALL" >> /etc/sudoers

#RUN sed -ri 's/^#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config

# ssh setting
#EXPOSE 22
#RUN sed -i -e 's/UsePrivilegeSeparation.*$/UsePrivilegeSeparation no/g' /etc/ssh/sshd_config
#CMD /usr/sbin/sshd -D
