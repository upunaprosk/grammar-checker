import streamlit as st
import spacy


def get_html(html: str):
    """Convert HTML so it can be rendered."""
    WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")
    return WRAPPER.format(html)


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_model(name: str) -> spacy.language.Language:
    """Load a spaCy model."""
    return spacy.load(name)


DEFAULT_LABEL_COLORS = {'Spelling': '#FFFF00',
                        'Capitalisation': '#FFD700',
                        'Lex part choice': '#00FA9A',
                        'Lex item choice': '#90EE90',
                        'Category confusion': '#98FB98',
                        'Formational affixes': '#66CDAA',
                        'Verb pattern': '#C71585',
                        'Noun number': '#DB7093',
                        'Word order': '#FF1493',
                        'Numerals': '#FF69B4',
                        'Determiners': '#FFB6C1',
                        'Agreement errors': '#FFC0CB',
                        'Prepositions': '#7B68EE',
                        'Redundant comp': '#6495ED',
                        'Tense choice': '#1E90FF',
                        'Punctuation': '#A52A2A',
                        'Articles': '#D2691E'}

TPL_SPAN = """
    <span style="font-weight: bold; display: inline-block; position: relative;">
        {text}
        {span_slices}
        {span_starts}
    </span>
    """

TPL_SPAN_SLICE = """
    <span style="background: {bg}; top: {top_offset}px; height: 1px; left: -1px; width: calc(100% + 2px); position: absolute;">
    </span>
    """

TPL_SPAN_START = """
    <span style="background: {bg}; top: {top_offset}px; height: 4px; border-top-left-radius: 2px; border-bottom-left-radius: 3px; left: -1px; width: calc(100% + 1px); position: absolute;">
        <span style="background: {bg}; z-index: 10; color: #000; top: -0.5em; padding: 2px 3px; position: absolute; font-size: 0.6em; font-weight: bold; line-height: 1; border-radius: 3px">
            {label}{kb_link}
        </span>
    </span>
    """

SDDESCRIPTION = """

|  | Description |
| --- | --- |
| **Pipeline** | `punctuation`, `spelling`, `articles`, `grammar_major`, `grammar_minor`, `vocabulary` |
| **f1-scores** | `punctuation`:0.760, `spelling`:0.910, `capitalisation`:0.871, `articles`:0.824, `lex_part_choice`: 0.14, `lex_item_choice`: 0.644, `Category_confusion`: 0.640, `Formational_affixes`: 0.688, `Verb_pattern`:0.373, `Noun_number`:0.897, `Word_order`:0.345, `Numerals`:0.650, `Determiners`:0.044, `Agreement_errors`:0.830, `Prepositions`:0.694, `Redundant_comp`:0.452, `Tense_choice`:0.794  |"""
