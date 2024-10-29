from typing import List, Sequence, Tuple, Optional, Dict, Union, Callable
import streamlit as st
import spacy
from spacy.language import Language
from spacy import displacy
import pandas as pd
from spacy.tokens import Span
from util import load_model, get_html, \
    DEFAULT_LABEL_COLORS, TPL_SPAN, TPL_SPAN_START, TPL_SPAN_SLICE, SDDESCRIPTION

ATTRS = ["text", "label_", "start", "end", "start_char", "end_char"]
FOOTER = """<span style="font-size: 1.75em">&hearts; Built with [`spacy-streamlit`](https://github.com/explosion/spacy-streamlit)</span>"""


def visualize(
        spacy_model: str = "en_grammar_checker",
        default_text: str = "",
        ner_attrs: List[str] = ATTRS,
        show_json_doc: bool = True,
        show_meta: bool = True,
        show_config: bool = True,
        show_pipeline_info: bool = True,
        key: Optional[str] = None,
        get_default_text: Callable[[Language], str] = None,
) -> None:
    """Visualize error tags"""

    st.sidebar.title("Essay Grammar Checker Checker")
    st.sidebar.markdown(SDDESCRIPTION)
    model_load_state = st.info(f"Loading model '{spacy_model}'...")
    nlp = load_model(spacy_model)
    model_load_state.empty()
    if show_pipeline_info:
        st.sidebar.subheader("Pipeline info")
        desc = f"""<p style="font-size: 0.85em; line-height: 1.5"><strong>{spacy_model}:</strong> <code>v{nlp.meta['version']}</code></p>"""
        st.sidebar.markdown(desc, unsafe_allow_html=True)

    default_text = (
        get_default_text(nlp) if get_default_text is not None else default_text
    )
    text = st.text_area("Text to analyze", default_text, key=f"{key}_visualize_text")
    doc = nlp(text)
    visualizer = st.selectbox("Select rendering style",
                              options=["ner", "span"]
                              )
    if "ner" in visualizer:
        ner = spacy.blank("en")
        ner = ner.create_pipe("ner")
        orig_ents = list(doc.ents)
        added_ents = []
        added_labels = []
        depatched_spans = []
        [depatched_spans.extend(list(doc.spans[i])) for i in doc.spans.keys()]
        depatched_spans = sorted(depatched_spans, key=lambda s: s.start)
        start_span = 0
        for s in depatched_spans:
            if s.start >= start_span:
                start_span = s.end
                s_label = " ".join(s.label_.capitalize().split("_"))
                added_ents.append(Span(doc, s.start, s.end, label=s_label))
                added_labels.append(s_label)
                ner.add_label(s_label)

        doc.ents = orig_ents + added_ents
    st.header("Span Categories")
    if "ner" in visualizer:
        visualize_ner(doc, labels=set(added_labels), attrs=ner_attrs, key=key)
    if "span" in visualizer:
        visualize_spans(doc, attrs=ner_attrs)

    if show_json_doc or show_meta or show_config:
        st.header("Pipeline information")
        if show_json_doc:
            json_doc_exp = st.expander("JSON Doc")
            json_doc_exp.json(doc.to_json())

        if show_meta:
            meta_exp = st.expander("Pipeline meta.json")
            meta_exp.json(nlp.meta)

        if show_config:
            config_exp = st.expander("Pipeline config.cfg")
            config_exp.code(nlp.config.to_str())

    st.sidebar.markdown(
        FOOTER,
        unsafe_allow_html=True,
    )


def visualize_ner(
        doc: Union[spacy.tokens.Doc, List[Dict[str, str]]],
        *,
        labels: Sequence[str] = tuple(),
        attrs: List[str] = ATTRS,
        show_table: bool = True,
        key: Optional[str] = None,
):
    """
    Visualizer for named entities.
    doc (Doc, List): The document to visualize.
    labels (list): The entity labels to visualize.
    attrs (list):  The attributes on the entity Span to be labeled. Attributes are displayed only when the show_table
    argument is True.
    key (str): Key used for the streamlit component for selecting labels.
    """
    displacy_options = dict()
    displacy_options["colors"] = DEFAULT_LABEL_COLORS

    label_select = st.multiselect(
        "Error labels",
        options=labels,
        default=list(labels),
        key=f"{key}_ner_label_select",
    )

    displacy_options["ents"] = label_select
    html = displacy.render(
        doc,
        style="ent",
        options=displacy_options,
    )
    style = "<style>mark.entity { display: inline-block }</style>"
    st.write(f"{style}{get_html(html)}", unsafe_allow_html=True)
    if show_table:
        data = [
            [str(getattr(ent, attr)) for attr in attrs]
            for ent in doc.ents
            if ent.label_ in label_select
        ]
        if data:
            df = pd.DataFrame(data, columns=attrs)
            st.dataframe(df)


def visualize_spans(
        doc: Union[spacy.tokens.Doc, List[Dict[str, str]]],
        *,
        attrs: List[str] = ATTRS,
        show_table: bool = True,
):
    """
    Visualizer for Span Categorizer.
    doc (Doc, List): The document to visualize.
    attrs (list):  The attributes on the entity Span to be labeled. Attributes are displayed only when the show_table
    argument is True.
    """

    render_errors = ['all', 'punctuation', 'spelling', \
                     'articles', 'vocabulary', 'articles', 'grammar_major', 'grammar_minor']
    render_error = st.selectbox("Select error type",
                                options=render_errors
                                )

    if render_error == "all":
        upd_spans = []
        upd_intervals = []
        doc.spans[render_error] = []
        for sc in doc.spans.keys():
            for e in doc.spans[sc]:
                if (e.start, e.end) not in upd_intervals:
                    upd_intervals.append((e.start, e.end))
                upd_spans.append(Span(doc, e.start, e.end, " ".join(e.label_.capitalize().split("_"))))
        doc.spans[render_error] = upd_spans
    # template = {"span": TPL_SPAN, "slice": TPL_SPAN_SLICE, "start": TPL_SPAN_START}
    options = {"colors": DEFAULT_LABEL_COLORS, "spans_key": render_error}
    html = displacy.render(doc, style="span", options=options)
    style = "<style>mark.entity { display: inline-block }</style>"
    st.write(f"{style}{get_html(html)}", unsafe_allow_html=True)
    if show_table:
        data = [
            [str(getattr(ent, attr)) for attr in attrs]
            for ent in doc.spans[render_error]
        ]
        if data:
            df = pd.DataFrame(data, columns=attrs)
            st.dataframe(df)


# Ref: spacy-streamlit: https://github.com/explosion/spacy-streamlit