import json
import logging
import logging.config
import os

def setup_logging(
    default_path='configs/logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def preload_fonts():
    from hammerdraw.text_drawer import TextDrawer
    default_finder = TextDrawer.get_default_text_finder()
    default_finder.preload_font('times.ttf', 'Times New Roman')
    default_finder.preload_font('timesbd.ttf', 'Times New Roman', bold=True)
    default_finder.preload_font('timesi.ttf', 'Times New Roman', italic=True)
    default_finder.preload_font('timesbi.ttf', 'Times New Roman', italic=True, bold=True)
    default_finder.preload_font('BOD_R.TTF', 'Bodoni MT')
    default_finder.preload_font('BOD_B.TTF', 'Bodoni MT', bold=True)
    default_finder.preload_font('BOD_CR.TTF', 'Bodoni MT Condensed')
    default_finder.preload_font('BOD_CB.TTF', 'Bodoni MT Condensed', bold=True)
    default_finder.preload_font('constan.ttf', 'Constantia')
    default_finder.preload_font('constanb.ttf', 'Constantia', bold=True)
    default_finder.preload_font('constani.ttf', 'Constantia', italic=True)
    default_finder.preload_font('constanz.ttf', 'Constantia', italic=True, bold=True)

