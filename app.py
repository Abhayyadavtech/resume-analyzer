import streamlit as st
from parser import extract_text_from_pdf
from processor import clean_text
from analyzer import load_skills, analyze

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI-Based Resume Analyzer")
st.caption("Text comparison using NLP and Machine Learning (TF-IDF & Cosine Similarity)")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=200)

if st.button("Analyze Resume"):
    if resume_file is None:
        st.error("Please upload a PDF resume first.")
    elif not jd_text.strip():
        st.error("The job description is empty. Please enter the job description text.")
    else:
        try:
            raw_resume = extract_text_from_pdf(resume_file)
            resume_clean = clean_text(raw_resume)
            jd_clean = clean_text(jd_text)
            result = analyze(resume_clean, jd_clean, load_skills())

            st.subheader("Analysis Result")
            st.metric("Text Similarity", f"{result['similarity']} %")
            st.progress(min(int(result["similarity"]), 100))

            c1, c2 = st.columns(2)
            with c1:
                st.success("✅ Matched Skills")
                st.write(", ".join(result["matched"]) or "None")
            with c2:
                st.warning("❌ Skills Not Found in Resume")
                st.write(", ".join(result["missing"]) or "None")

            with st.expander("All Skills Detected in Resume"):
                st.write(", ".join(result["resume_skills"]) or "None")

            st.info(
                "Note: This is a text similarity indicator only. "
                "It is not a hiring score or a measure of a candidate's ability."
            )
        except ValueError as e:
            st.error(str(e))
        except Exception:
            st.error("An unexpected error occurred. Please try again.")