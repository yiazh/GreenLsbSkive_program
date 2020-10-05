import math


def capital_recovery_factor(rate=0.05, life=25):
    '''
    capital recovery factor, the ratio used to determine the present value of a series of equal annual cash payments.
    The payments could be made weekly, monthly, quarterly, yearly, or at any other regular interval of time, and are
    commonly known as annuities.

    Given present value P, we have:
    P =  A(\frac{1}{1+i}+\frac{1}{(1+i)^2}+...+\frac{1}{(1+i)^{life}})
    with A denoting the annuity.
    Futher
    A = crf *P

    :param rate: annual rate
    :param life: years
    :return: annuity
    '''
    crf = (rate * (1 + rate) ** life) / ((1 + rate) ** life - 1)
    return crf  # Money/year


def cost_of_energy(capacity, capex, omcost, capacity_factor=0.4, rate=0.05, life=25):
    '''
    cost of energy
    :param capex: capital expenditure, considering the depreciation, euros/MW
    :param omcost: o&m cost, euros/MW, 2% capex, a typical value
    :param capacity_factor: The average power generated, divided by the rated peak power.
    :param rate: annual interest rate
    :param life: project life, year
    :return: cost of energy, euros/Mwh
    '''
    coe = (capex * capital_recovery_factor(rate, life) * capacity + omcost * capacity) / (
                capacity * 8640 * capacity_factor)
    return coe


def net_present_value(initial_investment=100, interest_rate=0.07, annual_cost=10, annual_profit=20, length_project=20):
    '''
    Net present value is used to evaluate the profitability of a project by transforming all cash flows -both the costs
    and profits - in the future to their present value.
    If Npv is bigger than zero, the investor will benefit from this project, vice versa.
    :param initial_investment:
    :param interest_rate:
    :param annual_cost:
    :param annual_profit:
    :param length_project:
    :return:
    '''
    npv = -initial_investment
    for i in range(length_project):
        npv = npv - annual_cost / math.pow(1 + interest_rate, i + 1) + annual_profit / math.pow(1 + interest_rate,
                                                                                                i + 1)
    return npv


def internal_rate_of_return(initial_investment=100, annual_cost=10, annual_profit=20, length_project=20):
    def npv(interest_rate):
        return net_present_value(initial_investment=initial_investment, interest_rate=interest_rate,
                                 annual_cost=annual_cost,
                                 annual_profit=annual_profit, length_project=length_project)

    if annual_profit < annual_cost:
        return -1
    else:
        a = -1
        b = 1
        c = (a + b) / 2
        while math.fabs(npv(c)) >= 1e-6:
            if npv(c) < 0:
                (b,c) = (c, (c+a)/2)
                # b = c
                # c = (c + a) / 2
            else:
                (a,c) = (c,(c+b)/2)
                # a = c
                # c = (c + b) / 2
        return c


if __name__ == '__main__':
    a = capital_recovery_factor()
    b = cost_of_energy(26.8, 3e6, 3e6 * 0.02, 0.4)
    print(a, b)
    print('Only consider O&M cost: {}'.format(cost_of_energy(26.8, 0, 3e6 * 0.02)))
    c = internal_rate_of_return(initial_investment=100, annual_cost=10, annual_profit=20,
                                length_project=20)
    print(c)
    print(net_present_value(initial_investment=100, interest_rate=c, annual_cost=10, annual_profit=20,
                            length_project=20))
