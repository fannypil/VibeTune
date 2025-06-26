FROM node:20-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Clean install dependencies
RUN npm cache clean --force && \
    npm install --legacy-peer-deps && \
    npm install @heroicons/react react-router-dom lucide-react


# Copy the rest of the application
COPY . .

# Initialize Tailwind
RUN npx tailwindcss init -p

EXPOSE 5173

ENV VITE_HOST=0.0.0.0
ENV PATH=/app/node_modules/.bin:$PATH

CMD ["npm", "run", "dev", "--", "--host"]