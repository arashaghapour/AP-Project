# ==========================================
# 1. Base Runtime Environment
# ==========================================
FROM python:3.10-slim

# تنظیمات بهینه پایتون برای کانتینر
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# پوشه کاری اصلی کانتینر
WORKDIR /app

# نصب ابزار curl جهت بررسی وضعیت سلامت (Healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# کپی و نصب نیازمندی‌ها (جهت استفاده از کش لایه‌ها)
COPY requirements.txt .
RUN pip install -r requirements.txt

# کپی کردن تمام فایل‌ها و پوشه‌ها (شامل کدهای src و پوشه تصاویر static) به داخل کانتینر
COPY . .

# پورت پیش‌فرض پروژه
EXPOSE 8000

# اجرای وب‌سرور از پوشه ریشه با ارجاع به ماژول داخلی src.main
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]