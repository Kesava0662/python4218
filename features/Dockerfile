FROM python:3.11-slim-bullseye
 
# ----------------------
# Set working directory
# ----------------------
WORKDIR /app
 
# ----------------------
# System dependencies
# ----------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip gnupg xvfb x11vnc novnc websockify \
    xfce4 xfce4-terminal dbus-x11 \
    libnss3 libxss1 libappindicator3-1 libatk-bridge2.0-0 \
    libatk1.0-0 libdrm2 libgbm1 libgtk-3-0 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 libxtst6 \
    fonts-liberation libasound2 \
    python3-tk python3-dev build-essential \
    pkg-config default-libmysqlclient-dev mariadb-client \
&& rm -rf /var/lib/apt/lists/*
 
# ----------------------
# Install Google Chrome
# ----------------------
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | tee /etc/apt/keyrings/google.asc && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google.asc] http://dl.google.com/linux/chrome/deb/ stable main" \
> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*
 
# ----------------------
# Install ChromeDriver (matching Chrome)
# ----------------------
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) && \
    CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION}") && \
    wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromed… -O chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64 chromedriver.zip
 
# ----------------------
# Python dependencies
# ----------------------
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
 
RUN pip install --no-cache-dir Appium-Python-Client
 
# ----------------------
# Copy project files
# ----------------------
COPY . .
 
# ----------------------
# Expose noVNC
# ----------------------
EXPOSE 6080 5900
 
# ----------------------
# Startup script
# ----------------------
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh
 
# ----------------------
# Default CMD
# ----------------------
CMD ["/startup.sh"]
