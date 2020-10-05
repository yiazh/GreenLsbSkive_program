'''
Created on: 20200915

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''
from Hybrid_wind_hydrogen.class_definition import HWHS, sizing_hwhs_problme, Absolute_path
from equipment_package import wind_turbine, electrolyser, hydrogen_tank, economic
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations

a = HWHS(wind_turbine.wind_turbine(r=45, height=55))

problem = sizing_hwhs_problme(hwhs=a)

max_evaluations = 25000

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

res = pd.DataFrame({'x': [front[i].objectives[0] for i in range(front.__len__())],
                    'y': [front[i].objectives[1] for i in range(front.__len__())]
                    })
res.to_excel('C:\PhD\GreenLsbSkive_program\Hybrid_wind_hydrogen\Data\output.xlsx')
