from channels.db import database_sync_to_async
from ..models import Tagger


@database_sync_to_async
def get_tagger(client_id) -> Tagger:
    return Tagger.objects.get(client_id=client_id)

