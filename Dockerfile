FROM quay.io/jupyter/minimal-notebook
USER root
RUN pip install pandas s3fetch
RUN conda install -y -c https://conda.anaconda.org/plotly plotly
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
COPY --chmod=755 run-init.sh /tmp
ENTRYPOINT [ "/tmp/run-init.sh" ]