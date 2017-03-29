FROM pymc/pymc3

MAINTAINER Alex Tong <alexanderytong@gmail.com>

USER root

RUN apt-get update --fix-missing && \
    apt-get install -y libav-tools && \
    apt-get install -y --allow-unauthenticated git g++ && \
    apt-get clean && \
    pip install git+https://github.com/pymc-devs/pymc3 && \
    rm -rf /var/lib/apt/lists/* $HOME/.c*

USER $NB_USER

ENV XDG_CACHE_HOME /home/$NB_USER/.cache/
ENV MPLBACKEND=Agg

RUN pip3 install seaborn

# Import to build font cache.
RUN python -c "import matplotlib.pyplot"

ENV PYTHONPATH $PYTHONPATH:"$HOME"/pymc3

