FROM python:3.11-slim

# HF Spaces requires a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy the package
COPY --chown=user redteam_env/ /app/redteam_env/

# Install dependencies directly (no uv needed)
RUN pip install --no-cache-dir \
    "openenv-core[core]>=0.2.2" \
    "fastapi>=0.115.0" \
    "pydantic>=2.0.0" \
    "uvicorn>=0.24.0" \
    "requests>=2.31.0"

# HF Spaces needs port 7860
CMD ["uvicorn", "redteam_env.server.app:app", "--host", "0.0.0.0", "--port", "7860"]
