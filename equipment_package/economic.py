import math

def crf(rate=0.05, life=25):
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


def coe(capacity, capex, omcost, capacity_factor=0.4, rate=0.05, life=25):
    '''
    cost of energy
    :param capex: capital expenditure, considering the depreciation, euros/MW
    :param omcost: o&m cost, euros/MW, 2% capex, a typical value
    :param capacity_factor: The average power generated, divided by the rated peak power.
    :param rate: annual interest rate
    :param life: project life, year
    :return: cost of energy, euros/Mwh
    '''
    coe = (capex * crf(rate, life) * capacity + omcost * capacity) / (capacity * 8640 * capacity_factor)
    return coe


if __name__ == '__main__':
    a = crf()
    b = coe(26.8, 3e6, 3e6 * 0.02, 0.4)
    print(a, b)
    print('Only consider O&M cost: {}'.format(coe(26.8, 0, 3e6 * 0.02)))
