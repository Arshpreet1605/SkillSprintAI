"""
app/ui/pages/contact.py
------------------------
Contact page — project links and team info.
No form backend in Sprint 1 (placeholder UI only).
"""

import streamlit as st


def render_contact_page() -> None:
    """Renders the Contact page content."""

    # ── Page header ──────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="margin-bottom:2rem;">
            <h2 style="font-size:2rem;font-weight:800;color:#F0F4FF;
                       margin-bottom:0.4rem;">Get in Touch</h2>
            <p style="color:#9EB3D8;font-size:1rem;">
                Have feedback, ideas, or found a bug? We'd love to hear from you.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Contact cards ─────────────────────────────────────────────────────
    links = [
        ("🐙", "GitHub Repository",
         "Star, fork, and contribute to SkillSprint AI.",
         "https://github.com/your-org/skillsprint-ai"),
        ("🐦", "Twitter / X",
         "Follow us for updates and announcements.",
         "https://twitter.com/skillsprintai"),
        ("💼", "LinkedIn",
         "Connect with the team on LinkedIn.",
         "https://linkedin.com/company/skillsprintai"),
        ("📧", "Email",
         "Drop us a line at hello@skillsprint.ai.",
         "mailto:hello@skillsprint.ai"),
    ]

    col1, col2 = st.columns(2, gap="medium")
    for idx, (icon, title, desc, url) in enumerate(links):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.markdown(
                f"""
                <a href="{url}" target="_blank" style="text-decoration:none;">
                    <div class="section-card" style="cursor:pointer;min-height:110px;">
                        <div style="font-size:1.8rem;margin-bottom:0.5rem;">{icon}</div>
                        <div style="font-weight:700;color:#F0F4FF;
                                    margin-bottom:0.25rem;">{title}</div>
                        <div style="font-size:0.85rem;color:#9EB3D8;
                                    line-height:1.5;">{desc}</div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True,
            )

    # ── Feedback form placeholder ─────────────────────────────────────────
    st.markdown(
        """
        <div class="section-card" style="margin-top:1rem;">
            <div class="card-title">✉️ Send a Message</div>
            <p style="color:#9EB3D8;font-size:0.9rem;margin-bottom:0;">
                A contact form will be available in a future sprint.
                For now, please reach us via email or GitHub Issues.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
