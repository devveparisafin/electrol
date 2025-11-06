import streamlit as st
import pdfplumber
import os
import time
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title="Smart PDF Search", page_icon="🔍", layout="wide")

# --- Custom CSS for style ---
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 2.2rem;
            font-weight: bold;
            color: #2E86C1;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            font-size: 1rem;
            color: #555;
            margin-bottom: 2rem;
        }
        .footer {
            text-align: center;
            font-size: 0.9rem;
            color: #999;
            margin-top: 30px;
        }
        .dataframe th, .dataframe td {
            text-align: left !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='title'>🔍 Smart PDF Search Tool</div>", unsafe_allow_html=True)
# st.markdown("<div class='subtitle'>Search across all PDF files in the <b>pdfs/</b> folder</div>", unsafe_allow_html=True)

# --- Folder Check ---
pdf_folder = "pdfs"

if not os.path.exists(pdf_folder):
    st.error(f"❌ Folder '{pdf_folder}' not found! Please create it and add PDFs.")
else:
    search_text = st.text_input("Enter text to search 🔎", placeholder="e.g. વેપારી સાફિન ...")

    if st.button("Start Search 🚀", use_container_width=True):
        if not search_text.strip():
            st.warning("⚠️ Please enter text to search.")
        else:
            results = []
            pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
            total_files = len(pdf_files)

            if total_files == 0:
                st.error("No PDF files found in the folder.")
            else:
                progress = st.progress(0)
                status = st.empty()

                # --- Search PDFs ---
                with st.spinner("🔍 Searching all PDF files..."):
                    for i, filename in enumerate(pdf_files, start=1):
                        file_path = os.path.join(pdf_folder, filename)
                        status.text(f"Processing: {filename} ({i}/{total_files})")

                        try:
                            with pdfplumber.open(file_path) as pdf:
                                for page_num, page in enumerate(pdf.pages, start=1):
                                    text = page.extract_text()
                                    if not text:
                                        continue
                                    lines = text.split('\n')
                                    for line_num, line in enumerate(lines, start=1):
                                        if search_text.lower() in line.lower():
                                            results.append({
                                                "File Name": filename,
                                                "Page": page_num,
                                                "Line": line.strip()
                                            })
                        except Exception as e:
                            st.error(f"Error reading {filename}: {e}")

                        progress.progress(i / total_files)
                        time.sleep(0.1)

                # --- Display Results ---
                st.markdown("---")
                if results:
                    df = pd.DataFrame(results)
                    st.success(f"✅ Found **{len(results)}** matches for '{search_text}' in **{total_files}** PDFs.")

                    # Show dataframe with styling
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Optional: allow download
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "⬇️ Download Results as CSV",
                        data=csv,
                        file_name="search_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.info(f"No matches found for '{search_text}'.")

                st.markdown("<div class='footer'> Develop By Vepari Safin </div>", unsafe_allow_html=True)
