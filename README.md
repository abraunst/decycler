# decycler

This code implements the decycling and dismantling procedures devoloped in 

Braunstein, Alfredo, Luca Dall'Asta, Guilhem Semerjian, and Lenka Zdeborová. "Network Dismantling." Proceedings of the National Academy of Sciences, October 18, 2016, 201605083. doi:10.1073/pnas.1605083113, arxiv:1603.08883.

Please cite it if you find this code useful!

Compilation:
===========

You'll need the boost libraries. To compile the multi-threading version, 
you need an openmp-compliant C++ compiler (e.g. g++). In that case just uncomment the 
corresponding OMP line in the Makefile. 
Adjust Makefile as needed and issue 'make'




How to test:
============

RANDOM GRAPH
--------

    # generate an N=78125, <k>=1.5 graph as in the paper

    python gnp.py 78125 3.5 1 > graph.txt

    # find a decycling set (use ./decycler to adjust parameters. If you have OMP working -jn would run in n threads)

    ./decycler -o < graph.txt > seeds.txt

    # break the decycled graph into components of size <= 100

    cat graph.txt seeds.txt  | python treebreaker.py 100 > broken.txt

    # reintroduce removed nodes as long as component are of size <= 200

    cat graph.txt seeds.txt broken.txt | ./reverse-greedy -t 200 > output.txt

    # the resulting seed set should be in output.txt in the format:

    S i


TWITTER NETWORK
----------

    # again, use -jn to run with n threads if you have OMP

    zcat twitter.txt.gz | ./decycler -o > seeds-twitter.txt

    (zcat twitter.txt.gz; cat seeds-twitter.txt) | python treebreaker.py 100 > broken-twitter.txt

    (zcat twitter.txt.gz; cat seeds-twitter.txt broken-twitter.txt ) | ./reverse-greedy -t 100000 > output-twitter.txt
