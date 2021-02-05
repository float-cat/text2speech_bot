from t2s import botcfg
from t2s import keyboard
from t2s import preprocessing
from t2s import speakers
from t2s import speechkit
from t2s import tg_bot

from t2s.botcfg import (BotCfg, UserCfg,)
from t2s.keyboard import (BotKeyboard,)
from t2s.preprocessing import (TextPreprocessing,)
from t2s.speakers import (Speakers, checklanguage,)
from t2s.speechkit import (speakersinfo, synthesize,)
from t2s.tg_bot import (TGText2SpeechBot, env_config, tg_t2s_bot,)

__all__ = ['BotCfg', 'BotKeyboard', 'Speakers', 'TGText2SpeechBot',
           'TextPreprocessing', 'UserCfg', 'botcfg', 'checklanguage',
           'env_config', 'keyboard', 'preprocessing', 'speakers',
           'speakersinfo', 'speechkit', 'synthesize', 'tg_bot', 'tg_t2s_bot']

