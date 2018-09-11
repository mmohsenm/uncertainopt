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

Here, <img  src="https://github.com/mmohsenm/uncertainopt/blob/master/images/obj_coef.png" width="11%">
are objective coefficient parameters (lets call them set `C`), 
<img  src="https://github.com/mmohsenm/uncertainopt/blob/master/images/cons_coef.png" width="15%">
are constraints coefficient parameters (lets call them set `A`), 
and <img  src="https://github.com/mmohsenm/uncertainopt/blob/master/images/rhs.png" width="11%">
are right hand side parameters (lets call them `b`). Either of these parameters 
or all of them can be uncertain or random, and you may have their probability distribution, or not. 
Depending on which set is random, one might adopt different approach to model and solve the underlying problem.
In general, there are two approaches to optimization under uncertainty:
* Here & Now
    - Estimate (guess) random parameters and solve the problem
    - Use Chance Constraints
* Wait & See
In this approach generally you can take corrective actions 
when you observe the true value of an uncertain parameter. So, you can use either:
    - Recourse Models
    - Dynamic Programming
    
In the following sections, we explain each of these methods in details using the following simple example.
### Here & Now
In this approach, we estimate or guess the highly possible outcome of random parameters, 
or optimize under certain confidence level.
#### Estimate Parameters
Use mean value or quartile values. Examples: delivery time, portfolio optimization, etc
#### Chance Constrained Optimization
### Wait & See
#### Recourse Models
##### Two-stage Models
##### Multi-stage Models
* *Nonanticipativity*
#### Dynamic Programming

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



