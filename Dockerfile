FROM python:3.6-alpine3.6

ADD kubelogctl.py /kubelogctl.py

RUN apk add --update curl \
  && rm -rf /var/cache/apk/* \
  && LATEST_VERSION=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt) \
  && echo "Downloading kubectl ${LATEST_VERSION}..." \
  && curl -s -LO https://storage.googleapis.com/kubernetes-release/release/${LATEST_VERSION}/bin/linux/amd64/kubectl \
  && chmod +x ./kubectl \
  && mv ./kubectl /usr/local/bin/

ENTRYPOINT ["python", "/kubelogctl.py"]
