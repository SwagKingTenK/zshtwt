
from zshtwt import user

User = user.User('user_config.txt', 'followers.csv', 'following.csv')
User.authUser()