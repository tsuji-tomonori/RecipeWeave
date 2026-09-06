FROM node:24-bookworm-slim
WORKDIR /application
COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN npm ci --prefix frontend
COPY frontend ./frontend
COPY tools/build-service-docs.mjs ./tools/
COPY docs ./docs
RUN node frontend/scripts/prepare-ocr.mjs
WORKDIR /application/frontend
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
