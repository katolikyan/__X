import tensornetwork as tn
import numpy as np
import qcsimulator.gate_classes as gates
from qcsimulator.execution_results import Execution_result

class Circuit():

  def __init__(self, number_of_qbits: int) -> None:
    self._qbits = []
    self._edges = []
    self._num_of_qbits = number_of_qbits
    #self.crnt_result = None  # current result of the last execution.
    #self.exec_history = []   # stored results for every execution.
    #self.qasm = []           # append qasm notation after every method call.

    for i in range(number_of_qbits):
      qbit = self._qbit_init()
      self._qbits.append(qbit)
      self._edges.append(qbit[0])

    # --- Take a str parametr to __init__ to create a circuit with certain
    #     bitstring on it.

    # --- Register creation option:
    # --- Create a matrix instead of multiple qubits. and reshape it. option.

    # --- Register creation option:
    # --- Outer product connecction option.
    #self.circuit = tn.outer_product_final_nodes(self._qbits, self._edges)
    #for i, edge in enumerate(self.circuit):
    #  self._edges[i] = edge

    # --- Register creation option:
    # --- Controlled identity connecction at the begining.
    #for i in range(len(self._edges) - 1):
    #  self.ci(i, i + 1)

  def _qbit_init(self):
    return tn.Node(np.array([1.0 + 0j, 0.0 + 0j]))

  def _check_input(self, *indexes, only_positive=False):
    distinct = []
    for index in indexes:
      if not isinstance(index, int):
        raise ValueError("The values have to be indexes of "
                         "the circuit's qubits.")
      if only_positive:
        if index >= self._num_of_qbits or index < 0:
          raise ValueError("Index passed in is out of range. This method "
                           "currently accepts only positive indices.")
      else:
        if index >= self._num_of_qbits or index < -self._num_of_qbits:
          raise ValueError("Index passed in is out of range. Index "\
                           "represents the qbit you are trying to access.")
      if index not in distinct:
        distinct.append(index)
      else:
        raise ValueError("Indexes of qbits have to be distinct numbers. "
                         "It helps to prevent usless extra  calculations.")

  def i(self, qubit_idx: int) -> None:
    self._check_input(qubit_idx)
    i_gate = gates.I_gate()
    self._edges[qubit_idx] ^ i_gate.node[0]
    self._edges[qubit_idx] = i_gate.node[1]

  def x(self, qubit_idx: int) -> None:
    self._check_input(qubit_idx)
    x = gates.X_gate()
    self._edges[qubit_idx] ^ x.node[0]
    self._edges[qubit_idx] = x.node[1]

  def y(self, qubit_idx: int) -> None:
    self._check_input(qubit_idx)
    y = gates.Y_gate()
    self._edges[qubit_idx] ^ y.node[0]
    self._edges[qubit_idx] = y.node[1]

  def z(self, qubit_idx: int) -> None:
    self._check_input(qubit_idx)
    z = gates.Z_gate()
    self._edges[qubit_idx] ^ z.node[0]
    self._edges[qubit_idx] = z.node[1]

  def h(self, qubit_idx: int) -> None:
    self._check_input(qubit_idx)
    h = gates.H_gate()
    self._edges[qubit_idx] ^ h.node[0]
    self._edges[qubit_idx] = h.node[1]

  def t(self, qubit_idx: int) -> None:
    self._check_input(qubit_idx)
    t = gates.T_gate()
    self._edges[qubit_idx] ^ t.node[0]
    self._edges[qubit_idx] = t.node[1]

  def ci(self, control: int, target: int) -> None:
    self._check_input(control, target)
    ci = gates.CI_gate()
    self._edges[control] ^ ci.node[0]
    self._edges[target]  ^ ci.node[1]
    self._edges[control] = ci.node[2]
    self._edges[target]  = ci.node[3]

  def cx(self, control: int, target: int) -> None:
    self._check_input(control, target)
    cx = gates.CX_gate()
    self._edges[control] ^ cx.node[0]
    self._edges[target]  ^ cx.node[1]
    self._edges[control] = cx.node[2]
    self._edges[target]  = cx.node[3]

  def cz(self, control: int, target: int) -> None:
    self._check_input(control, target)
    cz = gates.CZ_gate()
    self._edges[control] ^ cz.node[0]
    self._edges[target]  ^ cz.node[1]
    self._edges[control] = cz.node[2]
    self._edges[target]  = cz.node[3]

  def cy(self, control: int, target: int) -> None:
    self._check_input(control, target)
    cy = gates.CY_gate()
    self._edges[control] ^ cy.node[0]
    self._edges[target]  ^ cy.node[1]
    self._edges[control] = cy.node[2]
    self._edges[target]  = cy.node[3]

  def ch(self, control: int, target: int) -> None:
    self._check_input(control, target)
    ch = gates.CH_gate()
    self._edges[control] ^ ch.node[0]
    self._edges[target]  ^ ch.node[1]
    self._edges[control] = ch.node[2]
    self._edges[target]  = ch.node[3]

  def crot(self, control: int, target: int, angle: float) -> None:
    if not np.isreal(angle):
      raise ValueError("angle parameter have to be a real number")
    self._check_input(control, target)
    crot = gates.CROT_gate(angle)
    self._edges[control] ^ crot.node[0]
    self._edges[target]  ^ crot.node[1]
    self._edges[control] = crot.node[2]
    self._edges[target]  = crot.node[3]

  def qft(self, first: int, last: int) -> None:
    self._check_input(first, last, only_positive=True)
    for crnt in range(first, last + 1):
      self.h(crnt)
      for i in range(crnt, last):
        angle = np.pi / (2 ** (i + 1))
        self.crot(i + 1, crnt, angle)

  def qft_rev(self, first: int, last: int) -> None:
    self._check_input(first, last, only_positive=True)
    for crnt in reversed(range(first, last + 1)):
      for i in reversed(range(crnt, last)):
        angle = -1 * np.pi / (2 ** (i + 1))
        self.crot(i + 1, crnt, angle)
      self.h(crnt)

  def execute(self) -> Execution_result:
    for i in range(len(self._edges) - 1):
      self.ci(i, i + 1)

    nodes = tn.reachable(self._edges[0])
    result_node = tn.contractors.greedy(nodes, self._edges)
    result = Execution_result(result_node)
    for i in range(len(result_node.tensor.shape)):
      self._edges[i] = result_node.get_edge(i)
    return result


def circuit_init(n_qbit: int) -> Circuit:
  if not isinstance(n_qbit, int):
    raise ValueError("The only parametr circuit_init accsepts is a number "
                     "describing number of qbits on the circuit")
  if n_qbit < 1:
    raise ValueError("The number of qbits have to be a positiv number. (1-20)")
  if n_qbit > 20:
    raise ValueError("The maximum of qbits currently supported is 20")
  return Circuit(n_qbit)