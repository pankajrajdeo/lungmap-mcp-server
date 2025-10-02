# LungMAP Database Agent Tools - Usage Guide (v2.3)

This guide explains how to use the refactored and consolidated LungMAP database tools. This version includes powerful sample-based filtering within the main search tool and clearer boundaries between tools.

**Note for Agent Developers:** The most detailed and up-to-date usage guidance, including `USE WHEN` / `DO NOT USE` instructions and parameter descriptions, is located in the Pydantic `Input` class docstring for each tool. This guide provides a high-level overview and workflow examples.

## Core Principles of the New Design

1.  **Consolidation:** A single primary discovery tool (`lungmap_search_datasets`) handles most search needs.
2.  **Clear Boundaries:** Each tool has a distinct purpose, clarified in its description.
3.  **Intelligent Operation:** The search tool handles short queries automatically and provides actionable error and truncation messages.
4.  **Token Efficiency:** `CONCISE` response formats are the default, and all parts of the response are simplified.

## The Tool Suite (8 Tools)

1.  **`lungmap_search_datasets`**: Primary discovery tool for datasets, now with sample characteristic filters.
2.  **`lungmap_get_dataset_details`**: Deep-dive on a single dataset to get all files and comprehensive metadata.
3.  **`lungmap_get_sample_details`**: Deep-dive on a single sample.
4.  **`lungmap_get_analysis_results`**: Get computational analysis results for datasets.
5.  **`lungmap_get_molecular_entities`**: Look up genes, proteins, probes, etc.
6.  **`lungmap_get_infrastructure_resources`**: Look up researchers, sites, and tools.
7.  **`lungmap_list_controlled_vocabulary`**: Discover valid filter terms.
8.  **`lungmap_search_media`**: Search for files or images across all datasets.

---

## 1. `lungmap_search_datasets`

This is the starting point for almost all workflows. It is used for all dataset discovery tasks.

### Key Features:
-   **Unified Search:** Combines text search with filters for datasets *and samples*.
-   **Sample-Based Filtering:** Find datasets that contain samples with specific demographics.
-   **Short-Query Handling:** Automatically maps terms like "RNA" to the correct filter.

### Workflow Examples:

**A. Find datasets containing specific samples:**
```python
# Find datasets that contain samples from healthy, adult, male donors
lungmap_search_datasets(
    species="human",
    sample_age_ranges=["adult"],
    sample_sex="male"
)
```

**B. Standard text search:**
```python
# Find mouse datasets related to the gene SFTPC
lungmap_search_datasets(
    text_query="SFTPC",
    species="mouse"
)
```

---

## 2. `lungmap_get_dataset_details`

Use this tool *after* you have a single, specific `dataset_id` to get all information, including files.

### Workflow Example:
```python
# Get all details for a specific dataset, including its files and images
lungmap_get_dataset_details(
    dataset_id="LMEX0000000273",
    include_files=True,
    include_images=True,
    include_image_files=True
)
```

---

## 3. `lungmap_get_sample_details`

Use this tool when you have a specific `sample_id` and need to know more about that individual sample.

### Workflow Example:
```python
# Get all details for a single sample
lungmap_get_sample_details(sample_id="LMSP0000001176")
```

---

## 4. `lungmap_get_analysis_results`

This tool retrieves computational analysis results. It uses a `detail_level` enum for clarity.

### Workflow Example:
```python
# Get the standard analysis results (metadata + gene lists) for a dataset
lungmap_get_analysis_results(
    dataset_ids=["LMEX0000000661"],
    detail_level="standard"
)
```

---

## 5. `lungmap_get_molecular_entities`

This tool is for looking up specific information about molecular or ontological entities.

### Workflow Example:
```python
# Get the members of a specific gene set from an analysis
lungmap_get_molecular_entities(
    entity_type="entity_set",
    entity_ids=["LMHL0000000717"],
    include_members=True
)
```

---

## 6. `lungmap_get_infrastructure_resources`

Use this tool to find information about the people, places, and tools behind the data.

### Workflow Example:
```python
# Find researchers from a specific site
lungmap_get_infrastructure_resources(
    resource_type="researcher", 
    site_ids=["LMSI0000000001"]
)
```

---

## 7. `lungmap_list_controlled_vocabulary`

This is a utility tool to discover the valid filter values that can be used in other tools.

### Workflow Example:
```python
# See what values are accepted for the 'races' filter in `lungmap_search_datasets`
lungmap_list_controlled_vocabulary(category="races")
```

---

## 8. `lungmap_search_media`

This tool allows for top-level searches for files or images across all datasets.

### Workflow Example:
```python
# Find all original image files in the database
lungmap_search_media(
    media_type="files", 
    file_type_ids=["image_original"],
    limit=5
)
```
