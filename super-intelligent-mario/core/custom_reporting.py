import pathlib
from __init__ import PROJ_DIR
import pickle

from neat.reporting import *


"""
THIS IS CUSTOMIZATION OF NEAT'S REPORTING CLASS TO SAVE BEST GEN GENOME AS PICKLE
"""


class CustomStdOutReporter(StdOutReporter):
    def __init__(self, show_species_detail):
        super().__init__(show_species_detail)

    def post_evaluate(self, config, population, species, best_genome):

        # region CUSTOMIZATIONS
        all_genomes = [g for g in itervalues(population)]

        def key(genome):
            return genome.fitness

        all_genomes.sort(key=key)
        worst_genome = all_genomes[0]

        worst_genome_file = pathlib.Path(PROJ_DIR).joinpath("results","notable_genomes", "worst-" + str(self.generation) + ".pkl")
        with open(worst_genome_file, "wb") as output:
            pickle.dump(worst_genome, output, 1)

        best_genome_file = pathlib.Path(PROJ_DIR).joinpath("results","notable_genomes", "best-" + str(self.generation) + ".pkl")
        with open(best_genome_file, "wb") as output:
            pickle.dump(best_genome, output, 1)
        # endregion CUSTOMIZATIONS

        # pylint: disable=no-self-use
        fitnesses = [c.fitness for c in itervalues(population)]
        fit_mean = mean(fitnesses)
        fit_std = stdev(fitnesses)
        best_species_id = species.get_species_id(best_genome.key)
        print("Population's average fitness: {0:3.5f} stdev: {1:3.5f}".format(fit_mean, fit_std))
        print(
            "Best fitness: {0:3.5f} - size: {1!r} - species {2} - id {3}".format(
                best_genome.fitness, best_genome.size(), best_species_id, best_genome.key
            )
        )