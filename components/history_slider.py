import streamlit as st
from pathlib import Path
import json

def afiseaza_istoric():
    history_path = Path("history")
    history_path.mkdir(exist_ok=True)
    fisiere = sorted(history_path.glob("*.json"), reverse=True)

    if not fisiere:
        st.info("🛈 Nu există oferte istorice salvate.")
        return

    with st.expander("🕘 Oferte istorice (click pentru listă)"):
        selected_file = st.selectbox(
            "Selectează o ofertă salvată:",
            options=[f.name for f in fisiere],
            format_func=lambda x: x.replace(".json", "")
        )

        if selected_file:
            file_path = history_path / selected_file
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            st.markdown("---")
            st.markdown(f"### 📄 Ofertă: `{json_data.get('numar', 'N/A')}`")
            st.write(f"👤 Client: {json_data.get('client', 'N/A')}")
            st.write(f"📞 Telefon: {json_data.get('telefon', 'N/A')}")
            st.write(f"💰 Valoare totală: **{json_data.get('valoare_total', 'N/A')} RON**")

            if st.button("🔁 Regenerare această ofertă"):
                # Trimite datele înapoi în formular
                st.session_state["nume_client"] = json_data.get("client", "")
                st.session_state["telefon_client"] = json_data.get("telefon", "")
                dim = json_data.get("dimensiuni", {})
                st.session_state["înălțime"] = dim.get("înălțime", 100)
                st.session_state["lățime"] = dim.get("lățime", 100)
                st.session_state["adâncime"] = dim.get("adâncime", 100)
                st.session_state["tip_dulap"] = json_data.get("tip_dulap", "")
                st.session_state["prompt_descriere"] = json_data.get("descriere", "")
                st.success("🎯 Oferta a fost încărcată în formularul de mai sus. O poți ajusta și genera din nou.")
