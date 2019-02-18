# docker-sklearn-reproducible
a docker container template to reproduce experiments run utilizing sci-kit learn


After running:

`docker build -t aymulyar:sklearn-experiment`

Run:

`docker run -it --rm aymulyar:sklearn-experiment /bin/ash`

To spawn and enter into an `ash` (like bash but for alpine linux) terminal in the container.
