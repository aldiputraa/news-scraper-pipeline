# megunakan base image Python yang ringan
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements agar bisa install library
COPY requirements.txt .

# Install library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file proyek ke dalam container
COPY . .

# mejalankan script saat container dijalankan
CMD ["python", "scraper.py"]
