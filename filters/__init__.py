from loader import dp
from .Admin import IsAdmin
from .Group import IsGroup
from .Chat import IsPrivate
from .Is_Admin_bot import IsAdmin_bot

if __name__ == 'filters':
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin_bot)
