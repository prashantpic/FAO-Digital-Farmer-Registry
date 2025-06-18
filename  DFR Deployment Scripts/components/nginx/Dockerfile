FROM nginx:stable-alpine

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration templates
COPY ./config/nginx.conf.template /etc/nginx/nginx.conf.template
COPY ./config/sites-available/dfr.conf.template /etc/nginx/sites-available/dfr.conf.template

# Create SSL directory (certificates will be mounted here as volumes)
RUN mkdir -p /etc/nginx/ssl/

# Copy Nginx entrypoint script and make it executable
COPY ./nginx_entrypoint.sh /usr/local/bin/nginx_entrypoint.sh
RUN chmod +x /usr/local/bin/nginx_entrypoint.sh

# Install gettext for envsubst utility
RUN apk add --no-cache gettext

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["/usr/local/bin/nginx_entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]