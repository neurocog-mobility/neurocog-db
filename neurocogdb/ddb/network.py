import duckdb
from neurocogdb.config.paths import fetch_ddb_path
import pandas as pd
import duckdb


def load_network_elements():
    con = duckdb.connect(fetch_ddb_path())

    # Fetch entities
    programs = con.execute("SELECT id, name FROM programs").fetchall()
    projects = con.execute(
        "SELECT id, name, program_id, start_date, end_date FROM projects"
    ).fetchall()
    members = con.execute("SELECT id, name, role FROM members").fetchall()
    collaborators = con.execute(
        "SELECT id, name, affiliation FROM collaborators"
    ).fetchall()
    funding = con.execute("SELECT id, organization FROM funding").fetchall()

    # Fetch relationships
    program_members = con.execute(
        "SELECT program_id, member_id FROM program_members"
    ).fetchall()
    program_collabs = con.execute(
        "SELECT program_id, collaborator_id FROM program_collaborators"
    ).fetchall()
    program_funding = con.execute(
        "SELECT program_id, funding_id FROM program_funding"
    ).fetchall()
    project_members = con.execute(
        "SELECT project_id, member_id FROM project_members"
    ).fetchall()

    nodes, edges = [], []

    # Programs
    for pid, name in programs:
        label = name.replace(" ", "\n").replace("_", "\n")
        nodes.append(
            {"data": {"id": f"program_{pid}", "label": label, "type": "program"}}
        )

    # Projects
    for proj_id, name, prog_id, start_date, end_date in projects:
        # determine status
        if pd.to_datetime(start_date) > pd.to_datetime("today"):
            status = "upcoming"
        elif pd.to_datetime(end_date) < pd.to_datetime("today"):
            status = "completed"
        else:
            status = "ongoing"

        label = name.replace(" ", "\n").replace("_", "\n").replace("-", "\n")
        nodes.append(
            {
                "data": {
                    "id": f"project_{proj_id}",
                    "label": label,
                    "type": "project",
                    "status": status,
                }
            }
        )
        if prog_id:  # link project to its program
            edges.append(
                {
                    "data": {
                        "source": f"program_{prog_id}",
                        "target": f"project_{proj_id}",
                        "label": "includes",
                    }
                }
            )

    # Members
    for mid, name, role in members:
        label = name.replace(" ", "\n").replace("_", "\n")
        nodes.append(
            {"data": {"id": f"member_{mid}", "label": label, "type": "member"}}
        )

    # Collaborators
    for cid, name, aff in collaborators:
        label = f"{name}" if aff else name
        label = label.replace(" ", "\n").replace("_", "\n")
        nodes.append(
            {"data": {"id": f"collab_{cid}", "label": label, "type": "collaborator"}}
        )

    # Funding
    for fid, org in funding:
        label = org.replace(" ", "\n").replace("_", "\n")
        nodes.append(
            {"data": {"id": f"funding_{fid}", "label": label, "type": "funding"}}
        )

    # Program ↔ Collaborators
    for prog_id, collab_id in program_collabs:
        edges.append(
            {
                "data": {
                    "source": f"program_{prog_id}",
                    "target": f"collab_{collab_id}",
                    "label": "has collaborator",
                }
            }
        )

    # Program ↔ Funding
    for prog_id, fund_id in program_funding:
        edges.append(
            {
                "data": {
                    "source": f"program_{prog_id}",
                    "target": f"funding_{fund_id}",
                    "label": "funded by",
                }
            }
        )

    # Project ↔ Members
    for proj_id, mem_id in project_members:
        edges.append(
            {
                "data": {
                    "source": f"member_{mem_id}",
                    "target": f"project_{proj_id}",
                    "label": "works on",
                }
            }
        )

    # Program ↔ Members
    for prog_id, mem_id in program_members:
        keep_edge = True
        for proj_id, _, _, _, _ in projects:
            test_edge = {
                "data": {
                    "source": f"member_{mem_id}",
                    "target": f"project_{proj_id}",
                    "label": "works on",
                }
            }
            test_edge_proj = {
                "data": {
                    "source": f"program_{prog_id}",
                    "target": f"project_{proj_id}",
                    "label": "includes",
                }
            }
            if test_edge in edges and test_edge_proj in edges:
                keep_edge = False
        if keep_edge:
            edges.append(
                {
                    "data": {
                        "source": f"program_{prog_id}",
                        "target": f"member_{mem_id}",
                        "label": "has member",
                    }
                }
            )

    con.close()

    # print(edges[0])
    # print({'data': {'source': 'program_ae83c681-62b0-4cfe-840f-d23e6de0dd1c', 'target': 'project_0d9db150-89f2-49b2-beda-4a99441531d7', 'label': 'includes'}} in edges)

    # add edge ids
    for i, e in enumerate(edges):
        if "id" not in e["data"]:
            e["data"]["id"] = f"edge-{e['data']['source']}-{e['data']['target']}-{i}"

    return nodes, edges
