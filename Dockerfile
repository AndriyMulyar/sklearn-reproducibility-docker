#base alpine linux docker image with python installed
FROM python:3.7.2-alpine3.8


RUN echo "http://mirror1.hs-esslingen.de/pub/Mirrors/alpine/v3.8/main" >> /etc/apk/repositories; \
    echo "http://mirror1.hs-esslingen.de/pub/Mirrors/alpine/v3.8/community" >> /etc/apk/repositories; \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories; \
    echo "http://mirror1.hs-esslingen.de/pub/Mirrors/alpine/edge/testing" >> /etc/apk/repositories


#Install C headers (BLAS, etc)
RUN apk add --no-cache --virtual sklearn-runtime python git bash zlib hdf5 libgfortran libgcc libstdc++ musl openblas && \
    apk add --no-cache --virtual .build-deps build-base python-dev zlib-dev hdf5-dev freetype-dev libpng-dev openblas-dev && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip install --no-cache-dir "numpy==1.15.3" && \
    pip install cython imblearn pandas && \
    pip install https://github.com/scikit-learn/scikit-learn/archive/0.20.2.tar.gz && \
    pip install https://github.com/AndriyMulyar/PyLearningBenchmarks/archive/1.0.0.tar.gz && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*


#RUN pip install git+https://github.com/AndriyMulyar/PyLearningBenchmarks.git
#install a stable version of scikit-learn

COPY /experiment/ /home/experiment/

ENV PYTHONPATH /home/experiment/PyLearningBenchmarks

WORKDIR /home/experiment/

CMD python example_experiment.py
