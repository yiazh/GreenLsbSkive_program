'''
Created on: 20200915

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''
from Hybrid_wind_hydrogen.class_definition import HWHS, sizing_hwhs_problem, Absolute_path
from equipment_package import wind_turbine, electrolyser, hydrogen_tank, economic
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from pathlib import Path
import pandas as pd

a = HWHS(wind_turbine.wind_turbine(r=45, height=55))

problem = sizing_hwhs_problem(hwhs=a, objective= 0, linearization= True)

max_evaluations = 20000

algorithm = NSGAII(
    problem=problem,
    population_size=100,
    offspring_population_size=100,
    mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
    crossover=SBXCrossover(probability=1.0, distribution_index=20),
    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
)

algorithm.run()
solutions = algorithm.get_result()

from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions

front = get_non_dominated_solutions(solutions)

plot_front = Plot(title='Pareto front approximation', axis_labels=['x', 'y'])
plot_front.plot(front, label='OMOPSO-ZDT1')

# Save results
save = {0:'Maximal profits',
        1:'Maximal green hydrogen',
        2:'Maximal electrolyser efficiency'}

res_dict = {save[problem.objective]: [front[i].objectives[0] for i in range(front.__len__())],
            'IRR': [front[i].objectives[1] for i in range(front.__len__())],
            'Electrolyser capacity': [front[i].variables[0] for i in range(front.__len__())],
            'Tank size': [front[i].variables[1] for i in range(front.__len__())]
            }
res = pd.DataFrame(res_dict)

try:
    res.to_excel(Path(Path().absolute() / 'Data' / (save[problem.objective] + '.xlsx')),float_format='%.3f', index=False)
    print('Successfully saved')
except PermissionError:
    print('File already exists')

'''
@article{BENITEZHIDALGO2019100598,
   title = "jMetalPy: A Python framework for multi-objective optimization with metaheuristics",
   journal = "Swarm and Evolutionary Computation",
   pages = "100598",
   year = "2019",
   issn = "2210-6502",
   doi = "https://doi.org/10.1016/j.swevo.2019.100598",
   url = "http://www.sciencedirect.com/science/article/pii/S2210650219301397",
   author = "Antonio Benítez-Hidalgo and Antonio J. Nebro and José García-Nieto and Izaskun Oregi and Javier Del Ser",
   keywords = "Multi-objective optimization, Metaheuristics, Software framework, Python, Statistical analysis, Visualization",
}
'''

