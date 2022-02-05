# This is project to determine critical point of glass transition of colloid system

This project intends to simulate the glass transition process with the idea of 'cage affect' where particles in colloid systems are only allowed to move in certain space which acts like a cage. Mathematically speaking or in terms of simulation target, compared to standard random walk, where MSD (Mean Square Distance) increases infinitely as long as the colloid system has infinite space, the particles in colloid systems that are facing glass transition are retained in certain area and the MSD will reaches its peak and maintains at this level. This is how we determine the critical point of glass transition.

And for the colloid system, there are all kinds of particles avaiable at theoretical level for simulation. I chose the most simple one, hard-sphere model, where particles are hard spheres with no interactions with other particles, and the only restriction is that particles can not be overlapped. It's a simple model but also easy to investigate.

One of the most difficult prolems when I actually started the simulation is that if we randomly put particles into the system to create the initial state of the sytem, it's ofen that we can not put too many particles in it. It's difficult to increase the particle volume rate since high particle volumne rate always demonstrate specific structures. There are certain methods to increase the particle volumne rate, but at that time, I do not have enough time/knowledge to finish that.

Furthermore, if more complicated particle models are applied, we can investigate colloid systems that are closer to real ones.
