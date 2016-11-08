import trafaret as t


CHAT_TYPES = ['private', 'group', 'supergroup', 'channel']
ENTITY_TYPES = ['mention', 'hashtag', 'bot_command', 'url', 'email', 'bold', 'italic', 'code',
                'pre', 'text_link', 'text_mention']

chosen_inline_result = t.Dict()
callback_query = t.Dict()
inline_query = t.Dict()

user = t.Dict({
    'id': t.Int(gt=0),       # Integer Unique identifier for this user or bot
    'first_name': t.String,  # User‘s or bot’s first name
    'last_name': t.String,   # User‘s or bot’s last name
    'username': t.String,    # User‘s or bot’s username
}).make_optional('last_name', 'username')

chat = t.Dict({
    'id': t.Int(gt=0),            # Integer Unique identifier for this chat.
    'type': t.Enum(*CHAT_TYPES),  # Type of chat
    'title': t.String,            # Title, for supergroups, channels and group chats
    'username': t.String,         # Username, for private chats, supergroups and channels
    'first_name': t.String,       # First name of the other party in a private chat
    'last_name': t.String,        # Last name of the other party in a private chat
    'all_members_are_administrators': t.Bool,  # True if a group has ‘All Members Are Admins’ enabled.
}).make_optional('title', 'username', 'first_name', 'last_name', 'all_members_are_administrators')

message_entity = t.Dict({
    'type': t.Enum(ENTITY_TYPES),  # Type of the entity. ENTITY_TYPES
    'offset': t.Int(gt=0),         # Offset in UTF-16 code units to the start of the entity
    'length': t.Int(gt=0),         # Length of the entity in UTF-16 code units
    'url': t.String,               # For “text_link” only, url that will be opened after user taps on the text
    'user': user,                  # User. For “text_mention” only, the mentioned user
}).make_optional('url', 'user')

message = t.Dict({
    'message_id': t.Int(gt=0),
    'date': t.Int(gt=0),
    'from': user,
    'forward_from': user,
    'chat': chat,
    'forward_from_chat': chat,
    'forward_date': t.Int(gt=0),
    'reply_to_message': t.Dict().allow_extra('*'),
    'text': t.String,
    'entities': t.List(message_entity)
}).make_optional(
    'from', 'forward_from', 'forward_from_chat', 'forward_date', 'reply_to_message'
).ignore_extra('*')

update = t.Dict({
    'update_id': t.Int(gt=0),
    'message': message,
    'edited_message': message,
    'inline_query': inline_query,
    'chosen_inline_result': chosen_inline_result,
    'callback_query': callback_query
}).make_optional(
    'message', 'edited_message', 'inline_query', 'chosen_inline_result', 'callback_query'
)


