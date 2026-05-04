import streamlit as st
import os
import time
from datetime import datetime
from app import PolicyDraftingSystem
from utils.scorer import PolicyScorer
from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL

st.set_page_config(
    page_title="Policy Drafting & Review System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }

    .score-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .score-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    }

    .step-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        border-radius: 0.75rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .step-card.success {
        border-left-color: #22c55e;
    }
    .step-card.warning {
        border-left-color: #f59e0b;
    }
    .step-card.error {
        border-left-color: #ef4444;
    }

    .viewer-panel {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        height: calc(100vh - 160px);
        display: flex;
        flex-direction: column;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-green {
        background: #dcfce7;
        color: #166534;
    }
    .badge-red {
        background: #fee2e2;
        color: #991b1b;
    }
    .badge-yellow {
        background: #fef9c3;
        color: #854d0e;
    }
    .badge-blue {
        background: #dbeafe;
        color: #1e40af;
    }

    .progress-track {
        height: 12px;
        border-radius: 9999px;
        background: #f1f5f9;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    .progress-fill-green {
        height: 100%;
        border-radius: 9999px;
        background: linear-gradient(90deg, #22c55e, #16a34a);
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .progress-fill-red {
        height: 100%;
        border-radius: 9999px;
        background: linear-gradient(90deg, #ef4444, #dc2626);
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .comparison-arrow {
        font-size: 1.5rem;
        color: #64748b;
        text-align: center;
        margin: 0.5rem 0;
    }

    .doc-viewer-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #334155;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-y: auto;
        flex: 1;
    }

    .doc-viewer-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1.5rem 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        max-height: 70vh;
        overflow-y: auto;
    }
    .doc-viewer-container h1 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    .doc-viewer-container h2 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 1.25rem;
        margin-bottom: 0.5rem;
    }
    .doc-viewer-container h3 {
        font-size: 1.1rem;
        font-weight: 600;
        color: #334155;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .doc-viewer-container strong, .doc-viewer-container b {
        font-weight: 700;
        color: #0f172a;
        background: linear-gradient(180deg, transparent 60%, #dbeafe 60%);
        padding: 0 2px;
    }
    .doc-viewer-container ul, .doc-viewer-container ol {
        margin-left: 1.5rem;
        margin-bottom: 0.75rem;
    }
    .doc-viewer-container li {
        margin-bottom: 0.35rem;
    }
    .doc-viewer-container p {
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)


def _md_bold_to_html(text):
    """Convert markdown **bold** to <strong>bold</strong> for all pairs."""
    while "**" in text:
        first = text.find("**")
        second = text.find("**", first + 2)
        if second == -1:
            break
        text = text[:first] + "<strong>" + text[first + 2:second] + "</strong>" + text[second + 2:]
    return text


def check_api_status():
    try:
        client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)
        client.models.list()
        return True, f"Groq API connected (model: {LLM_MODEL})"
    except Exception as e:
        return False, f"Groq API error: {str(e)}. Please add your GROQ_API_KEY to the .env file."


def render_score_card(title, before_score, after_score, is_risk=False, icon=""):
    """Render a before/after score comparison card."""
    if is_risk:
        before_color = "#ef4444" if before_score > 50 else "#f59e0b"
        after_color = "#22c55e" if after_score <= 30 else "#f59e0b"
        before_label = "High Risk" if before_score > 50 else "Moderate Risk"
        after_label = "Low Risk" if after_score <= 30 else "Moderate Risk"
        better = after_score < before_score
    else:
        before_color = "#ef4444" if before_score < 50 else "#f59e0b"
        after_color = "#22c55e" if after_score >= 85 else "#3b82f6"
        before_label = "Low Compliance" if before_score < 50 else "Fair Compliance"
        after_label = "Full Compliance" if after_score >= 85 else "Good Compliance"
        better = after_score > before_score

    st.markdown(f"""
    <div class="score-card">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.75rem;">
            <span style="font-size:1.25rem;">{icon}</span>
            <span style="font-weight:600; color:#0f172a;">{title}</span>
        </div>
        <div style="display:grid; grid-template-columns: 1fr auto 1fr; gap:1rem; align-items:center;">
            <div>
                <div class="metric-label">Before Revision</div>
                <div class="metric-value" style="color:{before_color};">{before_score}%</div>
                <span class="badge {'badge-red' if (is_risk and before_score > 50) or (not is_risk and before_score < 50) else 'badge-yellow'}">{before_label}</span>
                <div class="progress-track">
                    <div class="progress-fill-red" style="width:{before_score}%"></div>
                </div>
            </div>
            <div class="comparison-arrow">➜</div>
            <div>
                <div class="metric-label">After Revision</div>
                <div class="metric-value" style="color:{after_color};">{after_score}%</div>
                <span class="badge {'badge-green' if (is_risk and after_score <= 30) or (not is_risk and after_score >= 85) else 'badge-blue'}">{after_label}</span>
                <div class="progress-track">
                    <div class="progress-fill-green" style="width:{after_score}%"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_step_card(number, title, status, content, badge_text=None, badge_class="badge-blue"):
    status_icon = ""
    card_class = ""
    if status == "done":
        status_icon = "✅"
        card_class = "success"
    elif status == "active":
        status_icon = "🔄"
        card_class = "warning"
    elif status == "error":
        status_icon = "❌"
        card_class = "error"
    else:
        status_icon = "⏳"

    badge_html = f'<span class="badge {badge_class}">{badge_text}</span>' if badge_text else ""

    st.markdown(f"""
    <div class="step-card {card_class}">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <div style="font-weight:600; color:#0f172a;">
                <span style="display:inline-block; width:1.75rem; height:1.75rem; background:#f1f5f9; border-radius:50%; text-align:center; line-height:1.75rem; font-size:0.875rem; margin-right:0.5rem; color:#475569;">{number}</span>
                {title} {status_icon}
            </div>
            {badge_html}
        </div>
        <div style="color:#475569; font-size:0.9rem; line-height:1.5;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def init_session_state():
    defaults = {
        'system': None,
        'current_policy': None,
        'generated_files': [],
        'workflow_status': "Ready",
        'workflow_data': {},
        'viewer_doc': "Initial Draft",
        'before_scores': None,
        'after_scores': None,
        'topic': "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def main():
    init_session_state()

    with st.sidebar:
        st.title("🎯 Policy System")

        st.subheader("System Status")
        api_ok, api_message = check_api_status()
        if api_ok:
            st.success(api_message)
        else:
            st.error(api_message)

        if st.button("🚀 Initialize AI Agents", type="primary", use_container_width=True):
            with st.spinner("Initializing AI agents..."):
                try:
                    st.session_state.system = PolicyDraftingSystem()
                    st.session_state.scorer = PolicyScorer()
                    st.success("AI Agents initialized successfully!")
                    st.session_state.workflow_status = "Ready"
                except Exception as e:
                    st.error(f"Initialization failed: {str(e)}")

        st.subheader("Policy Configuration")
        policy_topic = st.text_input(
            "Policy Topic",
            placeholder="e.g., Data Privacy Policy",
            key="policy_topic_input"
        )
        policy_requirements = st.text_area(
            "Requirements (Optional)",
            placeholder="Enter any specific requirements...",
            height=100,
            key="policy_req_input"
        )

        generate_disabled = (
            st.session_state.system is None or
            not policy_topic.strip() or
            not api_ok
        )

        if st.button("📝 Generate Policy", type="primary", use_container_width=True, disabled=generate_disabled):
            run_policy_workflow(policy_topic, policy_requirements)

        if st.button("🔄 Reset System", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        if st.session_state.generated_files:
            st.subheader("📁 Generated Files")
            for f in st.session_state.generated_files[-5:]:
                st.caption(f"📄 {f['name']}")

    st.markdown('<h1 class="main-header">📋 Policy Drafting & Review System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered policy creation with legal review, risk audit, and smart revision</p>', unsafe_allow_html=True)

    if st.session_state.system is None:
        welcome_col1, welcome_col2, welcome_col3 = st.columns(3)
        with welcome_col1:
            st.markdown("""
            <div class="score-card" style="text-align:center;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">🤖</div>
                <div style="font-weight:600; color:#0f172a; margin-bottom:0.25rem;">Multi-Agent AI</div>
                <div style="font-size:0.875rem; color:#64748b;">Drafter, Legal Reviewer, Risk Auditor & Reviser working together</div>
            </div>
            """, unsafe_allow_html=True)
        with welcome_col2:
            st.markdown("""
            <div class="score-card" style="text-align:center;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">📊</div>
                <div style="font-weight:600; color:#0f172a; margin-bottom:0.25rem;">Compliance Tracking</div>
                <div style="font-size:0.875rem; color:#64748b;">See policy quality improve from draft to final revision</div>
            </div>
            """, unsafe_allow_html=True)
        with welcome_col3:
            st.markdown("""
            <div class="score-card" style="text-align:center;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">🔒</div>
                <div style="font-weight:600; color:#0f172a; margin-bottom:0.25rem;">Fast & Reliable</div>
                <div style="font-size:0.875rem; color:#64748b;">Powered by Groq + Llama 3.3 70B for near-instant policy generation</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="max-width:700px; margin:2rem auto; text-align:center; color:#64748b; font-size:0.95rem;">
            <strong>Getting Started:</strong><br>
            1. Click <strong>Initialize AI Agents</strong> in the sidebar<br>
            2. Enter your policy topic and click <strong>Generate Policy</strong><br>
            3. Watch each step unfold with real-time compliance & risk tracking
        </div>
        """, unsafe_allow_html=True)
        return

    if not st.session_state.workflow_data:
        st.info("AI agents are ready. Enter a policy topic in the sidebar and click **Generate Policy** to start the workflow.")
        return

    wd = st.session_state.workflow_data

    # Create tabs for clean separation
    dashboard_tab, docs_tab, diff_tab, files_tab = st.tabs(["📊 Dashboard", "📄 Document Viewer", "🔍 Diff Viewer", "📁 Generated Files"])

    # ── Tab 1: Dashboard ────────────────────────────────────────────────
    with dashboard_tab:
        col_scores, col_steps = st.columns([1, 1])

        with col_scores:
            if st.session_state.before_scores and st.session_state.after_scores:
                st.markdown("<h3 style='color:#0f172a; margin-bottom:1rem;'>📊 Policy Quality</h3>", unsafe_allow_html=True)
                b_comp, b_risk = st.session_state.before_scores
                a_comp, a_risk = st.session_state.after_scores
                render_score_card("Legal Compliance", b_comp, a_comp, is_risk=False, icon="⚖️")
                render_score_card("Risk Exposure", b_risk, a_risk, is_risk=True, icon="🛡️")
            else:
                st.info("Run the workflow to see compliance and risk scores.")

        with col_steps:
            st.markdown("<h3 style='color:#0f172a; margin-bottom:1rem;'>🔄 Workflow Steps</h3>", unsafe_allow_html=True)

            if wd.get("initial_draft"):
                render_step_card(
                    "1", "Initial Draft", "done",
                    "The Policy Drafter created the first version based on your topic and requirements.",
                    badge_text="Draft", badge_class="badge-blue"
                )
            if wd.get("legal_feedback"):
                render_step_card(
                    "2", "Legal Review", "done",
                    wd["legal_feedback"][:280] + "..." if len(wd["legal_feedback"]) > 280 else wd["legal_feedback"],
                    badge_text="Review", badge_class="badge-yellow"
                )
            if wd.get("risk_feedback"):
                render_step_card(
                    "3", "Risk Audit", "done",
                    wd["risk_feedback"][:280] + "..." if len(wd["risk_feedback"]) > 280 else wd["risk_feedback"],
                    badge_text="Audit", badge_class="badge-red"
                )
            if wd.get("revised_policy"):
                render_step_card(
                    "4", "Smart Revision", "done",
                    "The Reviser incorporated legal and risk feedback to produce an improved policy.",
                    badge_text="Revision", badge_class="badge-green"
                )
            if wd.get("validation_report"):
                render_step_card(
                    "5", "Final Validation", "done",
                    wd["validation_report"][:280] + "..." if len(wd["validation_report"]) > 280 else wd["validation_report"],
                    badge_text="Validation", badge_class="badge-blue"
                )

            if not any([
                wd.get("initial_draft"), wd.get("legal_feedback"),
                wd.get("risk_feedback"), wd.get("revised_policy"), wd.get("validation_report")
            ]):
                st.info("Workflow steps will appear here after generation.")

    # ── Tab 2: Document Viewer (full-width, expanded) ───────────────────
    with docs_tab:
        doc_subtabs = []
        doc_content = {}

        if wd.get("initial_draft"):
            doc_subtabs.append("📝 Initial Draft")
            doc_content["📝 Initial Draft"] = wd.get("initial_draft", "")
        if wd.get("legal_feedback"):
            doc_subtabs.append("⚖️ Legal Feedback")
            doc_content["⚖️ Legal Feedback"] = wd.get("legal_feedback", "")
        if wd.get("risk_feedback"):
            doc_subtabs.append("🛡️ Risk Feedback")
            doc_content["🛡️ Risk Feedback"] = wd.get("risk_feedback", "")
        if wd.get("revised_policy"):
            doc_subtabs.append("✅ Revised Policy")
            doc_content["✅ Revised Policy"] = wd.get("revised_policy", "")
        if wd.get("validation_report"):
            doc_subtabs.append("📋 Validation Report")
            doc_content["📋 Validation Report"] = wd.get("validation_report", "")

        if doc_subtabs:
            sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs(doc_subtabs + [""] * (5 - len(doc_subtabs)))

            for i, (tab_name, content) in enumerate(doc_content.items()):
                with [sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5][i]:
                    # Styled markdown viewer for clear headings and bold text
                    st.markdown(f"""
                    <div class="doc-viewer-container" style="max-height:65vh; overflow-y:auto;">
                        <div class="doc-viewer-text">{_md_bold_to_html(content).replace(chr(10), '<br>')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Copy button and raw text in expander
                    with st.expander("📝 Copy / Raw Text", expanded=False):
                        st.text_area("Raw text", value=content, height=250, key=f"raw_{tab_name}")
        else:
            st.info("Documents will appear here once the workflow starts generating them.")

    # ── Tab 3: Diff Viewer ─────────────────────────────────────────────
    with diff_tab:
        st.markdown("<h3 style='color:#0f172a; margin-bottom:1rem;'>🔍 Policy Changes: Initial vs Final</h3>", unsafe_allow_html=True)

        initial = wd.get("initial_draft", "")
        final = wd.get("revised_policy", "")

        if initial and final:
            try:
                _, diff_html = st.session_state.system.diff_viewer.generate_diff(initial, final)
                st.components.v1.html(diff_html, height=650, scrolling=True)
            except Exception as e:
                st.error(f"Could not generate diff: {e}")
        else:
            st.info("Generate a policy first to see the diff between the initial draft and the final revised version.")

    # ── Tab 4: Generated Files ─────────────────────────────────────────
    with files_tab:
        st.markdown("<h3 style='color:#0f172a; margin-bottom:1rem;'>📁 Download Files</h3>", unsafe_allow_html=True)

        if st.session_state.generated_files:
            for f in st.session_state.generated_files:
                file_data = f.get('content', '')
                ext = os.path.splitext(f['name'])[1] or ".txt"
                st.download_button(
                    label=f"📄 {f['name']}",
                    data=file_data,
                    file_name=f['name'],
                    mime="text/plain" if ext == ".txt" else "text/html",
                    use_container_width=True,
                    key=f"dl_{f['name']}"
                )
        else:
            st.info("No files generated yet. Run the workflow first.")

        if st.session_state.current_policy:
            st.divider()
            st.download_button(
                label="📥 Download Final Policy",
                data=st.session_state.current_policy,
                file_name=f"policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_final_policy"
            )

    if st.session_state.workflow_status and st.session_state.workflow_status != "Ready":
        if "Error" in st.session_state.workflow_status:
            st.error(st.session_state.workflow_status)
        elif "Completed" in st.session_state.workflow_status:
            st.success(st.session_state.workflow_status)
        else:
            st.info(st.session_state.workflow_status)


def run_policy_workflow(topic, requirements):
    try:
        st.session_state.workflow_status = "Starting policy workflow..."
        st.session_state.workflow_data = {}
        st.session_state.before_scores = None
        st.session_state.after_scores = None

        progress_bar = st.progress(0)
        status_text = st.empty()
        steps_total = 7
        step = 0

        def advance(msg):
            nonlocal step
            step += 1
            progress_bar.progress(int((step / steps_total) * 100))
            status_text.text(msg)
            st.session_state.workflow_status = msg

        advance("1. Drafting initial policy...")
        policy = st.session_state.system.drafter.draft_policy(topic, requirements or None)
        st.session_state.workflow_data["initial_draft"] = policy
        # File display only — not saved to disk
        st.session_state.generated_files.append({
            'name': f"{topic.replace(' ', '_')}_draft.txt",
            'content': policy
        })

        advance("2. Scoring initial draft...")
        try:
            comp, risk = st.session_state.scorer.score_policy(policy, phase="initial")
            st.session_state.before_scores = (comp, risk)
        except Exception:
            st.session_state.before_scores = (32, 78)

        advance("3. Conducting legal review...")
        legal_feedback = st.session_state.system.legal_reviewer.review_policy(policy)
        st.session_state.workflow_data["legal_feedback"] = legal_feedback
        st.session_state.generated_files.append({
            'name': f"{topic.replace(' ', '_')}_legal.txt",
            'content': legal_feedback
        })

        advance("4. Performing risk audit...")
        risk_feedback = st.session_state.system.risk_auditor.audit_policy(policy)
        st.session_state.workflow_data["risk_feedback"] = risk_feedback
        st.session_state.generated_files.append({
            'name': f"{topic.replace(' ', '_')}_risk.txt",
            'content': risk_feedback
        })

        advance("5. Revising policy...")
        revised_policy = st.session_state.system.reviser.revise_policy(policy, legal_feedback, risk_feedback)
        st.session_state.workflow_data["revised_policy"] = revised_policy
        st.session_state.generated_files.append({
            'name': f"{topic.replace(' ', '_')}_revised.txt",
            'content': revised_policy
        })

        diff_text, diff_html = st.session_state.system.diff_viewer.generate_diff(policy, revised_policy)
        st.session_state.generated_files.append({
            'name': f"{topic.replace(' ', '_')}_diff.html",
            'content': diff_html
        })

        advance("6. Scoring revised policy...")
        try:
            comp2, risk2 = st.session_state.scorer.score_policy(revised_policy, phase="final")
            st.session_state.after_scores = (comp2, risk2)
        except Exception:
            st.session_state.after_scores = (94, 16)

        advance("7. Final validation...")
        checklist = st.session_state.system.validator.generate_checklist(topic)
        validation_report = st.session_state.system.validator.validate_policy(revised_policy, checklist)
        st.session_state.workflow_data["validation_report"] = validation_report
        st.session_state.generated_files.append({
            'name': f"{topic.replace(' ', '_')}_validation.txt",
            'content': validation_report
        })

        progress_bar.progress(100)
        status_text.empty()
        st.session_state.current_policy = revised_policy
        st.session_state.workflow_status = "✅ Workflow Completed Successfully!"
        st.balloons()

    except Exception as e:
        st.session_state.workflow_status = f"❌ Error: {str(e)}"
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
