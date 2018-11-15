import requests

base_url = "https://api.telegram.org/bot{token}/{method}"

def send_message(token, chat_id, text, reply_markup=None):
    url = base_url.format(token=token, method='sendMessage')

    headers = {'Content-Type': 'application/json'}

    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': {
            'inline_keyboard': reply_markup
        }
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code == requests.codes.ok:
        return r.json.get('ok')
    else:
        return r.text


def send_chat_action(token, chat_id, action):
    """Tell the user that something is happening on the bot's side.

    Args:
        token (String): telegram bot token
        chat_id (String): Unique identifier for the target chat or username of the target channel
        action (String): typing | upload_photo | record_video | upload_video | record_audio | upload_audio |
                         upload_document | find_location | record_video_note | upload_video_note

    """

    url = base_url.format(token=token, method='sendChatAction')

    headers = {'Content-Type': 'application/json'}

    payload = {
        'chat_id': chat_id,
        'action': action
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code == requests.codes.ok:
        return r.json().get('ok')
    else:
        return False


def send_photo(token, chat_id, photo, caption=None, reply_markup=None, parse_mode='Markdown'):
    """Send a photo.

    Args:
        token (String): telegram bot token
        chat_id (String): Unique identifier for the target chat or username of the target channel
        photo (InputFile or String): file_id | url | file
        caption (String) : Photo caption. Optional.
        parse_mode (String) : Markdown or HTML. Optional.
        reply_markup (InlineKeyboardMarkup) : Additional interface options.
    """

    url = base_url.format(token=token, method='sendPhoto')

    headers = {'Content-Type': 'application/json'}

    payload = {
        'chat_id': chat_id,
        'photo': photo,
        'parse_mode': parse_mode,
        'caption': caption,
        'reply_markup': {
            'inline_keyboard': [
                reply_markup
            ]
        }
    }
    r = requests.post(url, json=payload, headers=headers)

    if r.status_code == requests.codes.ok:
        return r.json().get('ok')
    else:
        return False
