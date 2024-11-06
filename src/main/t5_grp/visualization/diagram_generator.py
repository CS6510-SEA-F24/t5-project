from graphviz import Digraph


def generate_dot_diagram(pipeline_data):
    """
    Generates a complete pipeline diagram with proper positioning.

    Parameters:
        pipeline_data (dict): The parsed YAML content containing pipeline information.

    Returns:
        Digraph: A graphviz Digraph object representing the pipeline diagram.
    """
    # Get the pipeline name from the data, or use 'Pipeline' as default if not available
    pipeline_name = pipeline_data.get('pipeline', {}).get('name', 'Pipeline')
    dot = Digraph(comment=pipeline_name)

    # Basic graph settings
    dot.attr(
        compound='true',# Allows edges to cross cluster boundaries
        rankdir='LR',  # Left-to-right layout
        nodesep='0.5',  # Node separation
        ranksep='1.0',  # Rank separation
        splines='ortho'  # Use orthogonal edge routing to reduce overlaps
    )

    stages = pipeline_data.get('stages', [])
    jobs = pipeline_data.get('jobs', [])
    stage_dict = {stage: [] for stage in stages}
    for job in jobs:
        stage_dict[job['stage']].append(job)
    job_dependencies = {job['name']: job.get('needs', []) for job in jobs}


    # A list to accumulate all artifacts from stages
    cumulative_artifacts = []
    prev_artifacts_node = None

    # Iterate through each stage and create subgraphs (clusters) for them
    for stage in stages:
        with dot.subgraph(name=f'cluster_{stage}') as stage_cluster:
            stage_cluster.attr(
                label=stage, # Label for the cluster
                color='black',
                style='filled,rounded',
                fillcolor='white',
                fontcolor='black',
                fontsize='16',
                margin='20',
                fixedsize='true',  # Fix size of the subgraph
                width='4',  # Set fixed width
                height='4',  # Set fixed height

            )
            # Filter jobs that belong to this stage
            stage_jobs = [job for job in jobs if job.get('stage') == stage]
            stage_artifacts = []

            for job in stage_jobs:
                job_name = job.get('name')
                # Add a node for each job in the stage
                stage_cluster.node(
                    job_name,
                    label=job_name, # Label for the job node
                    shape='box',
                    style='filled,rounded',
                    fontcolor='black',
                    width='1',  # Width of each job node
                    height='0.5',  # Height of each job node
                    fillcolor='white' if not job.get('allow_failure', False) else 'lightgrey'
                    # Color based on `allow_failure`
                )
                # Collect artifacts if present in the job
                if 'artifacts' in job:
                    stage_artifacts.extend(job['artifacts'].get('paths', []))

            # Add artifacts as a node if they exist
            if stage_artifacts:
                artifact_label = '\n'.join(stage_artifacts)
                node_name = f'{stage}_artifacts'
                stage_cluster.node(
                    node_name,
                    label=artifact_label, # Label for the artifacts node
                    shape='box',
                    style='filled,rounded',
                    fillcolor='white',
                    fontcolor='black',
                    color='blue',   # Border color for the artifacts node
                    margin='0.2',
                    width='1.5',
                    height='0.75',
                )
                cumulative_artifacts.extend(stage_artifacts)
                # Create an invisible edge to maintain layout order
                if prev_artifacts_node:
                    stage_cluster.edge(prev_artifacts_node, node_name, style='invis')
                prev_artifacts_node = node_name

    # Add a final artifacts node at the bottom of the pipeline
    if cumulative_artifacts:
        final_label = '\n'.join(cumulative_artifacts)
        dot.node(
            'final_artifacts',
            label=final_label,
            shape='box',
            style='filled,rounded',
            fillcolor='white',
            fontcolor='black',
            color='blue',
            margin='0.2'
        )
        if prev_artifacts_node:
            dot.edge(prev_artifacts_node, 'final_artifacts', style='invis')

    # Add edges to represent dependencies between jobs
    for job_name, dependencies in job_dependencies.items():
        for dependency in dependencies:
            dot.edge(dependency, job_name)

    return dot

