# A Practical Guide to Optimization under Uncertainty


Optimization under Uncertainty has lots of used cases in many real world 
and practical problems in the area of supply chain, transportation, 
retail and finance. However, current available resources provide limited 
help to industry practitioners. 
If you look at some online resources on Two-stage Stochastic Programming, 
Dynamic Programming and Robust Optimization, you see they get too technical 
too soon which puts a burden on their applicability. 
In this guide, I'm trying to provide a simple tutorial on how to 
solve optimization problems (mainly linear and mixed integer linear programming) 
when we face some uncertainty. We give a simple practical example and show 
how one can formulate that problem in the presence of uncertainty, provide 
useful algorithms and present sample codes in Python for reference.

## Prerequisites
We assume a reader of this tutorial is familiar with basics Linear and Mixed Integer Programming, 
and knows what _Decision Variables_, _Constraints_, _Objective Function_, and _Non-negativity restriction_ are.


## Modeling Uncertainty
Before explaining possible approaches one may take to solve an optimization problem under uncertainty,
let me refresh your memory on deterministic LP/MIP problems. 
A typical LP/MIP problem has a mathematical form like this:

<p align="center">
<img  src="https://github.com/mmohsenm/uncertainopt/blob/master/images/lp_model.png" width="40%">
</p>

Here, <img  src="https://github.com/mmohsenm/uncertainopt/blob/master/images/obj_coef.png" width="12%" height="10%">
are objective coefficient parameters
   
### Mean value, Worst case and Best case optimization
### Chance Constrained Optimization
### Recourse Models``
#### Two-stage Models
#### Multi-stage Models
* *Nonanticipativity*
### Dynamic Programming

## Optimization Algorithms
Here we provide some helpful algorithms that come handy when dealing 
with optimization under uncertainty.
### Bender’s Decomposition
### Lagrangian Relaxation

## Authors

* **Mohsen Moarefdoost, Ph.D.** 


## License


## Acknowledgments

*



