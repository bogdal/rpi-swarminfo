Swarm Info
==========

``SwarmInfo`` displays some information regarding the Docker Swarm status on the LCD (I²C bus).

It works on the ``Raspberry Pi`` devices.

Build an image:

.. code-block:: bash

    docker build -t swarminfo .

Run a new container:

.. code-block:: bash

    docker run -it -d --name swarminfo --privileged -v /var/run/docker.sock:/var/run/docker.sock swarminfo

.. image:: https://github-bogdal.s3.amazonaws.com/rpi-swarminfo/lcd.jpg
