# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM ubuntu:20.04 as chroot

ENV PATH="/usr/local/bin:${PATH}"

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt-get update && apt-get install -yq --no-install-recommends python3 python3-pip python3-dev debootstrap

RUN debootstrap --arch=amd64 focal /home/user/chroot http://archive.ubuntu.com/ubuntu/

# Copia i file dell'applicazione
COPY flag.txt /home/user/
COPY app.py /home/user/
COPY templates /home/user/templates
COPY requirements.txt /

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f
COPY --from=chroot / /chroot
COPY nsjail.cfg /home/user/


# Installa le dipendenze Python nel chroot
RUN python3 -m pip install -r chroot/requirements.txt




# Compila il file app.py
RUN pyinstaller chroot/home/user/app.py
RUN mv /dist /chroot/home/user
RUN chmod a+rwx /chroot/home/user/
RUN apt-get update && apt-get -y install curl
RUN chroot /chroot/home/user/chroot /bin/bash -c "apt-get update && apt-get install -y build-essential"

# Aggiungi la configurazione di nsjail


# Usa l'immagine base di KCTF per la fase finale



CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/dist/app/app"

