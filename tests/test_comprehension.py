
import os
from pyan.analyzer import CallGraphVisitor
from pyan.visgraph import VisualGraph
from pyan.writers import DotWriter

def test_list_comprehension():
    code = """
def foo():
    pass

def bar():
    x = [foo() for i in range(10)]
"""
    filename = "test_list_comprehension.py"
    with open(filename, "w") as f:
        f.write(code)

    try:
        visitor = CallGraphVisitor([filename])
        
        # Check if the edge from bar to foo exists
        found = False
        for from_node, to_nodes in visitor.uses_edges.items():
            if from_node.name == "bar":
                for to_node in to_nodes:
                    if to_node.name == "foo":
                        found = True
                        break
        
        assert found, "Edge from bar to foo not found in list comprehension"

    finally:
        if os.path.exists(filename):
            os.remove(filename)

def test_generator_expression():
    code = """
def foo():
    pass

def bar():
    x = (foo() for i in range(10))
"""
    filename = "test_generator_expression.py"
    with open(filename, "w") as f:
        f.write(code)

    try:
        visitor = CallGraphVisitor([filename])
        
        # Check if the edge from bar to foo exists
        found = False
        for from_node, to_nodes in visitor.uses_edges.items():
            if from_node.name == "bar":
                for to_node in to_nodes:
                    if to_node.name == "foo":
                        found = True
                        break
        
        assert found, "Edge from bar to foo not found in generator expression"

    finally:
        if os.path.exists(filename):
            os.remove(filename)
