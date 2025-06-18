FROM odoo:18.0

# Set DEBIAN_FRONTEND to noninteractive to avoid prompts during package installation
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wkhtmltopdf \
    python3-pip \
    python3-dev \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libffi-dev \
    postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# If you have custom Python dependencies for your addons, uncomment and use requirements.txt
# COPY requirements.txt /tmp/requirements.txt
# RUN pip3 install --no-cache-dir -r /tmp/requirements.txt \
#     && rm /tmp/requirements.txt

# Create directory for custom addons
RUN mkdir -p /mnt/extra-addons && \
    chown odoo:odoo /mnt/extra-addons

# Copy Odoo configuration template
COPY ./config/odoo.conf.template /etc/odoo/odoo.conf.template
RUN chown odoo:odoo /etc/odoo/odoo.conf.template

# Copy and set permissions for the entrypoint script
COPY ./entrypoint.sh /usr/local/bin/dfr_entrypoint.sh
RUN chmod +x /usr/local/bin/dfr_entrypoint.sh && \
    chown odoo:odoo /usr/local/bin/dfr_entrypoint.sh

USER odoo

EXPOSE 8069
EXPOSE 8072 # Longpolling port

ENTRYPOINT ["/usr/local/bin/dfr_entrypoint.sh"]
CMD ["odoo"]