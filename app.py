import streamlit as st
from src.predict import predict

# try to import enhanced pipeline
try:
    from inference import analyze_text, analyze_url
    ENHANCED_AVAILABLE = True
except Exception:
    ENHANCED_AVAILABLE = False

st.set_page_config(page_title='Rumour Detection App', layout='centered')
st.title('Rumour Detection App')
st.write('Enter text or URL. Choose mode (Baseline/Enhanced) and click Predict/Analyze.')

mode = st.sidebar.selectbox('Mode', ['Baseline (fast)', 'Enhanced (fact-check + claims)'])
input_type = st.sidebar.radio('Input type', ['Text', 'URL'])

def render_factcheck_card(fc):
    st.markdown('### Fact-check evidence')
    st.markdown(f"**Claim:** {fc.get('claim')}")
    st.metric("Evidence score", fc.get('evidence_score', 0))
    fcs = fc.get('factchecks') or []
    for r in fcs:
        cr = r.get('claimReview')
        if cr and isinstance(cr, list) and len(cr) > 0:
            item = cr[0]
            pub = item.get('publisher', {}).get('name', '—')
            title = item.get('title') or item.get('text') or '—'
            url = item.get('url')
            verdict = item.get('textualRating') or ''
            st.write(f"**Publisher:** {pub}  ")
            if verdict:
                st.write(f"**Verdict:** {verdict}  ")
            st.write(f"**Title:** {title}")
            if url:
                st.write(f"[Read review]({url})")
            st.markdown('---')
        else:
            st.write("Claim text:", r.get('text') or r.get('claim') or '—')
            st.markdown('---')

if input_type == 'Text':
    user_text = st.text_area('Enter text to analyze', height=220)
    if st.button('Predict / Analyze'):
        if not user_text or user_text.strip() == '':
            st.warning('Please enter some text first.')
        else:
            # Baseline prediction
            try:
                baseline_pred = predict(user_text)
            except Exception as e:
                baseline_pred = f'Error running baseline predict(): {e}'
            st.subheader('Baseline prediction')
            st.write(baseline_pred)

            # Enhanced analysis
            if mode.startswith('Enhanced'):
                if ENHANCED_AVAILABLE:
                    try:
                        res = analyze_text(user_text)
                        st.subheader('Enhanced analysis (claims + fact-checks + model)')
                        st.write('Verdict:', res.get('verdict'))
                        st.write('Model prediction:', res.get('model_pred'))
                        st.write('Confidence:', res.get('confidence'))
                        hits = res.get('factcheck_matches', [])
                        if hits:
                            for i, h in enumerate(hits, 1):
                                st.markdown(f'### Claim {i}')
                                render_factcheck_card(h)
                                if st.checkbox(f"Show raw JSON for claim {i}"):
                                    st.json(h)
                        else:
                            st.info('No fact-check evidence found (or Fact Check API not available).')
                    except Exception as e:
                        st.error('Enhanced analysis failed: ' + str(e))
                        st.write('Make sure inference.py, services/ and supporting files are added.')
                else:
                    st.info('Enhanced mode not available — required modules not found. Using baseline only.')
else:
    url = st.text_input('Enter article URL (include http/https)')
    if st.button('Predict / Analyze URL'):
        if not url or url.strip() == '':
            st.warning('Please enter a URL first.')
        else:
            if ENHANCED_AVAILABLE:
                try:
                    res = analyze_url(url)
                    st.subheader('Enhanced analysis (URL)')
                    st.write('Verdict:', res.get('verdict'))
                    st.write('Model prediction:', res.get('model_pred'))
                    st.write('Confidence:', res.get('confidence'))
                    hits = res.get('factcheck_matches', [])
                    if hits:
                        for i, h in enumerate(hits, 1):
                            st.markdown(f'### Claim {i}')
                            render_factcheck_card(h)
                            if st.checkbox(f"Show raw JSON for claim {i}"):
                                st.json(h)
                    else:
                        st.info('No fact-check matches found (or Fact Check API not available).')
                except Exception as e:
                    st.error('Error analyzing URL: ' + str(e))
            else:
                st.info('Enhanced URL analysis not available. To enable it, add inference.py and the services folder.')
                base_pred = predict(url)
                st.subheader('Baseline prediction on URL string')
                st.write(base_pred)
