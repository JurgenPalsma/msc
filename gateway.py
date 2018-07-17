from py4j.java_gateway import JavaGateway, GatewayParameters, get_field
from individual import Individual
from fitness import Fitness
import logging

class pjGateWay:
    """
    Class useful if we want multiple gateways to test different fitness funcs
    """
    def __init__(self, port):
        self.port = port
        self.way = JavaGateway(gateway_parameters=GatewayParameters(port=self.port))


class fGateway(pjGateWay):
    """
    Bridge between python and java through py4j to get the Java Fitness function
    TODO: convert fitness to struct
    """
    def __init__(self, port):
        """
        Make sure the port is the same as the JVM machine
        """
        logger = logging.getLogger(__name__)
        logger.debug("Creating a fitness gateway on port %f" % port)
        pjGateWay.__init__(self, port)
        self.ga = self.way.entry_point
    
    def fitness(self, individual: Individual): # TODO: convert to fitness struct
        """
        Executes the DC-GA fitness function and returns a python-converted fitness struct
        """        
        j_indiv = self.__convert_individual_p_to_j(individual)
        fit = self.__convert_fitness_j_to_p(self.way.fitnessGateway(j_indiv))
        #if (fit.mdd == 0 ):
        #    print("Fit at 0 with individual:")
        #    print(individual.__repr__())
        return fit
        
    def testFitness(self, individual: Individual):
        """
        Executes the DC-GA fitness function on test data
        """        
        j_indiv = self.__convert_individual_p_to_j(individual)
        fit = self.__convert_fitness_j_to_p(self.way.testFitnessGateway(j_indiv))
        return fit

    def __convert_individual_p_to_j(self, individual: Individual):
        p_len = 5 + len(individual.threshold_weights)
        t_indiv = self.way.new_array(self.way.jvm.double, p_len)

        t_indiv[0] = individual.quantity
        t_indiv[1] = individual.b_start
        t_indiv[2] = individual.b_end
        t_indiv[3] = individual.q_short
        t_indiv[4] = individual.b_price
        
        for i in range(0, individual.threshold_number):
            t_indiv[i + 5] = individual.threshold_weights[i]
        return t_indiv

    def __convert_fitness_j_to_p(self, f):
        # TODO
        return Fitness(
            value = get_field(f, "value"),
            u_sell = get_field(f, "uSell"),
            u_buy = get_field(f, "uBuy"),
            noop = get_field(f, "noop"),
            realised_profit = get_field(f, "realisedProfit"),
            mdd = get_field(f, "MDD"),
            ret = get_field(f, "Return"),
            wealth = get_field(f, "wealth"),
            no_of_transactions = get_field(f, "noOfTransactions"),
            no_of_short_selling_transactions = get_field(f, "noOfShortSellingTransactions")
        )
		
#gateway = fGateway(27135)
#individual = [134.0, 0.3434593504962303, 0.8807313175318929, 0.0, 0.9790021314573502, 0.296501, 0.398711, 0.639533, 0.833413, 0.700392]
#print(gateway.fitness(individual))