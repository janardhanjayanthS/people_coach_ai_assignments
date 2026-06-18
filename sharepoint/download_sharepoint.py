import os

import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# --- Site-specific config ---
SHAREPOINT_HOSTNAME = "bitcotaiinc.sharepoint.com"
SITE_PATH = "/sites/GlobalResourcessample"
LIBRARY_NAME = "Knowledge Base Documents"  # the document library (drive) name

LOCAL_ROOT = "./downloads"

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def get_access_token() -> str:
    """Authenticate using client credentials flow and return a bearer token."""
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    )
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    if "access_token" not in result:
        raise RuntimeError(
            f"Failed to acquire token: {result.get('error_description')}"
        )
    return result["access_token"]


def get_site_id(token: str) -> str:
    """Resolve the SharePoint site ID from hostname + site path."""
    url = f"{GRAPH_BASE}/sites/{SHAREPOINT_HOSTNAME}:{SITE_PATH}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    return resp.json()["id"]


def get_drive_id(token: str, site_id: str) -> str:
    """Find the drive (document library) ID matching LIBRARY_NAME."""
    url = f"{GRAPH_BASE}/sites/{site_id}/drives"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    drives = resp.json()["value"]

    for drive in drives:
        if drive["name"].lower() == LIBRARY_NAME.lower():
            return drive["id"]

    available = [d["name"] for d in drives]
    raise ValueError(
        f"Library '{LIBRARY_NAME}' not found. Available libraries: {available}"
    )


def list_children(token: str, drive_id: str, item_id: str = "root") -> list:
    """List immediate children (files + folders) of a drive item."""
    url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/children"
    items = []
    while url:
        resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        data = resp.json()
        items.extend(data.get("value", []))
        url = data.get("@odata.nextLink")  # handle pagination
    return items


def download_file(item: dict, local_path: str):
    """Download a single file using its download URL."""
    if os.path.exists(local_path):
        print(f"  SKIP (already exists): {local_path}")
        return

    download_url = item.get("@microsoft.graph.downloadUrl")
    if not download_url:
        print(f"  WARNING: no download URL for {item['name']}, skipping")
        return

    resp = requests.get(download_url)
    resp.raise_for_status()

    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(resp.content)
    print(f"  Downloaded: {local_path}")


def process_folder(token: str, drive_id: str, item_id: str, local_dir: str):
    """Recursively walk a folder, downloading files and descending into subfolders."""
    os.makedirs(local_dir, exist_ok=True)
    children = list_children(token, drive_id, item_id)

    for item in children:
        item_name = item["name"]
        local_path = os.path.join(local_dir, item_name)

        if "folder" in item:
            print(f"Entering folder: {local_path}")
            process_folder(token, drive_id, item["id"], local_path)
        elif "file" in item:
            download_file(item, local_path)
        else:
            print(f"  Skipping unknown item type: {item_name}")


def call_drive_items_delta(
    drive_id: str, token: str, item_id: str = "root", delta_link: str = None
) -> None:
    """Fetch and display delta (changes) for items inside the Knowledge Base Documents library.

    Delta tracks ALL items in the drive from the beginning of time on first call.
    Subsequent calls with a deltaLink return only what changed since last call.

    Change types:
        - created/modified : item appears normally in response
        - deleted          : item has a ``deleted`` facet, no other metadata

    Args:
        drive_id: Graph drive ID (already scoped to Knowledge Base Documents library).
        token: Bearer access token.
        item_id: Item ID to start delta from. Defaults to ``root`` (entire library).
        delta_link: Full deltaLink URL from a previous call. When provided, returns
            only changes since that call — ignores drive_id and item_id.
    """
    url = (
        delta_link
        if delta_link
        else f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/delta"
    )
    headers = {"Authorization": f"Bearer {token}"}

    all_items = []
    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        all_items.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    delta_link = data.get("@odata.deltaLink")

    print(f"\nDelta results for library: {LIBRARY_NAME}")
    print(f"Total items tracked: {len(all_items)}\n")

    for item in all_items:
        name = item.get("name", "(no name)")
        modified = item.get("lastModifiedDateTime", "")
        parent_path = item.get("parentReference", {}).get("path", "")

        if "deleted" in item:
            print(f"  [DELETED]  {name}")
        elif "folder" in item:
            print(f"  [FOLDER]   {name}  |  {parent_path}")
        elif "file" in item:
            size = item.get("size", 0)
            print(f"  [FILE]     {name}  |  {size} bytes  |  modified: {modified}")
        else:
            print(f"  [UNKNOWN]  {name}")

    print(f"\ndeltaLink (use for next incremental call):\n  {delta_link}")


def main():
    print("Authenticating...")
    token = get_access_token()

    print("Resolving site ID...")
    site_id = get_site_id(token)

    print("Resolving drive ID...")
    drive_id = get_drive_id(token, site_id)

    # print(f"Starting download into '{LOCAL_ROOT}'...\n")
    # process_folder(token, drive_id, "root", LOCAL_ROOT)

    # print("\nDone.")

    call_drive_items_delta(
        drive_id=drive_id,
        token=token,
        item_id="root",
        delta_link="https://graph.microsoft.com/v1.0/drives/b!WaLqR-lap0ipeoruYp7Ur9UWnC1U-jpJlOUf0-sRyqCorH_7PKgnR5FBGzJgOmhg/items/root/delta?token=NDslMjM0OyUyMzE7MztmYjdmYWNhOC1hODNjLTQ3MjctOTE0MS0xYjMyNjAzYTY4NjA7NjM5MTcyNzkwNDM3MTMwMDAwOzE2MjcxMTMwOTU7JTIzOyUyMzslMjMwOyUyMw",
    )


if __name__ == "__main__":
    main()
