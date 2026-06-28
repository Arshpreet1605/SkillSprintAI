"""
app/ui/components/sidebar.py
----------------------------
Sidebar navigation component.
Returns the currently selected navigation item as a string.
"""

import streamlit as st
from app.config.settings import APP_NAME, APP_ICON, NAV_ITEMS


def render_sidebar() -> str:
    """
    Renders the left navigation sidebar.

    Returns
    -------
    str
        The navigation label the user has selected (e.g. '🏠  Home').
    """
    with st.sidebar:
        # ── Logo / Brand ────────────────────────────────────────────────
        st.markdown(
            f"""
            <div style="text-align:center; padding: 1.5rem 0 1rem 0;">
                <div style="font-size:2.4rem;">{APP_ICON}</div>
                <div style="
                    font-size:1.15rem;
                    font-weight:700;
                    color:#F0F4FF;
                    letter-spacing:-0.3px;
                    margin-top:0.35rem;">
                    {APP_NAME}
                </div>
                <div style="
                    font-size:0.7rem;
                    color:#9EB3D8;
                    margin-top:0.2rem;
                    letter-spacing:0.5px;
                    text-transform:uppercase;">
                    Sprint 1 · v0.1
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<hr style='border-color:rgba(255,255,255,0.08);margin:0 0 1rem 0;'>",
            unsafe_allow_html=True,
        )

        # ── Navigation ──────────────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.72rem;color:#9EB3D8;"
            "text-transform:uppercase;letter-spacing:1px;"
            "font-weight:600;margin-bottom:0.5rem;'>Navigation</p>",
            unsafe_allow_html=True,
        )

        # Use session_state to track active page
        if "nav_selection" not in st.session_state:
            st.session_state["nav_selection"] = NAV_ITEMS[0]

        for item in NAV_ITEMS:
            is_active = st.session_state["nav_selection"] == item
            btn_style = (
                "background:rgba(21,101,192,0.30);color:#fff;"
                if is_active
                else "background:transparent;color:#9EB3D8;"
            )
            if st.button(
                item,
                key=f"nav_{item}",
                use_container_width=True,
            ):
                st.session_state["nav_selection"] = item
                st.rerun()

        # ── Footer ──────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="
                position:fixed;
                bottom:1.5rem;
                font-size:0.72rem;
                color:#4A6080;
                text-align:center;
                width:200px;">
                © 2026 SkillSprint AI<br>
                Built with ❤️ &amp; Streamlit
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state["nav_selection"]
