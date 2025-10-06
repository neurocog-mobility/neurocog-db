# gui/queries.py
import duckdb
from neurocogdb.config.paths import fetch_ddb_path


def get_connection():
    return duckdb.connect(fetch_ddb_path())


def get_project_status_counts():
    con = get_connection()
    df = con.execute(
        """
        SELECT status, COUNT(*) AS count
        FROM (
            SELECT 
                CASE 
                    WHEN end_date IS NOT NULL AND end_date < CURRENT_DATE THEN 'completed'
                    WHEN start_date IS NOT NULL AND start_date > CURRENT_DATE THEN 'upcoming'
                    ELSE 'active'
                END AS status
            FROM projects
        ) sub
        GROUP BY status
    """
    ).df()
    con.close()
    return df


def get_participants_per_project():
    con = get_connection()
    df = con.execute(
        """
        SELECT p.name as project, 
               SUM(pp.collected) as collected, 
               SUM(pp.total) as target
        FROM project_participants pp
        JOIN projects p ON pp.project_id = p.id
        WHERE (p.start_date IS NULL OR p.start_date <= CURRENT_DATE)
        AND (p.end_date IS NULL OR p.end_date >= CURRENT_DATE)
        GROUP BY p.name
    """
    ).df()
    con.close()
    return df


def get_project_timeline():
    con = get_connection()
    df = con.execute(
        """
        SELECT name, start_date, end_date
        FROM projects
    """
    ).df()
    con.close()
    return df


def get_locations_summary():
    con = get_connection()
    df = con.execute(
        """
        SELECT l.name as location, COUNT(pl.project_id) as active_projects
        FROM project_locations pl
        JOIN locations l ON pl.location_id = l.id
        JOIN projects p ON p.id = pl.project_id
        WHERE (p.start_date IS NULL OR p.start_date <= CURRENT_DATE)
        AND (p.end_date IS NULL OR p.end_date >= CURRENT_DATE)
        GROUP BY l.name
        ORDER BY active_projects DESC
    """
    ).df()
    con.close()
    return df


def get_funding_summary():
    con = get_connection()
    df = con.execute(
        """
        SELECT f.organization, COUNT(pf.program_id) as n_programs
        FROM funding f
        JOIN program_funding pf ON f.id = pf.funding_id
        GROUP BY f.organization
        ORDER BY n_programs DESC
    """
    ).df()
    con.close()
    return df


import duckdb
import json
from collections import OrderedDict

def load_projects():
    """
    Load all projects with associated program, funding, participants,
    data sources, outputs, and members from DuckDB.

    JSON arrays are converted to Python lists, with deduplication.
    """
    con = get_connection()

    query = """
    SELECT
        p.id,
        p.name,
        CASE 
            WHEN p.end_date IS NOT NULL AND p.end_date < CURRENT_DATE THEN 'completed'
            WHEN p.start_date IS NOT NULL AND p.start_date > CURRENT_DATE THEN 'upcoming'
            ELSE 'ongoing'
        END AS status,
        p.start_date,
        p.end_date,
        p.source_path,
        -- prog.name AS program,
        JSON_GROUP_ARRAY(JSON_OBJECT('name', prog.name, 'source', prog.source_path)) AS program,
        JSON_GROUP_ARRAY(JSON_OBJECT('organization', f.organization)) AS funding,
        JSON_GROUP_ARRAY(JSON_OBJECT('label', pp.label, 'collected', COALESCE(pp.collected, 0), 'total', COALESCE(pp.total, 0))) AS participant_groups,
        JSON_GROUP_ARRAY(JSON_OBJECT('modality', d.modality, 'device', d.device)) AS data_sources,
        JSON_GROUP_ARRAY(JSON_OBJECT('type', o.type, 'name', po.name, 'url', po.url, 'date', po.date)) AS outputs,
        JSON_GROUP_ARRAY(JSON_OBJECT('name', m.name, 'role', m.role, 'valid', m.valid)) AS members

    FROM projects p
    LEFT JOIN programs prog ON p.program_id = prog.id
    LEFT JOIN program_funding pf ON prog.id = pf.program_id
    LEFT JOIN funding f ON pf.funding_id = f.id
    LEFT JOIN project_participants pp ON p.id = pp.project_id
    LEFT JOIN project_data pd ON p.id = pd.project_id
    LEFT JOIN data d ON pd.data_id = d.id
    LEFT JOIN project_outputs po ON p.id = po.project_id
    LEFT JOIN outputs o ON po.output_id = o.id
    LEFT JOIN project_members pm ON p.id = pm.project_id
    LEFT JOIN members m ON pm.member_id = m.id

    GROUP BY p.id, p.name, p.start_date, p.end_date, p.source_path, prog.name
    ORDER BY p.start_date DESC;
    """

    df = con.execute(query).df()

    # Convert JSON strings to Python lists and deduplicate
    json_cols = ["program", "funding", "participant_groups", "data_sources", "outputs", "members"]
    for col in json_cols:
        def parse_and_dedupe(cell):
            if not cell:
                return []
            items = json.loads(cell)
            # Deduplicate while preserving order
            seen = set()
            deduped = []
            for x in items:
                key = tuple(sorted(x.items()))
                if key not in seen:
                    seen.add(key)
                    deduped.append(x)
            return deduped

        df[col] = df[col].apply(parse_and_dedupe)

    return df
