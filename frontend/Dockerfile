FROM node:20-slim

WORKDIR /app

RUN adduser --disabled-password --gecos "" --uid 10001 appuser

COPY package.json ./
RUN npm install --only=production

COPY server.js ./
COPY public ./public

USER appuser

ENV PORT=3000
EXPOSE $PORT

CMD ["node", "server.js"]
