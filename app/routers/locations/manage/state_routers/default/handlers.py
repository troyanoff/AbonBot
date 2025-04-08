import logging

from aiogram import Router

from handlers.base import Data
from handlers.manage.base import ManageBase, ManageConfig
from schemas.representations import LocationListSchema, ClientReprSchema
from services.clients import get_client_service
from services.locations import get_location_service
from routers.locations.manage.state import states_group
from .terminology import terminology


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.manage


async def location_count(data: Data):
    state_data = await data.request.state.get_data()
    company_uuid = state_data['company_uuid']
    client_uuid = state_data['client_uuid']
    service = get_client_service()
    client: ClientReprSchema = await service.get(uuid=client_uuid)
    location_service = get_location_service()
    locations: LocationListSchema = await location_service.get_list(
        company_uuid=company_uuid)
    return client.is_premium or locations.total_count == 0


config = ManageConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='location',
    service_caller=get_location_service,
    term=terminology,
    callbacks={
        'update': 'routers.locations.update.handler',
        'create': 'routers.locations.create.handler',
    },
    callbacks_validate={
        'create': (location_count, 'forbitten')
    },
    format_caption={
        'name': 'name',
        'description': 'description',
        'city': 'city',
        'street': 'street',
        'house': 'house',
        'flat': 'flat',
    },
    back_button='back_state'
)

handler = ManageBase(
    config=config
)
