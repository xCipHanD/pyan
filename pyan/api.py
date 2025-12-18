import os
from glob import glob
import logging
from .analyzer import CallGraphVisitor

def create_callgraph(filenames, root=None, includes=None, logger=None):
    """
    Analyze the given Python source files and return a dictionary of nodes
    representing the call graph.

    Args:
        filenames (list): List of paths to Python source files to analyze.
        root (str, optional): Package root directory. If None, it is inferred.
        includes (list, optional): Additional directories to search for modules.
        logger (logging.Logger, optional): Logger instance.

    Returns:
        dict: A dictionary where keys are qualified node names and values are
              dictionaries containing node information:
              - 'name': Qualified name of the node.
              - 'type': Flavor of the node (e.g., 'module', 'class', 'function').
              - 'filename': Path to the source file where the node is defined.
              - 'line': Line number where the node is defined.
              - 'defines': List of qualified names of nodes defined by this node.
              - 'uses': List of qualified names of nodes used by this node.
    """
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.NullHandler())

    # Expand globs if necessary (though typically the caller should do this)
    expanded_filenames = []
    for fn in filenames:
        if '*' in fn or '?' in fn:
            expanded_filenames.extend(glob(fn, recursive=True))
        else:
            expanded_filenames.append(fn)
    
    expanded_filenames = [os.path.abspath(fn) for fn in expanded_filenames]

    if root:
        root = os.path.abspath(root)
    
    if includes:
        includes = [os.path.abspath(inc) for inc in includes]

    visitor = CallGraphVisitor(expanded_filenames, root=root, includes=includes, logger=logger)
    
    # Convert visitor data to the requested dictionary format
    nodes_dict = {}
    
    # Collect all nodes
    all_nodes = []
    for name, node_list in visitor.nodes.items():
        all_nodes.extend(node_list)
        
    for node in all_nodes:
        qualified_name = node.get_name()
        
        # Get defined nodes
        defined_nodes = []
        if node in visitor.defines_edges:
            for defined in visitor.defines_edges[node]:
                defined_nodes.append(defined.get_name())
        
        # Get used nodes
        used_nodes = []
        if node in visitor.uses_edges:
            for used in visitor.uses_edges[node]:
                used_nodes.append(used.get_name())
        
        # Get source location
        filename = node.filename
        line = None
        end_line = None
        if node.ast_node:
            if hasattr(node.ast_node, 'lineno'):
                line = node.ast_node.lineno
            if hasattr(node.ast_node, 'end_lineno'):
                end_line = node.ast_node.end_lineno
            
        nodes_dict[qualified_name] = {
            'name': qualified_name,
            'type': str(node.flavor).split('.')[-1].lower() if node.flavor else 'unknown',
            'filename': filename,
            'line': line,
            'end_line': end_line,
            'defines': defined_nodes,
            'uses': used_nodes
        }
        
    return nodes_dict
