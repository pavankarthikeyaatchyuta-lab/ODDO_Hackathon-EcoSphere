FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build && cp -r .next/static .next/standalone/.next/static
ENV HOSTNAME=0.0.0.0
CMD ["node", ".next/standalone/server.js"]
