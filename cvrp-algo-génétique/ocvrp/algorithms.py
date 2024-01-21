import math
import random as r
from typing import Dict, Union, List

from ocvrp.util import Building, Individual

class CycleInfo:
    def __init__(self, father: Individual, mother: Individual):
        self._mother = mother
        self._father = father

    @staticmethod
    def _find_cycle(start, correspondence_map):
        cycle = [start]
        current = correspondence_map[start]
        while current not in cycle:
            cycle.append(current)
            current = correspondence_map[current]
        return cycle

    def get_cycle_info(self):
        return self._get_cycle_info()

    def _get_cycle_info(self):
        f_cpy = self._father[:]
        m_cpy = self._mother[:]
        correspondence_map = dict(zip(f_cpy, m_cpy))

        cycles_list = []
        for i in range(len(f_cpy)):
            cycle = self._find_cycle(f_cpy[i], correspondence_map)

            if len(cycles_list) == 0:
                cycles_list.append(cycle)
            else:
                flag = False
                for j in cycles_list:
                    for k in cycle:
                        if k in j:
                            flag = True
                            break
                if not flag:
                    cycles_list.append(cycle)
        return cycles_list


def cycle_xo(ind1: Individual, ind2: Individual, cvrp) -> Dict[str, Union[List[None], List[list], List[bool]]]:
    cl = CycleInfo(ind1, ind2).get_cycle_info()
    p_children = []
    cycle_len = len(cl)

    # Calculates number of iterations to generate combos before quitting.
    if cycle_len == 1:
        runtime = 2
    elif cycle_len == 2:
        runtime = 4
    elif cycle_len == 3:
        runtime = 8
    elif cycle_len == 4:
        runtime = 16
    else:
        runtime = math.ceil(5 * math.log(cycle_len) + 24)

    for i in range(runtime):
        o_child = Individual([None] * len(ind1), None)
        e_child = Individual([None] * len(ind1), None)

        # The binaries represent combination of binaries
        binaries = [bool(r.getrandbits(1)) for _ in cl]
        all_ = len(set(binaries))

        # With binaries of all identical values, we ensure at least one change in the cycle combination
        if all_ == 1:
            ri = r.randint(0, len(binaries) - 1)
            binaries[ri] = not binaries[ri]

        # We forgo this binary if it already exists
        if any(b['binaries'] == binaries for b in p_children):
            continue

        bin_counter = 0
        for c in cl:
            if not binaries[bin_counter]:
                # if 0, get from ind2
                for allele in c:
                    ind1_idx = ind1.index(allele)
                    o_child[ind1_idx] = ind2[ind1_idx]
                    e_child[ind1_idx] = ind1[ind1_idx]
            else:
                # else 1, get from ind1
                for allele in c:
                    ind1_idx = ind1.index(allele)
                    o_child[ind1_idx] = allele
                    e_child[ind1_idx] = ind2[ind1_idx]
            bin_counter += 1

        o_child.fitness = cvrp.calc_fitness(o_child)
        p_children.append({
            "o-child": o_child,
            "e-child": e_child,
            "cycles": cl,
            "binaries": binaries
        })

    # Sort based on O-Child fitness, then grab the corresponding e-child for that o-child as well
    children = min(p_children, key=lambda pc: pc['o-child'].fitness)
    children["e-child"].fitness = cvrp.calc_fitness(children['e-child'])

    return children


def order_xo(ind1: Individual, ind2: Individual) -> Individual:
    bound = len(ind1)

    cxp1 = r.randint(0, (bound - 1) // 2)
    cxp2 = r.randint(((bound - 1) // 2) + 1, bound - 1)
    child = [None] * bound
    for i in range(cxp1, cxp2 + 1):
        child[i] = ind1[i]

    parent_idx = cxp2 + 1
    child_idx = cxp2 + 1
    parent_bound = child_bound = bound

    while child_idx != cxp1:
        if parent_idx == parent_bound:
            parent_idx = 0
            parent_bound = cxp2 + 1

        if child_idx == child_bound:
            child_idx = 0
            child_bound = cxp1

        if ind2[parent_idx] not in child:
            child[child_idx] = ind2[parent_idx]
            child_idx += 1
        parent_idx += 1

    return Individual(child, None)


def inversion_mut(child: Individual) -> Individual:
    mid = (len(child) // 2) - 1
    idx1 = r.randint(0, mid)
    idx2 = r.randint(mid + 1, len(child) - 1)

    # Swap the values until all values are mirrored
    while idx1 <= idx2:
        _swap(child, idx1, idx2)
        idx1 += 1
        idx2 -= 1

    return child


def swap_mut(child: Individual) -> Individual:
    idx1 = r.randint(0, len(child) - 1)
    idx2 = r.randint(0, len(child) - 1)
    _swap(child, idx1, idx2)

    return child

def _swap(ll: Individual, idx1: int, idx2: int) -> None:
    ll[idx1], ll[idx2] = ll[idx2], ll[idx1]
