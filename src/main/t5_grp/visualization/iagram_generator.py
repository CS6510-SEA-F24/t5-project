import graphviz
import yaml

def generate_dot_diagram(pipeline_data):
    """
    Generates a Graphviz Digraph object based on the provided pipeline data.

    Parameters:
    - pipeline_data (dict): A dictionary containing the stages and jobs of the pipeline.

    Returns:
    - graphviz.Digraph: A Digraph object representing the pipeline diagram.
    """
    dot = graphviz.Digraph(comment='Pipeline Diagram')
    # Set the layout direction of the graph from left to right
    dot.attr(rankdir='LR')
    # Retrieve all stages and jobs data
    stages = pipeline_data.get('stages', [])
    jobs = {name: info for name, info in pipeline_data.items() if isinstance(info, dict) and 'stage' in info}

    stage_nodes = {}
    for stage in stages:
        # Create a subgraph for each stage
        with dot.subgraph(name=f'cluster_{stage}') as stage_cluster:

            stage_cluster.attr(label=stage, style='rounded,filled', color='lightgrey',shape='box',pencolor='black', bgcolor='white',margin='0',fontsize='20')
            # Add invisible helper nodes at the top-left and bottom-right corners to control subgraph size
            stage_cluster.node(f'{stage}_invisible_topleft', '',
                               width='0', height='0', style='invisible')
            stage_cluster.node(f'{stage}_invisible_bottomright', '',
                               width='5', height='2', style='invisible')
            # Save the stage node
            stage_nodes[stage] = stage_cluster
            # Add job nodes to the corresponding stage subgraph
            for job_name, job_info in jobs.items():
                if job_info['stage'] == stage:
                    stage_cluster.node(job_name, job_name,shape='box',style='rounded,filled',
                                       width='1.5', height='0.5', fixedsize='true')
    # Add edges based on job dependencies
    for job_name, job_info in jobs.items():
        if 'needs' in job_info:
            for need in job_info['needs']:
                dot.edge(need, job_name,shape='box')

    return dot
