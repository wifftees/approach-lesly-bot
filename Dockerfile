FROM node:20-slim AS frontend
WORKDIR /app/miniapp
COPY miniapp/package*.json ./
RUN npm ci
COPY miniapp/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot/ ./bot/
COPY --from=frontend /app/miniapp/dist ./miniapp/dist
CMD ["python", "-m", "bot.main"]
