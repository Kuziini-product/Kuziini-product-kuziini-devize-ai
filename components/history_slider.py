import streamlit as st
import json
import os

def afiseaza_istoric():
    st.markdown("## 📁 Istoric oferte")
    
    if not os.path.exists("history"):
        st.info("Nu există oferte salvate.")
        return

    files = sorted(os.listdir("history"), reverse=True)
    for f in files:
        if f.endswith(".json"):
            with open(os.path.join("history", f), encoding="utf-8") as fi:
                data = json.load(fi)
                with st.expander(f"📄 {data['numar']} – {data['client']} ({data['valoare']} RON)"):
                    st.write(f"📞 {data.get('telefon', '-')}")
                    st.write(f"📐 Dimensiuni: {data.get('dimensiuni', '-')}")
                    st.write(f"📦 Tip dulap: {data.get('tip', '-')}")
                    st.write(f"📝 Descriere: {data.get('prompt', '-')}")
