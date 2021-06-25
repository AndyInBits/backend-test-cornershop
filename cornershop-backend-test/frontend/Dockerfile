FROM node:12

EXPOSE 3000
ARG ENVIRONMENT
RUN printenv

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

ENV PORT 3000
# Create app directory
RUN mkdir -p /opt/cornershop/frontend
WORKDIR /opt/cornershop/frontend
# Installing dependencies
COPY frontend/package.json /opt/cornershop/frontend/
RUN npm install

# Copying source files
COPY frontend/ /opt/cornershop/frontend

# Running the app
CMD "npm" "run" "dev"
