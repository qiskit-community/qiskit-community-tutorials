# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

from qiskit.aqua.algorithms import ExactEigensolver
from qiskit.chemistry.drivers import PySCFDriver, UnitsType
from qiskit.chemistry.core import Hamiltonian


# An example of using a loop to vary inter-atomic distance.
# Inside the loop the 'atom' value is updated
# with a new molecular configuration. The molecule is H2 and its inter-atomic distance
# i.e the distance between the two atoms, is altered from 0.5 to 1.0. Each atom is
# specified by x, y, z coords and the atoms are set on the z-axis, equidistant from
# the origin, and updated by d inside the loop where the molecule string has this value
# substituted by format(). Note the negative sign preceding the first format
# substitution point i.e. the {} brackets
#

molecule = 'H .0 .0 -{0}; H .0 .0 {0}'
for i in range(21):
    d = (0.5 + i * 0.5 / 20) / 2
    driver = PySCFDriver(molecule.format(d), unit=UnitsType.ANGSTROM,
                         charge=0, spin=0, basis='sto3g')
    qmolecule = driver.run()
    operator = Hamiltonian()
    qubit_op, aux_ops = operator.run(qmolecule)
    result = ExactEigensolver(qubit_op).run()
    _, result = operator.process_algorithm_result(result)
    print('{:.4f} : {}'.format(d * 2, result['energy']))
