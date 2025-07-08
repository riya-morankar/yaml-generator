import streamlit as st
import yaml
import datetime
from pathlib import Path

# Load manifest for repo short names
manifest_path = Path("config/gss_hvs_git_repos.yaml")  
with open(manifest_path) as f:
    manifest = yaml.safe_load(f)

REPO_MAP = manifest.get("repos", {})
REPO_KEYS = list(REPO_MAP.keys())

st.title("GitHub PR Tracker Input Generator")

# Include "All" option
multiselect_options = ["All"] + REPO_KEYS

# User input
selected_repos = st.multiselect(
    "Select repositories (multi-select):",
    options=multiselect_options
)

# Handle "All" logic
if "All" in selected_repos:
    selected_repos = REPO_KEYS

start_date = st.date_input("Start Date", datetime.date.today().replace(day=1))
end_date = st.date_input("End Date", datetime.date.today())

if st.button("Generate YAML"):
    if not selected_repos:
        st.warning("Please select at least one repository.")
    else:
        yaml_data = {
            "repos": ",".join(selected_repos),
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        output_path = "workflow_input.yaml"
        with open(output_path, "w") as f:
            yaml.dump(yaml_data, f)

        st.success("workflow_input.yaml created successfully!")
        st.code(yaml.dump(yaml_data), language="yaml")

        with open(output_path, "rb") as file:
            st.download_button(
                label=" Download workflow_input.yaml",
                data=file,
                file_name="workflow_input.yaml",
                mime="text/yaml"
            )
