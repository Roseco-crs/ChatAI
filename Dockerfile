FROM python:3.10-slim

# Hugging Face runs on UID 1000
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user/app

# Install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY --chown=user . .

# IMPORTANT: Use --server.address and --server.port
# Do NOT use --host or -p
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
