# Use a lightweight Nginx image to serve a placeholder page
FROM nginx:stable-alpine

# Copy a simple placeholder HTML file to the Nginx HTML directory
RUN echo "<h1>Frontend is under construction</h1>" > /usr/share/nginx/html/index.html

# Expose the port Nginx will serve on
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]