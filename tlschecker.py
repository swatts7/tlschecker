import streamlit as st
import requests
import pandas as pd
from io import StringIO

# Function to get TLS version
def get_tls_version(url, headers):
    try:
        with requests.get(url, headers=headers, stream=True) as response:
            st.write(f"Connected to {url}")

            if hasattr(response.raw, 'connection') and hasattr(response.raw.connection, 'sock') and hasattr(response.raw.connection.sock, 'version'):
                tls_version = response.raw.connection.sock.version()
                st.write(f"TLS version for {url}: {tls_version}")
                return tls_version
            else:
                st.write(f"TLS version info not available for {url}")
                return "TLS version info not available"
    except requests.RequestException as e:
        st.write(f"Error connecting to {url}: {e}")
        return f"Error: {e}"

# Function to check TLS versions for a list of URLs and return a DataFrame
def check_tls_versions(urls):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for url in urls:
        version = get_tls_version(url, headers)
        results.append({"URL": url, "TLS Version": version})

    return pd.DataFrame(results)

# Streamlit interface
st.title("TLS Version Checker")

# Text area for URL input
url_input = st.text_area("Enter URLs (one per line)")

# Button to check TLS versions
if st.button("Check TLS Versions"):
    urls = url_input.split("\n")  # Split input into a list of URLs
    if urls:
        df_results = check_tls_versions(urls)
        st.write(df_results)

        # CSV Download
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='tls_versions.csv',
            mime='text/csv',
        )
    else:
        st.error("Please enter at least one URL.")
