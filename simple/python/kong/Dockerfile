FROM kong

# get ContainerPilot release
ENV CONTAINERPILOT_VERSION 3.8.0
RUN export CP_SHA1=84642c13683ddae6ccb63386e6160e8cb2439c26 \
    && curl -Lso /tmp/containerpilot.tar.gz \
         "https://github.com/joyent/containerpilot/releases/download/${CONTAINERPILOT_VERSION}/containerpilot-${CONTAINERPILOT_VERSION}.tar.gz" \
    && echo "${CP_SHA1}  /tmp/containerpilot.tar.gz" | sha1sum -c \
    && tar zxf /tmp/containerpilot.tar.gz -C /bin \
    && rm /tmp/containerpilot.tar.gz

# add ContainerPilot configuration
COPY containerpilot.json5 /etc/containerpilot.json5
ENV CONTAINERPILOT=/etc/containerpilot.json5

# CMD ping 8.8.8.8
CMD /bin/containerpilot

EXPOSE 8000 8443 8001 7946