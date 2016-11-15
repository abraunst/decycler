# decycler

This code implements the decycling and dismantling procedures devoloped in 

Braunstein, A., Dall’Asta, L., Semerjian, G., Zdeborová, L., 2016. Network dismantling. PNAS 201605083. doi:10.1073/pnas.1605083113, arxiv:1603.08883


    @article{braunstein_network_2016,
	title = {Network dismantling},
	issn = {0027-8424, 1091-6490},
	url = {http://www.pnas.org/content/early/2016/10/18/1605083113},
	doi = {10.1073/pnas.1605083113},
	abstract = {We study the network dismantling problem, which consists of determining a minimal set of vertices in which removal leaves the network broken into connected components of subextensive size. For a large class of random graphs, this problem is tightly connected to the decycling problem (the removal of vertices, leaving the graph acyclic). Exploiting this connection and recent works on epidemic spreading, we present precise predictions for the minimal size of a dismantling set in a large random graph with a prescribed (light-tailed) degree distribution. Building on the statistical mechanics perspective, we propose a three-stage Min-Sum algorithm for efficiently dismantling networks, including heavy-tailed ones for which the dismantling and decycling problems are not equivalent. We also provide additional insights into the dismantling problem, concluding that it is an intrinsically collective problem and that optimal dismantling sets cannot be viewed as a collection of individually well-performing nodes.},
	language = {en},
	urldate = {2016-10-20},
	journal = {PNAS},
	author = {Braunstein, Alfredo and Dall’Asta, Luca and Semerjian, Guilhem and Zdeborová, Lenka},
	month = oct,
	year = {2016},
	keywords = {graph fragmentation, Influence maximization, message passing, Percolation, random graphs},
	pages = {201605083},
    }


Please cite it if you find this code useful!

Compilation:
===========

You'll need the boost libraries. To compile the multi-threading version, 
you need an openmp-compliant C++ compiler (e.g. g++). In that case just uncomment the 
corresponding OMP line in the Makefile. 
Adjust Makefile as needed and issue 

    make


Usage
==========

    $ ./decycler --help
    Usage: ./decycler <option> ... 
    where <option> is one or more of:
    --help                                produce help message
    -d [ --depth ] arg (=20)              set maximum time depth
    -t [ --maxit ] arg (=10000)           set maximum number of iterations
    -D [ --macdec ] arg (=30)             set maximum number of decisional iterations
    -e [ --tolerance ] arg (=9.99999975e-06)  set convergence tolerance
    -g [ --rein ] arg (=0.00100000005)    sets reinforcement parameter rein
    -m [ --mu ] arg (=0.100000001)        sets mu parameter
    -R [ --rho ] arg (=9.99999975e-06)    sets time damping
    -r [ --noise ] arg (=1.00000001e-07)  sets noise
    -s [ --seed ] arg                     sets instance seed
    -z [ --mseed ] arg                    sets messages seed
    -o [ --output ]                       outputs optimal seeds to std output
    -F [ --fields ]                       output fields on convergence
    -T [ --times ]                        output times on convergence
    -P [ --plotting ]                     output times while converging





How to test:
============

RANDOM GRAPH
--------

    # generate an N=78125, <k>=3.5 graph as in the paper
    python gnp.py 78125 3.5 1 > graph.txt

    # find a decycling set (use ./decycler to adjust parameters. 
    # If you have OMP working, ./decycler -jn would run in n threads)
    ./decycler -o < graph.txt > seeds.txt

    # break the decycled graph into components of size <= 100
    cat graph.txt seeds.txt  | python treebreaker.py 100 > broken.txt

    # reintroduce removed nodes as long as component are of size <= 200
    cat graph.txt seeds.txt broken.txt | ./reverse-greedy -t 200 > output.txt

    # the resulting seed set should be at the end of output.txt in the format:
    S i
    ...


TWITTER NETWORK
----------

    # twitter.txt.gz has been produced from the network that can be downloaded from 
    # http://www-levich.engr.ccny.cuny.edu/webpage/hmakse/network-science-destruction-perfected/
    # as follows:
    # wget http://www-levich.engr.ccny.cuny.edu/~min/retweetformat.txt
    # awk '{for (i=2;i<=NF;++i) if ($1>$i) printf "D %i %i\n",$1,$i}' retweetformat.txt | gzip > twitter.txt.gz
    # again, use ./decycler -jn to run with n threads if you have OMP
    zcat < twitter.txt.gz | ./decycler -o > seeds-twitter.txt

    # break the decycled graph into components of size <= 100
    (zcat < twitter.txt.gz; cat seeds-twitter.txt) | python treebreaker.py 100 > broken-twitter.txt

    # reintroduce removed nodes
    (zcat < twitter.txt.gz; cat seeds-twitter.txt broken-twitter.txt ) | ./reverse-greedy -t 100000 > output-twitter.txt
