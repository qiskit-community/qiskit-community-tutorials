# -*- coding: utf-8 -*-

# Copyright 2019 IBM.
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

from qiskit import execute, Aer, QuantumCircuit
from qiskit.test.base import dicts_almost_equal
from qiskit.transpiler.basepasses import AnalysisPass, TransformationPass
from qiskit.test.mock import FakeMelbourne # NB will need to install dev requirements
from qiskit.transpiler.passes import TrivialLayout
from qiskit.transpiler import PassManager
from qiskit.providers.aer.noise.device import basic_device_noise_model


"""
Your solution needs to comprise of one or more passes that you have written along with
a PassManager that uses them. The PassManager is allowed to use passes that are already
included in Qiskit. 
"""


class MyBasicAnalysisPass(AnalysisPass):
    """Analysis passes look at the DAG to identify some property and then write this
    to the property set so that it can be accessed by other passes"""

    def run(self, dag):
        self.property_set['my depth'] = dag.depth()


class MyBasicTransformationPass(TransformationPass):
    """Transformation passes alter the DAG and then return a DAG. They can use properties that
    have been written to the property set.
    """
    def __init__(self, properties):
        self.properties = properties

    def run(self, dag):
        dag_depth = self.property_set['my depth']
        gates = self.properties.gates
        return dag


""" To test your passes you can use the fake backend classes. Your solutions will be tested against
Yorktown, Ourense and Melbourne, as well as some internal backends. """
backend = FakeMelbourne()
properties = backend.properties()
coupling_map = backend.configuration().coupling_map


""" You must submit a pass manager which uses at least one pass you have written. 
Examples of creating more complex pass managers can be seen in qiskit.transpiler.preset_passmanagers"""
pass_manager = PassManager()
pass_manager.append(TrivialLayout(coupling_map))
pass_manager.append(MyBasicAnalysisPass())
pass_manager.append(MyBasicTransformationPass(properties))

""" This allows us to simulate the noise a real device has, so that you don't have to wait for jobs to complete
on the actual backends."""
noise_model = basic_device_noise_model(properties)
simulator = Aer.get_backend('qasm_simulator')


""" This is the circuit we are going to look at"""
qc = QuantumCircuit(2, 2)
qc.h(1)
qc.measure(0, 0)
circuits = [qc]


result_normal = execute(circuits,
                        simulator,
                        coupling_map=coupling_map).result().get_counts()

# NB we include the noise model in the second run
result_noisy = execute(circuits,
                       simulator,
                       noise_model=noise_model,
                       coupling_map=coupling_map).result().get_counts()

""" Check to see how similar the counts from the two runs are, where delta the allowed difference between
the counts. Returns an empty string if they are almost equal, otherwise returns an error message which can 
then be printed."""
equality_check = dicts_almost_equal(result_normal, result_noisy, delta=1e-8)

if equality_check:
    print(equality_check)
