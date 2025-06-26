FROM node:20-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies including peer dependencies
RUN npm install -g npm@latest && \
    npm install && \
    npm install -D tailwindcss postcss autoprefixer arg

# Copy the rest of the application
COPY . .

# Generate Tailwind and PostCSS config files
RUN npx tailwindcss init -p

EXPOSE 5173

ENV VITE_HOST=0.0.0.0
ENV PATH=/app/node_modules/.bin:$PATH

CMD ["npm", "run", "dev", "--", "--host"]