FROM ubuntu:20.04 as chroot

# Aggiungi il percorso di installazione di Python 3 alla variabile di ambiente PATH
ENV PATH="/usr/local/bin:${PATH}"

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt-get update && apt-get install -yq --no-install-recommends python3 python3-pip python3-dev

COPY flag /
#COPY chal /home/user/
COPY dhmitm.py /home/user/
COPY requirements.txt /
#COPY  /home/user/

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/
RUN python3 -m pip install -r chroot/requirements.txt
RUN pyinstaller /chroot/home/user/dhmitm.py
RUN mv /dist /chroot/home/user
RUN chmod a+rwx /chroot/home/user/
CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/dist/dhmitm/dhmitm" 
