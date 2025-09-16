FROM quay.io/jupyter/minimal-notebook:python-3.12

# Copy the Conda environment file into the container
COPY ./requirements/environment.yml /tmp/environment.yml

# Install the dependencies from the environment file
RUN mamba env update -n base -f /tmp/environment.yml && \
    mamba clean --all -y && \
    fix-permissions /opt/conda && \
    fix-permissions /home/$NB_USER
