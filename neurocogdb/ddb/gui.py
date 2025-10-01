# package/src/ddb/gui.py
import os
import duckdb
import streamlit as st
import pandas as pd
from neurocogdb.load.sync import sync_ddb

def main():
    db_path = os.path.join(os.path.dirname(__file__), "lab_catalog.ddb")

    @st.cache_data
    def load_data():
        con = duckdb.connect(db_path, read_only=True)
        
        # --- Programs ---
        programs = con.execute("SELECT * FROM programs").df()
        
        # --- Members ---
        members = con.execute("SELECT * FROM members").df()
        
        # --- Program members ---
        program_members = con.execute("""
            SELECT pm.program_id, m.name AS member_name, pm.role
            FROM program_members pm
            LEFT JOIN members m ON pm.member_id = m.id
        """).df()
        prog_members_agg = program_members.groupby("program_id")["member_name"].apply(lambda x: ", ".join(x)).reset_index()
        programs = programs.merge(prog_members_agg, left_on="id", right_on="program_id", how="left")
        
        # --- Funding ---
        funding = con.execute("SELECT * FROM funding").df()
        program_funding = con.execute("""
            SELECT pf.program_id, f.organization
            FROM program_funding pf
            LEFT JOIN funding f ON pf.funding_id = f.id
        """).df()
        prog_funding_agg = program_funding.groupby("program_id")["organization"].apply(lambda x: ", ".join(x)).reset_index()
        programs = programs.merge(prog_funding_agg, left_on="id", right_on="program_id", how="left")
        
        # --- Projects ---
        projects = con.execute("""
            SELECT p.*, prog.name AS program_name
            FROM projects p
            LEFT JOIN programs prog ON p.program_id = prog.id
        """).df()
        
        # --- Project members ---
        project_members = con.execute("""
            SELECT pm.project_id, m.name AS member_name
            FROM project_members pm
            LEFT JOIN members m ON pm.member_id = m.id
        """).df()
        proj_members_agg = project_members.groupby("project_id")["member_name"].apply(lambda x: ", ".join(x)).reset_index()
        projects = projects.merge(proj_members_agg, left_on="id", right_on="project_id", how="left")
        
        # --- Project data ---
        project_data = con.execute("""
            SELECT pd.project_id, d.category, d.modality, d.device
            FROM project_data pd
            LEFT JOIN data d ON pd.data_id = d.id
        """).df()
        
        con.close()
        return programs, projects, project_data, members, funding

    # --- Streamlit UI ---
    st.set_page_config(page_title="NeuroCogDB", layout="wide")
    st.title("NeuroCogDB")

    if st.button("Refresh Database"):
        sync_ddb()
        st.success("Database recreated successfully!")
        st.cache_data.clear()
        # Force rerun so updated values appear
        st.rerun()

    # --- Load all data ---
    programs, projects, project_data, members, funding = load_data()

    # --- Sidebar filters ---
    st.sidebar.header("Filters")

    # Program filter
    program_options = ["All"] + programs["name"].tolist()
    selected_program = st.sidebar.selectbox("Program", program_options)

    # Project status filter
    status_options = ["All"] + projects["status"].dropna().unique().tolist()
    selected_status = st.sidebar.selectbox("Project Status", status_options)

    # Member filter (any program/project member)
    all_member_names = members["name"].tolist()
    selected_member = st.sidebar.selectbox("Member", ["All"] + all_member_names)

    # Data modality filter
    all_modalities = project_data["modality"].dropna().unique().tolist()
    selected_modality = st.sidebar.selectbox("Data Modality", ["All"] + all_modalities)

    # Funding filter
    all_funding = funding["organization"].tolist()
    selected_funding = st.sidebar.selectbox("Funding Org", ["All"] + all_funding)

    # --- Filter projects ---
    filtered_projects = projects.copy()

    # Program filter
    if selected_program != "All":
        filtered_projects = filtered_projects[filtered_projects["program_name"] == selected_program]

    # Status filter
    if selected_status != "All":
        filtered_projects = filtered_projects[filtered_projects["status"] == selected_status]

    # Member filter: check if member appears in project member list or program member list
    if selected_member != "All":
        filtered_projects = filtered_projects[
            filtered_projects["member_name"].str.contains(selected_member, na=False)
        ]

    # Funding filter: filter projects whose program has the selected funding
    if selected_funding != "All":
        programs_with_funding = programs[programs["organization"].str.contains(selected_funding, na=False)]
        filtered_projects = filtered_projects[filtered_projects["program_id"].isin(programs_with_funding["id"])]

    # --- Drill-down with expanders ---
    for _, prog_row in programs.iterrows():
        # Apply program filter
        if selected_program != "All" and prog_row["name"] != selected_program:
            continue
        
        with st.expander(f"Program: {prog_row['name']} | Members: {prog_row.get('member_name','')} | Funding: {prog_row.get('organization','')}", expanded=True):
            st.write(f"Start: {prog_row['start_date']}, End: {prog_row['end_date']}")
            
            # Projects under this program and filtered by sidebar
            prog_projects = filtered_projects[filtered_projects["program_id"] == prog_row["id"]]
            
            if prog_projects.empty:
                st.info("No projects for this program (with current filters)")
                continue
            
            for _, proj_row in prog_projects.iterrows():
                with st.expander(f"Project: {proj_row['name']} | Members: {proj_row.get('member_name','')} | Status: {proj_row['status']}"):
                    st.write(f"Start: {proj_row['start_date']}, End: {proj_row['end_date']}")
                    st.write(f"Data Path: {proj_row['data_path']}")
                    
                    # Project data, filtered by modality
                    proj_data = project_data[project_data["project_id"] == proj_row["id"]]
                    if selected_modality != "All":
                        proj_data = proj_data[proj_data["modality"] == selected_modality]
                    
                    if not proj_data.empty:
                        st.subheader("Data Entries")
                        st.dataframe(proj_data[["category","modality","device"]], width="content")
                    else:
                        st.info("No data entries for this project (with current filters)")

if __name__ == "__main__":
    main()