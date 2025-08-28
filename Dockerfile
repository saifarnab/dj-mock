# Stage 1: Build environment
FROM python:3.12-slim AS build

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Install build dependencies, upgrade pip, and bash
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-dev \
    tzdata \
    python3-dev \
    bash \
    && ln -fs /usr/share/zoneinfo/Asia/Dhaka /etc/localtime && dpkg-reconfigure -f noninteractive tzdata \
    && python3 -m pip install --upgrade pip

# Install Python dependencies
WORKDIR /app
COPY ./requirements.txt ./

# Install 'wheel' before other packages
RUN pip install --no-cache-dir wheel \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.12-slim

# Install bash and set timezone
RUN apt-get update && apt-get install -y --no-install-recommends bash libglib2.0-0 libcairo2 \
    fonts-beng \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    && ln -fs /usr/share/zoneinfo/Asia/Dhaka /etc/localtime && dpkg-reconfigure -f noninteractive tzdata \
    && python3 -m pip install --upgrade pip

# Copy the installed packages from the build stage
COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin /usr/local/bin

# Copy application files
WORKDIR /app
COPY . .

# Add and use a non-root user
RUN useradd --no-create-home --user-group --system --shell /bin/false app \
    && chown -R app:app /app
USER app

