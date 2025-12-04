import streamlit as st
from src.predict import predict

# try to import enhanced pipeline
try:
    from inference import analyze_text, analyze_url
    ENHANCED_AVAILABLE = True
except Exception:
    ENHANCED_AVAILABLE = False

st.set_page_config(page_title='Rumour Detection', layout='centered', page_icon='🕵️‍♀️')
st.title('Rumour Detection • Fact-check Assistant')
st.write('Enter text or a news article URL. The app combines a model prediction with Fact Check Tools evidence.')

# sidebar controls
mode = st.sidebar.selectbox('Mode', ['Baseline (fast)', 'Enhanced (fact-check + claims)'])
input_type = st.sidebar.radio('Input type', ['Text', 'URL'])
show_raw = st.sidebar.checkbox('Show raw fact-check JSON', False)

def strongest_factcheck_entry(factchecks):
    # factchecks is a list of claim objects from Fact Check API
    # prefer those with claimReview present
    best = None
    for c in factchecks:
        if c.get('claimReview'):
            return c  # return the first with a review
        if not best:
            best = c
    return best

def render_strong_card(claim_obj):
    st.markdown('### 🔎 Top fact-check match')
    st.write('**Claim text:**', claim_obj.get('text') or claim_obj.get('claim') or '—')
    crs = claim_obj.get('claimReview') or []
    if crs:
        cr = crs[0]
        pub = cr.get('publisher', {}).get('name','—')
        title = cr.get('title') or cr.get('text') or '—'
        verdict = cr.get('textualRating') or '—'
        url = cr.get('url')
        st.write(f"**Publisher:** {pub}  •  **Verdict:** {verdict}")
        st.write(f"**Title:** {title}")
        if url:
            st.markdown(f"[Read review]({url})")
    else:
        st.info('No formal claim review found — showing claim text only.')

def render_all_matches(matches):
    if not matches:
        st.info('No fact-check matches (or API/resources not available).')
        return
    st.markdown('---')
    st.markdown('### All matched items')
    for i, m in enumerate(matches, 1):
        st.markdown(f'**Match {i} — claim:** {m.get("claim")}')
        st.write('Evidence score:', m.get('evidence_score', 0))
        if m.get('factchecks'):
            for idx, fc in enumerate(m.get('factchecks', []), 1):
                st.write(f"- Factcheck {idx}: {fc.get('claimant') or fc.get('text','(no claimant)')}")
        if show_raw:
            st.json(m)

def show_result_panel(res):
    st.subheader('Summary')
    st.metric('Verdict', res.get('verdict'))
    st.write('Model prediction:', res.get('model_pred'), '• Confidence:', res.get('confidence'))

    matches = res.get('factcheck_matches', [])
    if matches:
        # show strongest claim card (first match's first claim)
        top = matches[0]
        # top may include a actchecks field containing full claim objects
        factchecks = top.get('factchecks') or []
        if factchecks:
            strongest = strongest_factcheck_entry(factchecks)
            if strongest:
                render_strong_card(strongest)
        render_all_matches(matches)
    else:
        st.info('No fact-check evidence found.')

# UI: Text input flow
if input_type == 'Text':
    user_text = st.text_area('Enter text to analyze', height=220)
    if st.button('Analyze'):
        if not user_text.strip():
            st.warning('Please enter some text to analyze.')
        else:
            # Baseline
            try:
                baseline = predict(user_text)
            except Exception as e:
                baseline = f'Error in baseline predict(): {e}'
            st.subheader('Baseline prediction')
            st.write(baseline)

            # Enhanced analysis
            if mode.startswith('Enhanced'):
                if ENHANCED_AVAILABLE:
                    try:
                        res = analyze_text(user_text)
                        show_result_panel(res)
                    except Exception as e:
                        st.error('Enhanced analysis failed: ' + str(e))
                else:
                    st.info('Enhanced pipeline not available on this machine. Using baseline only.')
# UI: URL input flow
else:
    url = st.text_input('Enter article URL (include http/https)')
    if st.button('Analyze URL'):
        if not url.strip():
            st.warning('Please enter a URL.')
        else:
            if ENHANCED_AVAILABLE:
                try:
                    res = analyze_url(url)
                    show_result_panel(res)
                except Exception as e:
                    st.error('Error analyzing URL: ' + str(e))
            else:
                st.info('Enhanced URL analysis not available locally.')
                st.subheader('Baseline on URL string')
                st.write(predict(url))
