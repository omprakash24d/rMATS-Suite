import streamlit as st
import pandas as pd
import os
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

st.set_page_config(page_title="rMATS-Suite: Alternative Splicing Analysis & Visualization Toolkit", layout="wide")

st.markdown("""
    <style>
    /* Force high-contrast Light Mode */
    .stApp { background-color: #FFFFFF !important; color: #1A1A1A !important; }
    header { background-color: #FFFFFF !important; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #F0F2F6 !important; border-right: 1px solid #DDE2E6; }
    
    /* Buttons: Deep Sea Blue */
    .stButton>button { 
        background-color: #004085 !important; color: white !important; border-radius: 4px; 
        font-weight: 600; width: 100%; border: none; padding: 0.5rem;
    }
    .stButton>button:hover { background-color: #002752 !important; color: #FFFFFF !important; }

    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background-color: #F8F9FA !important; color: #1A1A1A !important;
        border: 1px solid #CED4DA !important;
    }
    
    /* Terminal Console Style */
    code { 
        color: #000000 !important; 
        background-color: #F1F3F5 !important; 
        border-left: 5px solid #004085 !important;
        display: block;
        padding: 10px;
    }
    
    h1, h2, h3 { color: #002752; font-family: 'Inter', sans-serif; }
    
    /* Clean Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px; 
        background-color: transparent; 
        border-bottom: 2px solid #F0F2F6;
    }
    .stTabs [data-baseweb="tab"] { 
        font-weight: 700; 
        color: #495057; 
        font-size: 1rem; 
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        border: none !important;
        transition: background-color 0.2s ease;
    }
    .stTabs [aria-selected="true"] { 
        color: #FFFFFF !important; 
        background-color: #004085 !important; 
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #F8F9FA;
        color: #004085;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Title ---
st.title("rMATS-Suite: Alternative Splicing Analysis & Visualization Toolkit")
st.caption("A high-performance portal for the automated detection of differential alternative splicing events (SE, MXE, A3SS, A5SS, RI) and the generation of publication-quality Sashimi visualizations. Built for researchers to seamlessly navigate from raw alignment data to statistical insights and isoform-level genomic plots.")

with st.expander("🚀 **Optimization & Best Practices**", expanded=True):
    st.markdown("""
        *   **I/O Performance:** For the fastest results, ensure your data is stored on an **SSD**.
        *   **Compute Power:** Maximize **CPU Threads** (24+ recommended) in the sidebar to reduce run time.
        *   **Plotting Ready:** Ensure BAM files are **indexed (.bai)** before generating Sashimi plots.
        *   **Clean Workflow:** Use distinct **Comparison IDs** to organize different experimental runs.
    """)

st.divider()

# --- Help Dialog ---
@st.dialog("rMATS-Suite: User Guide", width="large")
def show_help():
    # Scroll-to-top script
    st.components.v1.html("""
        <script>
            function forceScroll() {
                const dialog = window.parent.document.querySelector('div[role="dialog"]');
                if (dialog) {
                    dialog.scrollTop = 0;
                }
            }
            // Execute multiple times to catch rendering updates
            forceScroll();
            setTimeout(forceScroll, 100);
            setTimeout(forceScroll, 300);
            setTimeout(forceScroll, 1000);
        </script>
    """, height=0)
    
    # Top Close Button to prevent autofocusing at the bottom
    if st.button("Close Guide ", key="top_close"):
        st.rerun()

    st.markdown("""
        <style>
            div[data-testid="stDialog"] div[role="dialog"] {
                width: 90vw !important;
                max-width: 90vw !important;
            }
        </style>
        """, unsafe_allow_html=True)
    st.markdown("""
        ## 📚 Help Center
        This suite provides a high-performance graphical interface for **rMATS-turbo** and **Sashimi visualizations**. Follow this guide to get the most out of the tool.
        ---

        ### 📊 Phase 1: Running Differential Splicing Analysis
        Use the **"Run rMATS Analysis"** tab to process raw alignment files.
        
        1.  **Configure Compute:** In the sidebar, set **CPU Threads** to the maximum your system allows (e.g., 24, 32, or 64).
        2.  **Prepare Inputs:** 
            - Provide the absolute path to your **GTF Annotation** file.
            - List your **Group 1** and **Group 2** BAM files (one per line). 
            - *Note:* Files must be coordinate-sorted.
        3.  **Define Output:** Set a **Base Directory** and a unique **Comparison ID**. This prevents overwriting previous experiments.
        4.  **Execute:** Click the **Execute** button. The **Live Terminal** below will stream the rMATS engine logs in real-time. Wait for the "Analysis Complete!" message and balloons.

        ### 🎨 Phase 2: Generating Publication-Ready Sashimi Plots
        Use the **"Gene-Specific Sashimi Plots"** tab for visualization.

        1.  **Connect Data:** Point the **rMATS Result Dir** to the folder generated in Phase 1.
        2.  **Automated Search:** Enter a gene symbol (e.g., `SRSF11`). The app will instantly filter the results.
        3.  **Event Selection:** Review the table for FDR and Inclusion Levels. Select the specific **Event ID** you want to visualize from the dropdown.
        4.  **Plotting:** Click **Generate Sashimi Plot**. The engine will produce a detailed PDF showing genomic coverage and junction counts, saved in a `Sashimi_Plots` subfolder.

        ---

        ### 🚀 Performance & Optimization Tips
        *   **SSD vs HDD:** Bioinformatics I/O is the biggest bottleneck. Storing BAM files on an **SSD** can reduce processing time by over 50%.
        *   **BAM Indexing:** Every `.bam` file **MUST** have a matching `.bai` index in the same directory. If you don't have them, run `samtools index file.bam`.
        *   **Thread Scaling:** rMATS is highly parallel. Always allocate as many threads as possible for the statistical engine.
        *   **Absolute Paths:** Ensure all file paths start from the root (`/media/...` or `/home/...`). Relative paths may fail inside the Docker environment.

        ### 🛠 Troubleshooting
        *   **Permission Issues:** If generated files are read-only, run: `sudo chown -R $USER:$USER /your/output/path`.
        *   **Docker Errors:** Ensure your user is in the `docker` group and the Docker service is running.
        *   **Search No Matches:** Ensure the "Event Class" (SE, MXE, etc.) matches the type of splicing event you are looking for.

        ---
        *Designed and Developed wby Om.*
    """)
    if st.button("Close Guide", use_container_width=True):
        st.rerun()

with st.sidebar:
    if st.button("Help Center", use_container_width=True):
        show_help()
    
    st.header("⚙️ Global Config")
    THREADS = st.number_input("CPU Threads", value=24, help="Number of CPU cores allocated for analysis. 24-48 recommended for large datasets.")
    READLEN = st.number_input("Read Length (bp)", value=151, help="Total length of each sequencing read (e.g., 151 for 2x150bp paired-end).")
    LIBTYPE = st.selectbox("Library Type", ["fr-unstranded", "fr-firststrand", "fr-secondstrand"], index=1, 
                           help="Strandedness of the RNA-Seq library. 'fr-firststrand' is standard for most Illumina dUTP kits.")
    DOCKER_IMG = st.text_input("Docker Image", value="rmats-suite:latest", disabled=True, 
                               help="The fixed containerized environment for rMATS and Sashimi plotting.")
    
    st.divider()
    st.markdown("### 🏛️ Credits")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.link_button("rMATS", "https://github.com/Xinglab/rmats-turbo", use_container_width=True)
    with c_col2:
        st.link_button("Sashimi", "https://github.com/Xinglab/rmats2sashimiplot", use_container_width=True)
    
    with st.expander("📝 Cite rMATS"):
        st.caption("Shen S, Park JW, Lu ZX, Lin L, Henry MD, Wu YN, Zhou Q, Xing Y. **rMATS: Robust and flexible detection of differential alternative splicing from replicate RNA-Seq data.** *Proc Natl Acad Sci U S A.* 2014;111(51):E5593-601.")

tab1, tab2 = st.tabs(["📊 Run rMATS Analysis", "🎨 Gene-Specific Sashimi Plots"])

# --- TAB 1: RMATS PIPELINE ---
with tab1:
        
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📂 Inputs")
        gtf_path = st.text_input("GTF Annotation", "/media/erpl/hdd4/Om/rMATSGUI/Homo_sapiens.GRCh38.111.chr.gtf", 
                                help="Absolute path to the reference GTF file. Must match the BAM assembly (e.g., GRCh38).")
        b1_in = st.text_area("Group 1 BAMs (Control - One per line)", 
                            value="/media/erpl/hdd4/Om/AEH_AOH/aligned/AEN1_Aligned.sortedByCoord.out.bam\n/media/erpl/hdd4/Om/AEH_AOH/aligned/AEN2_Aligned.sortedByCoord.out.bam",
                            help="Provide absolute paths to BAM files for Group 1. Ensure each path is on a new line.")
    with c2:
        st.subheader("💾 Output")
        out_base = st.text_input("Base Directory", "/media/erpl/hdd4/Om/checking", 
                                help="The parent folder where experiment results will be saved.")
        comp_id = st.text_input("Comparison ID", "rmats_AENx_vs_AONx", 
                               help="A unique name for this analysis run. A subfolder with this name will be created.")
        b2_in = st.text_area("Group 2 BAMs (Experimental - One per line)", 
                            value="/media/erpl/hdd4/Om/AEH_AOH/aligned/AON1_Aligned.sortedByCoord.out.bam\n/media/erpl/hdd4/Om/AEH_AOH/aligned/AON2_Aligned.sortedByCoord.out.bam",
                            help="Provide absolute paths to BAM files for Group 2. Ensure each path is on a new line.")

    if st.button("EXECUTE RMATS ANALYSIS"):
        out_dir = os.path.join(out_base, comp_id)
        os.makedirs(out_dir, exist_ok=True)

        # Prepare path files
        b1_list = [f"/data{x.strip()}" for x in b1_in.split("\n") if x.strip()]
        b2_list = [f"/data{x.strip()}" for x in b2_in.split("\n") if x.strip()]
        
        b1_txt = os.path.join(out_dir, "b1.txt")
        b2_txt = os.path.join(out_dir, "b2.txt")
        with open(b1_txt, "w") as f: f.write(",".join(b1_list))
        with open(b2_txt, "w") as f: f.write(",".join(b2_list))

        st.subheader("⚙️ Process Logs")
        log_win = st.empty()
        
        # Custom Echo Headers
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        terminal_header = f"Starting rMATS analysis at {start_time}\n"
        terminal_header += "-"*45 + "\n"
        
        cmd = [
            "docker", "run", "--rm", "-e", "PYTHONUNBUFFERED=1", "-v", "/:/data", DOCKER_IMG,
            "python", "/opt/rmats/rmats.py",
            "--b1", f"/data{b1_txt}", "--b2", f"/data{b2_txt}",
            "--gtf", f"/data{gtf_path}", "--od", f"/data{out_dir}",
            "-t", "paired", "--readLength", str(READLEN),
            "--libType", LIBTYPE, "--nthread", str(THREADS)
        ]

        # --- Execution Section ---
        with st.status("🚀 Processing rMATS Analysis...", expanded=True) as status:
            # 💡 Helpful Hardware Tips for the User
            st.info("""
                **Performance Tip:** For the fastest results, ensure your data is stored 
                on an **SSD** rather than an HDD. Allocating **24 or more threads** 
                in the settings will significantly reduce computation time.
            """)

            # Start the subprocess
            proc = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                bufsize=1
            )
            
            full_log = [terminal_header]
            
            # Live Terminal Feed
            for line in iter(proc.stdout.readline, ""):
                full_log.append(line.strip())
                # Displaying the last 18 lines for a clean "scrolling" effect
                log_win.code("\n".join(full_log[-18:]))
            
            proc.wait()
            
            # Final Status Update
            if proc.returncode == 0:
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                st.success(f"✨ Success! Results saved in: {out_dir}")
                st.balloons()
            else:
                status.update(label="Analysis Failed", state="error", expanded=True)
                st.error("Execution stopped. Please check the logs above for library or path errors.")

# --- TAB 2: STREAMLINED SASHIMI ---
with tab2:
    st.subheader("🎨 Gene-Specific Sashimi Plotter")
    st.markdown("Search for a gene, select an automated event, and visualize splicing.")

    with st.expander("📂 1. Source Data Configuration", expanded=True):
        s_c1, s_c2 = st.columns(2)
        with s_c1:
            res_path = st.text_input("rMATS Result Dir", value="/media/erpl/hdd4/Om/checking/rmats_AENx_vs_AONx", 
                                    help="The folder containing the .MATS.JCEC.txt files from Phase 1.")
            ev_type = st.selectbox("Event Class", ["SE", "MXE", "A3SS", "A5SS", "RI"], 
                                  help="Select the splicing event type you wish to search for.")
        with s_c2:
            sb1 = st.text_area("Group 1 BAMs (Comma separated)", value=b1_in.replace("\n", ","),
                              help="Comma-separated absolute paths to Group 1 BAMs. Every BAM must have a .bai index file.")
            sb2 = st.text_area("Group 2 BAMs (Comma separated)", value=b2_in.replace("\n", ","),
                              help="Comma-separated absolute paths to Group 2 BAMs. Every BAM must have a .bai index file.")

    with st.expander("🔍 2. Automated Gene Search", expanded=True):
        target_gene = st.text_input("Search Gene Symbol", placeholder="e.g. SRSF11, TACC3", 
                                   help="Enter the official gene symbol to search within the selected result files.")
        selected_row = None
        
        if target_gene and res_path:
            file_to_read = os.path.join(res_path, f"{ev_type}.MATS.JCEC.txt")
            if os.path.exists(file_to_read):
                df = pd.read_csv(file_to_read, sep="\t")
                # Case-insensitive search
                matches = df[df['geneSymbol'].str.upper() == target_gene.upper()]
                
                if not matches.empty:
                    st.success(f"Found {len(matches)} event(s) for **{target_gene}**")
                    
                    # --- Show all matches first ---
                    st.write("### All Detected Events")
                    st.markdown("Review the coordinates and Inclusion Levels below to choose the correct Event ID:")
                    
                    # We display a cleaned version of the matches for better readability
                    display_cols = ['ID', 'chr', 'strand', 'exonStart_0base', 'exonEnd', 'IncLevelDifference', 'FDR']
                    st.dataframe(matches[display_cols], use_container_width=True)
                    
                    st.divider()
                    
                    # --- Selection Section ---
                    st.write("### Target Selection")
                    ev_id = st.selectbox("Select the specific Event ID to plot:", matches['ID'].tolist(),
                                        help="Pick the unique Event ID from the matches table above to generate the plot.")
                    
                    # Final selection for the plotting engine
                    selected_row = matches[matches['ID'] == ev_id]
                    
                else:
                    st.warning(f"No matches found for '{target_gene}' in {ev_type} results.")

    if st.button("GENERATE SASHIMI PLOT"):
        if selected_row is None:
            st.error("Please select a gene and an event ID first.")
        else:
            s_out = os.path.join(res_path, "Sashimi_Plots", f"{target_gene}_ID{ev_id}")
            os.makedirs(s_out, exist_ok=True)
            
            # Automated Extraction: Create the single-row file required by -e
            e_file = os.path.join(s_out, "target_event.txt")
            selected_row.to_csv(e_file, sep="\t", index=False)

            # Build Docker Command for Sashimi
            s_cmd = [
                "docker", "run", "--rm", "-v", "/:/data", DOCKER_IMG,
                "python", "/opt/sashimi/rmats2sashimiplot.py",
                "--b1", ",".join([f"/data{x.strip()}" for x in sb1.split(",") if x.strip()]),
                "--b2", ",".join([f"/data{x.strip()}" for x in sb2.split(",") if x.strip()]),
                "--event-type", ev_type, 
                "-e", f"/data{e_file}",
                "--exon_s", "1", 
                "--intron_s", "5",
                "--l1", "Group1", 
                "--l2", "Group2", 
                "-o", f"/data{s_out}"
            ]
            
            st.info(f"Rendering: {target_gene} (ID: {ev_id})")
            log_box = st.empty()
            
            with st.status("Generating Plot...") as status:
                proc = subprocess.Popen(s_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                sashimi_logs = [f"Plotting {target_gene} at {datetime.now()}\n", "-"*45]
                for line in iter(proc.stdout.readline, ""):
                    sashimi_logs.append(line.strip())
                    log_box.code("\n".join(sashimi_logs[-10:]))
                proc.wait()
                
                if proc.returncode == 0:
                    status.update(label="Sashimi Plot Ready!", state="complete")
                    st.success(f"Plot saved to: {s_out}")
                else:
                    st.error("Check logs. Ensure BAM files are indexed (.bai) and coordinates match.")

# --- Footer ---
st.divider()
st.markdown(
    """
    <div style="text-align: center; font-size: small;">
        Designed and Developed by <a href="https://om.indhinditech.com" target="_blank" style="color: #FF0000; font-weight: bold; text-decoration: none;">Om</a>
    </div>
    """,
    unsafe_allow_html=True
)