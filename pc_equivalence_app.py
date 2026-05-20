import streamlit as st

# -----------------------------
# Performance calculation logic
# -----------------------------
def performance_index(cores, ghz, ipc_factor):
    return cores * ghz * ipc_factor

def compare_systems(old_specs, new_specs):
    old_perf = performance_index(old_specs["cores"], old_specs["ghz"], old_specs["ipc"])
    new_perf = performance_index(new_specs["cores"], new_specs["ghz"], new_specs["ipc"])
    cpu_ratio = new_perf / old_perf

    ram_ratio = new_specs["ram_gb"] / old_specs["ram_gb"]
    storage_ratio = new_specs["storage_gb"] / old_specs["storage_gb"]

    return cpu_ratio, ram_ratio, storage_ratio


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="PC Equivalence Calculator", page_icon="🖥️")

st.markdown(
    "<h1 style='text-align: center;'>🖥️ PC Equivalence Calculator</h1>",
    unsafe_allow_html=True,
)
st.write("We all remember growing up using a PC that, compared to today's machines, seems incredibly slow. "
         "Have you ever wondered how many of your old PCs it would take to power your modern machine? "
         "Use this tool to find out!")

st.markdown(
    """
    <style>
    .ipc-label-row {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        margin-bottom: 0.2rem;
        font-size: 0.95rem;
        font-weight: 500;
    }

    .ipc-help-wrap {
        position: relative;
        display: inline-flex;
        align-items: center;
    }

    .ipc-help-icon {
        width: 1rem;
        height: 1rem;
        border-radius: 50%;
        border: 1px solid #9ca3af;
        color: #6b7280;
        font-size: 0.72rem;
        font-weight: 700;
        line-height: 1rem;
        text-align: center;
        cursor: help;
        user-select: none;
    }

    .ipc-tooltip {
        visibility: hidden;
        opacity: 0;
        transition: opacity 0.15s ease;
        position: absolute;
        left: 1.35rem;
        top: -0.25rem;
        z-index: 999;
        width: 260px;
        background: #111827;
        color: #f9fafb;
        border-radius: 8px;
        padding: 0.55rem 0.65rem;
        font-size: 0.78rem;
        line-height: 1.35;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25);
    }

    .ipc-help-wrap:hover .ipc-tooltip {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

OLD_PC_PRESETS = {
    "Custom": None,
    "IBM PC 5150 (1981)": {"cores": 1, "mhz": 4.77, "ipc": 1.0, "ram_mb": 64.0, "storage_mb": 10.0},
    "IBM PC XT (1983)": {"cores": 1, "mhz": 4.77, "ipc": 1.05, "ram_mb": 128.0, "storage_mb": 10000.0},
    "Apple IIe (1983)": {"cores": 1, "mhz": 1.023, "ipc": 0.9, "ram_mb": 64.0, "storage_mb": 140.0},
    "Commodore 64 (1982)": {"cores": 1, "mhz": 1.0, "ipc": 0.85, "ram_mb": 64.0, "storage_mb": 140.0},
    "Macintosh Plus (1986)": {"cores": 1, "mhz": 8.0, "ipc": 1.2, "ram_mb": 512.0, "storage_mb": 800.0},
    "486 DX2/66 (1992)": {"cores": 1, "mhz": 66.0, "ipc": 1.6, "ram_mb": 4096.0, "storage_mb": 512000.0},
    "Pentium 90 (1994)": {"cores": 1, "mhz": 90.0, "ipc": 2.0, "ram_mb": 8192.0, "storage_mb": 1000000.0},
}


def apply_old_pc_preset() -> None:
    preset_values = OLD_PC_PRESETS.get(st.session_state.old_pc_preset)
    if not preset_values:
        return

    st.session_state.old_cores = preset_values["cores"]
    st.session_state.old_mhz = preset_values["mhz"]
    st.session_state.old_ipc = preset_values["ipc"]
    st.session_state.old_ram = preset_values["ram_mb"]
    st.session_state.old_storage = preset_values["storage_mb"]


NEW_PC_PRESETS = {
    "Custom": None,
    "High-End Gaming Desktop (2024)": {"cores": 16, "ghz": 5.6, "ipc": 6.0, "ram_gb": 32.0, "storage_gb": 2000.0},
    "MacBook Pro M3 Max (2023)": {"cores": 16, "ghz": 4.05, "ipc": 7.5, "ram_gb": 36.0, "storage_gb": 1000.0},
    "Ultrabook Laptop (2024)": {"cores": 8, "ghz": 5.0, "ipc": 6.5, "ram_gb": 16.0, "storage_gb": 512.0},
    "iPhone 15 Pro": {"cores": 6, "ghz": 3.8, "ipc": 7.0, "ram_gb": 8.0, "storage_gb": 256.0},
    "Samsung Galaxy S24 Ultra": {"cores": 8, "ghz": 3.4, "ipc": 6.8, "ram_gb": 12.0, "storage_gb": 512.0},
    "Google Pixel 8 Pro": {"cores": 8, "ghz": 3.3, "ipc": 6.7, "ram_gb": 12.0, "storage_gb": 256.0},
}


def apply_new_pc_preset() -> None:
    preset_values = NEW_PC_PRESETS.get(st.session_state.new_pc_preset)
    if not preset_values:
        return

    st.session_state.new_cores = preset_values["cores"]
    st.session_state.new_ghz = preset_values["ghz"]
    st.session_state.new_ipc = preset_values["ipc"]
    st.session_state.new_ram = preset_values["ram_gb"]
    st.session_state.new_storage = preset_values["storage_gb"]

st.header("Old PC Specs")
st.selectbox(
    "Example Presets",
    list(OLD_PC_PRESETS.keys()),
    key="old_pc_preset",
    on_change=apply_old_pc_preset,
)
st.caption("Choose a preset to populate the old PC fields, or keep Custom to enter your own values.")
st.session_state.setdefault("old_cores", 1)
st.session_state.setdefault("old_mhz", 533.0)
st.session_state.setdefault("old_ipc", 1.0)
st.session_state.setdefault("old_ram", 128.0)
st.session_state.setdefault("old_storage", 2000.0)
old_cores = st.number_input("CPU Cores", min_value=1, key="old_cores")
old_mhz = st.number_input("Clock Speed (MHz)", min_value=0.1, key="old_mhz")
st.markdown(
    """
    <div class="ipc-label-row">
        <span>IPC Factor (baseline = 1)</span>
        <span class="ipc-help-wrap">
            <span class="ipc-help-icon">?</span>
            <span class="ipc-tooltip">IPC (Instructions Per Cycle) is how much work a CPU does each clock cycle. Higher IPC means better performance at the same clock speed.</span>
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
old_ipc = st.number_input(
    "old_ipc_label_hidden",
    min_value=0.1,
    key="old_ipc",
    label_visibility="collapsed",
)
old_ram = st.number_input("RAM (MB)", min_value=0.001, key="old_ram", format="%.3f")
old_storage = st.number_input("Storage (MB)", min_value=0.001, key="old_storage")

st.header("New PC Specs")
st.selectbox(
    "Example Presets",
    list(NEW_PC_PRESETS.keys()),
    key="new_pc_preset",
    on_change=apply_new_pc_preset,
)
st.caption("Choose a preset to populate the new PC fields, or keep Custom to enter your own values.")
st.session_state.setdefault("new_cores", 8)
st.session_state.setdefault("new_ghz", 3.4)
st.session_state.setdefault("new_ipc", 5.0)
st.session_state.setdefault("new_ram", 16.0)
st.session_state.setdefault("new_storage", 2048.0)
new_cores = st.number_input("CPU Cores", min_value=1, key="new_cores")
new_ghz = st.number_input("Clock Speed (GHz)", min_value=0.1, key="new_ghz")
st.markdown(
    """
    <div class="ipc-label-row">
        <span>IPC Factor (modern CPUs ~4-6x)</span>
        <span class="ipc-help-wrap">
            <span class="ipc-help-icon">?</span>
            <span class="ipc-tooltip">IPC (Instructions Per Cycle) is how much work a CPU does each clock cycle. Newer CPU architectures usually have a higher IPC than older ones.</span>
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
new_ipc = st.number_input(
    "new_ipc_label_hidden",
    min_value=0.1,
    key="new_ipc",
    label_visibility="collapsed",
)
new_ram = st.number_input("RAM (GB)", min_value=0.1, key="new_ram")
new_storage = st.number_input("Storage (GB)", min_value=0.1, key="new_storage")

if st.button("Calculate"):
    old_specs = {
        "cores": old_cores,
        "ghz": old_mhz / 1000.0,
        "ipc": old_ipc,
        "ram_gb": old_ram / 1000.0,
        "storage_gb": old_storage / 1000.0
    }

    new_specs = {
        "cores": new_cores,
        "ghz": new_ghz,
        "ipc": new_ipc,
        "ram_gb": new_ram,
        "storage_gb": new_storage
    }

    cpu_ratio, ram_ratio, storage_ratio = compare_systems(old_specs, new_specs)

    st.subheader("Results")
    st.write(f"**CPU Power:** It would take **{cpu_ratio:.1f}** of your old PCs to power your new PC")
    st.write(f"**RAM Capacity:** Your new PC has as much RAM as **{ram_ratio:.1f}** of your old PCs")
    st.write(f"**Storage Size:** Your new PC has as much storage as **{storage_ratio:.1f}** of your old PCs")

    st.success("Calculation complete!")
