import math

def crf(rate=0.05,life = 25):
    '''
    capital recovery factor
    :param rate: annual rate
    :param initial_cost:
    :param life: years
    :return: annuity
    '''
    crf = (rate*(1+rate)**life)/((1+rate)**life-1)
    return crf # Money/year

def coe(capacity, capex, omcost, power_production, rate = 0.05, life =25):
    '''
    cost of energy
    :param capex: capital expenditure, considering the depreciation, euros/year/MW
    :param omcost: o&m cost, euros/year/Mw, 2% capex
    :param power_production:
    :param rate:
    :param life:
    :return: cost of energy, if energy production is the total of a year, then the function returns average cost. if
    the argument time is 1/8640 and the corresponding energy production is within an hour, it returns to a hourly price.
    '''
    coe = (capex * crf(rate,life) * capacity + omcost *capacity) / (power_production*8640)
    return coe


if __name__ == '__main__':
    b=crf()
    a = coe(26.8,3e6,3e6*0.02,20)
    print(a,b)