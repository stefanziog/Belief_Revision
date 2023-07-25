from belief import Belief

from sympy.logic.boolalg import to_cnf, Not
from sympy.logic.inference import satisfiable


class BeliefBase:

    def __init__(self):
        self.beliefBase = {}
        self.valid_operators = ['&', '|', '>>', '<>', '~']

    def __str__(self):  # Done

        if len(self.beliefBase) == 0:
            return ""

        base = [belief for belief in self.beliefBase.keys()]
        stri = "{}".format(base[0])
        for b in base[1:]:
            stri += ", {}".format(b)

        return stri

    def validate_weight(self, x):
        if (0 <= x <= 100):
            return True
        else:
            return False


    def add(self, belief, weight):
        """ Checks if a belief is valid both in formatting and weight """
        if not self.validate_weight(weight):
            print("Invalid weight, weight within 0-100 range")
            return 0

        if not self.validate_formatting(belief) :
            print("Invalid formatting, press 'h' for help")
            return 0
        if not self.validate_belief(belief):
            print("invalid belief")
            return 0

        self._revision(belief, weight)
        #self.reorder() #

    def clear(self):
        """ Clears all beliefs from the BeliefBase """
        self.beliefBase.clear()
        print("The Belief Base is now empty!")
        return ''

    def get(self):
        """ Prints all the beliefs in an array format """
        if len(self.beliefBase) == 0:
            print('There is nothing stored in the Belief Base!')
        else:
            print("Overview of sentences in the Belief Base:\n")
            print("|    Belief Base    |")
            print("| Formula  | Weight |")
            print("-----------|--------")
            for value in self.beliefBase.values():
                formula_width = max(len(value.formula) + 2, 8)  # Minimum width is 9 (for "Formula") + 2 padding spaces
                formula_fmt = "| {:{}}".format(value.formula, formula_width)
                weight_fmt = " | {:>6} |".format(value.weight)
                print(formula_fmt + weight_fmt)
                print("|----------|--------|")


    def reorder(self):
        """ Reorders the belief base according to weight (higher to lower) """
        sorted_beliefs = sorted(self.beliefBase.values(), key=lambda x: x.weight, reverse=True).copy()
        self.beliefBase = {}
        for belief in sorted_beliefs:
            self.beliefBase[belief.formula] = belief



    def validate_formatting(self, belief):
        """ Validate format of user input """
        self.operators = self.valid_operators[0:-1]
        # add whitespace between and split on space to create a list of inputs
        if " " not in belief:
            belief = " ".join(belief)
        belief = belief.split(" ")
        for i in range(len(belief) - 1):
            if (not belief[i].isalpha() and not belief[i + 1].isalpha) and (
                    belief[i] not in self.valid_operators or belief[i] + belief[i + 1] not in self.valid_operators):
                return False
        # check if there is a digit
        if any(char.isdigit() for char in belief):
            return False
        # check if two consecutive characters and if two consecutive operators
        for i in range(0, len(belief) - 1):
            # check if they are not consecutive
            if (belief[i].isalpha() and belief[i + 1].isalpha()):
                return False
            if (belief[i] in self.valid_operators) and (belief[i + 1] in self.operators):
                return False
        # check if operators are in the beginning or end of the string
        if (belief[0] in self.operators) or (belief[-1] in self.valid_operators):
            return False

        return True

    def validate_belief(self, belief):
        """ Validate belief """
        if "<>" in belief:
            belief = self.bicond(belief)

        if (not satisfiable(to_cnf(belief))):
            return False

        return True

    def expand(self, belief, weight):
        """ Adds to the belief base without checking for consistency (is taken care of elsewhere) """
        belief = Belief(belief, weight)
        self.beliefBase[belief.formula] = belief

    def bicond(self, old):
        new = old.replace("<>", ">>").replace("(", "").replace(")", "")
        return "(" + new + ")&(" + new[-1] + ">>" + new[0] + ")"

    def _get_clause_pairs(self, clauses):
        """ Get all possible combinations of clauses """
        pairs = []
        clauses = list(clauses)
        for ind, c in enumerate(clauses):
            for sub_c in clauses[ind + 1:]:
                pairs.append((c, sub_c))
        return pairs

    def entailment(self, alpha):
        """ Check if Beliefbase entails new beliefs.
        Based on PL-Resolution Algorithm from Aritifical Intelligence a modern approach p.255"""

        clauses_cnf = self._collect_beliefs_cnf()
        clauses_cnf.append(to_cnf(Not(alpha)))

        cleaned_clauses = []
        for c in clauses_cnf:
            tempList = str(c).split("&")
            for t in tempList:
                cleaned_clauses.append(t.replace(" ", "").replace("(", "").replace(")", ""))

        clauses = set(cleaned_clauses)

        while True:
            new = set()
            clauses = set(clauses)
            clause_pairs = self._get_clause_pairs(clauses)

            for pairs in clause_pairs:
                resolvents = self._resolve(pairs)
                if '' in resolvents:  # if the list constains an empty clause
                    return True
                new = new.union(set(resolvents))

            if new.issubset(clauses):
                return False

            clauses = clauses.union(new)

    def _revision(self, belief, weight):
        """ Changes existing beliefs in regards to new beliefs, uses """

        if "<>" in belief:
            belief = self.bicond(belief)

        cnf = to_cnf(belief)
        negated_cnf = to_cnf(f'~({cnf})')
        self._contract(negated_cnf)
        self.expand(belief, weight)

    def _remove_beliefs(self, originalBeliefs, beliefsToRemove):
        """ Removes beliefs from the belief base """
        returnBase = originalBeliefs.copy()
        for k1 in beliefsToRemove.keys():
            for k2 in originalBeliefs.keys():
                if k1 == k2:
                    del returnBase[k1]
                    break

        return returnBase

    def _contract(self, negated_cnf):
        """ Removes all beliefs that don't align with new belief """
        beliefBaseCopy = self.beliefBase.copy()  # original beliefbase with all beliefs
        beliefBases = []

        if len(self.beliefBase) > 0:
            for k1 in beliefBaseCopy.keys():  # traverses once
                beliefBaseOuterCopy = self.beliefBase.copy()
                self.beliefBase = beliefBaseOuterCopy
                for k2 in beliefBaseCopy.keys():  # traverses size of belief times
                    if (self.entailment(negated_cnf)):
                        beliefBases.append(self.beliefBase.copy())

                    self._try_delete(self.beliefBase, k2)
                self._try_delete(beliefBaseOuterCopy, k1)

        beliefsToRemove = min(beliefBases, key=len, default={})

        originalBeliefs = beliefBaseCopy
        self.beliefBase = self._remove_beliefs(originalBeliefs, beliefsToRemove)
        self._try_delete(self.beliefBase, str(negated_cnf))

    def _try_delete(self, base, key):
        if key in base.keys():
            del base[key]

    def _resolve(self, pairs):
        """ Resolves each pair and erases contradictions if possible """
        resolvents = []

        ci = str(pairs[0]).replace(" ", "").split("|")
        cj = str(pairs[1]).replace(" ", "").split("|")

        for i in ci:
            for j in cj:
                j_negate = str(Not(j))
                if i == j_negate:
                    temp_ci = ci
                    temp_cj = cj

                    self._remove_contradiction(temp_ci, i)
                    self._remove_contradiction(temp_cj, j)

                    temp_clause = temp_ci + temp_cj
                    temp_clause = "|".join(temp_clause)
                    resolvents.append(temp_clause)

        return resolvents

    def _remove_contradiction(self, tmp_c, target):
        for x in tmp_c:
            if x == target:
                tmp_c.remove(target)

    def _collect_beliefs_cnf(self):
        """ Collect all beliefs """
        beliefs_cnf = []
        for value in self.beliefBase.values():
            beliefs_cnf.append(value.cnf)
        return beliefs_cnf
