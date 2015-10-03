from zshtwt import user
from zshtwt import authorize_zshtwt

Auth = authorize_zshtwt.Auth().oauth
User = user.User(Auth)

