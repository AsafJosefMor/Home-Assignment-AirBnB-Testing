# Base image: python:3.10-slim has minimal footprint and active Python support
FROM python:3.10-slim

# Copy the project into our image
WORKDIR /test-runner
COPY . /test-runner

# Required packages to run Chromium with Playwright
# libnss3, libxss1, libasound2   - Dependencies for Chromium internals and audio
# libgbm1, libgtk-3-0            - Required for headless and headed rendering
# libatk-bridge2.0-0             - Accessibility bridge (stable UI interaction)
RUN apt-get update && \
    apt-get install -y libnss3 libatk-bridge2.0-0 libxss1 libasound2 libgbm1 libgtk-3-0 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && pip install . && \
    python -m playwright install --with-deps

# Run the tests
# - Fail if a command fails, undefined variable is used or failure in piped commands
ENTRYPOINT ["/bin/bash", "-euo", "pipefail", "-c"]
CMD ["pytest tests/ --suite-timeout=$SUITE_TIMEOUT_SEC"]