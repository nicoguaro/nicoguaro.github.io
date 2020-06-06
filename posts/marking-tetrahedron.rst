.. title: Randomized Marking of a Tetrahedron
.. slug: marking-tetrahedron
.. date: 2020-06-05 22:58:32 UTC-05:00
.. tags: mathjax, monte carlo, combinatorics, computational geometry
.. category: Scientific Computing
.. link: 
.. description: 
.. type: text

Yesterday (June 4, 2020), Christian Howard posted on 
`Twitter <https://twitter.com/choward1491/status/1268736220055699457>`_
the following question

 You are given a tetrahedron τ. For each triangular facet of τ,
 we uniformly at random mark one of their edges. What is the
 probability that there exists an edge of τ that is marked twice?

I thought about a little bit but I couldn't find how to count
properly. Then, a number popped up in my mind out of the blue:
:math:`2/3`, but I don't know why. So, I decided to run a
simulation to check this number.

The right answer is :math:`51/81` that is approximately 63%. This
calculation is well explained in 
`Christian's blog <https://medium.com/@choward1491/randomized-marking-of-a-tetrahedron-f978593f43d2>`_
and with some cool drawings (and memes).

The algorithm
=============

The algorithm is quite simple. I number the edges in each face following
a counter-clockwise orientation:

- **face 0**: edge 0, edge 1, edge 2

- **face 1**: edge 0, edge 3, edge 4

- **face 2**: edge 1, edge 5, edge 3

- **face 3**: edge 2, edge 4, edge 5

Then, I take each face and pick a random number from :math:`(0, 1, 2)` and
mark the corresponding edge, and move to the following face. I repeat
this process several times and I count the favorable cases and divide
them by the number of trials to get an estimate of the probability.

Following is a Python code that follows this idea.


.. code:: python

    import numpy as np
    import matplotlib.pyplot as plt

    faces = np.array([
            [0, 1, 2],
            [0, 3, 4],
            [1, 5, 3],
            [2, 4, 5]])


    def mark_edges():
        marked_edges = np.zeros((6), dtype=int)
        for face in faces:
            num = np.random.randint(0, 3)
            edge = face[num]
            marked_edges[edge] += 1
        return marked_edges


    def comp_probs(N_min=1, N_max=5, ntrials=100):
        prob = []
        N_vals = np.logspace(N_min, N_max, ntrials, dtype=int)
        for N in N_vals:
            cont_marked = 0
            for cont in range(N):
                marked = mark_edges()
                if 2 in marked:
                    cont_marked += 1
            prob.append(cont_marked/N)
        return N_vals, prob

            
    #%% Computation
    N_min = 1
    N_max = 5
    ntrials = 100
    np.random.seed(seed=2)
    N_vals, prob = comp_probs(N_min, N_max, ntrials)

    #%% Plotting
    plt.figure(figsize=(4, 3))
    plt.hlines(0.63, 10**N_min, 10**N_max, color="#3f3f3f")
    plt.semilogx(N_vals, np.array(prob), "o", alpha=0.5)
    plt.xlabel("Number of trials")
    plt.ylabel("Estimated probability")
    plt.savefig("prob_tet.svg", dpi=300, bbox_inches="tight")
    plt.show()
 
And we can see the following evolution for different number of trials.

.. image:: /images/marked_tets.svg
   :width: 600 px
   :alt: Estimated probabilities for different sample sizes.
   :align:  center
