FROM python:3.11-slim

LABEL maintainer="vecesta.co@gmail.com"
LABEL description="Hardware-Aware Diffusers Studio by Vecesta.co"

WORKDIR /app

COPY pyproject.toml ./
COPY src/ ./src/
COPY fixtures/ ./fixtures/

RUN pip install --no-cache-dir -e .

EXPOSE 7860

ENTRYPOINT ["hardware-aware-diffusers-studio"]
CMD ["serve", "--port", "7860", "--host", "0.0.0.0"]
