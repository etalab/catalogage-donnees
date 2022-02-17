FROM node:16 AS base
WORKDIR /app/
COPY ./client/package.json ./client/package-lock.json ./client/

FROM base AS dependencies
RUN cd client && npm ci

FROM base AS release
COPY --from=dependencies /app/client/node_modules ./client/node_modules
COPY . .
EXPOSE 3000
WORKDIR /app/client
CMD ["npm", "run", "dev", "--", "--host"]
