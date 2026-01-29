import requests
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

# =============================
# CONFIG
# =============================
# Choose ONE backend
API_BASE = "http://127.0.0.1:8000"
API_BASE = "https://movie-rec-backend-l9q9.onrender.com"

TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# =============================
# STYLES
# =============================
st.markdown(
    """
<style>
.block-container { padding-top: 1rem; max-width: 1400px; }
.small-muted { color:#6b7280; font-size: 0.9rem; }
.movie-title { font-size: 0.9rem; line-height: 1.2rem; height: 2.4rem; overflow: hidden; }
.card { border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; padding: 12px; background: white; }
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# SESSION STATE
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")

if qp_view in ("home", "details"):
    st.session_state.view = qp_view

if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params.clear()
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = tmdb_id
    st.query_params["view"] = "details"
    st.query_params["id"] = str(tmdb_id)
    st.rerun()


# =============================
# API HELPER
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=20)
        if r.status_code >= 400:
            return None
        return r.json()
    except:
        return None


# =============================
# GRID UI
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        return

    colset = st.columns(cols)
    for i, m in enumerate(cards):
        with colset[i % cols]:
            if m.get("poster_url"):
                st.image(m["poster_url"], width=180)
            else:
                st.empty()

            if st.button("Open", key=f"{key_prefix}_{i}_{m.get('tmdb_id')}"):
                goto_details(m["tmdb_id"])

            st.markdown(
                f"<div class='movie-title'>{m.get('title','')}</div>",
                unsafe_allow_html=True
            )


# =============================
# DATA HELPERS
# =============================
def to_cards_from_tfidf_items(items):
    cards = []
    for x in items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title"),
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# 🔥 FIXED SEARCH PARSER (NO OVER-FILTERING)
def parse_tmdb_search_to_cards(data, limit: int = 24):
    if not data:
        return [], []

    raw_items = []

    # TMDB raw response
    if isinstance(data, dict) and "results" in data:
        for m in data["results"]:
            if m.get("id") and m.get("title"):
                raw_items.append(
                    {
                        "tmdb_id": int(m["id"]),
                        "title": m["title"],
                        "poster_url": f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None,
                        "release_date": m.get("release_date", ""),
                    }
                )

    # Backend formatted list
    elif isinstance(data, list):
        for m in data:
            if m.get("tmdb_id") and m.get("title"):
                raw_items.append(m)

    if not raw_items:
        return [], []

    # Suggestions
    suggestions = []
    for x in raw_items[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = raw_items[:limit]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("## 🎬 Menu")

    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")

    home_category = st.selectbox(
        "Home Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
    )

    grid_cols = st.slider("Grid Columns", 4, 8, 6)


# =============================
# HEADER
# =============================
st.title("🎬 Movie Recommender")
st.markdown(
    "<div class='small-muted'>Search → select → view details → get recommendations</div>",
    unsafe_allow_html=True
)
st.divider()

# =============================
# HOME VIEW
# =============================
if st.session_state.view == "home":
    query = st.text_input("Search movie", placeholder="anaconda, batman, avatar...")

    if query.strip():
        data = api_get_json("/tmdb/search", params={"query": query.strip()})
        suggestions, cards = parse_tmdb_search_to_cards(data)

        if suggestions:
            labels = ["-- Select --"] + [s[0] for s in suggestions]
            selected = st.selectbox("Suggestions", labels)

            if selected != "-- Select --":
                label_to_id = {s[0]: s[1] for s in suggestions}
                goto_details(label_to_id[selected])

        st.markdown("### Results")

        if cards:
            poster_grid(cards, cols=grid_cols, key_prefix="search")
        else:
            st.info("No results found. Try another keyword.")

    else:
        st.markdown(f"### 🏠 {home_category.replace('_',' ').title()}")

        home_cards = api_get_json("/home", params={"category": home_category, "limit": 24})
        poster_grid(home_cards or [], cols=grid_cols, key_prefix="home")


# =============================
# DETAILS VIEW
# =============================
if st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected")
        st.stop()

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("← Back"):
            goto_home()

    data = api_get_json(f"/movie/id/{tmdb_id}")
    if not data:
        st.error("Failed to load movie details")
        st.stop()

    left, right = st.columns([1, 2.5], gap="large")

    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], width=280)

    with right:
        st.markdown(f"## {data.get('title')}")
        st.markdown(
            f"<div class='small-muted'>Release: {data.get('release_date','-')}</div>",
            unsafe_allow_html=True
        )
        st.markdown("### Overview")
        st.write(data.get("overview") or "No overview available.")

    st.divider()
    st.markdown("### 🎯 Recommendations")

    title = data.get("title")
    if title:
        bundle = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if bundle:
            st.markdown("#### 🔎 Similar Movies")
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="tfidf",
            )

            st.markdown("#### 🎭 Genre Based")
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="genre",
            )
