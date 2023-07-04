FROM dreamacro/clash:latest AS builder

FROM python:3.11.4-slim-bullseye

# Install proxychains
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y proxychains && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    sed -i 's/^socks4/#&/' /etc/proxychains.conf && \
    echo "socks5 127.0.0.1 7891" >> /etc/proxychains.conf && \
    echo "http 127.0.0.1 7890" >> /etc/proxychains.conf

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --index-url http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com -r requirements.txt

COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /root/.config/clash/Country.mmdb /root/.config/clash/
COPY --from=builder /clash .
COPY config.yaml /root/.config/clash/config.yaml
COPY main.py /app/main.py

RUN echo "./clash &" >> start.sh && \
    echo "proxychains uvicorn main:app --host 0.0.0.0 --port 8000" >> start.sh && \
    chmod +x start.sh

CMD ["/bin/sh", "start.sh"]
