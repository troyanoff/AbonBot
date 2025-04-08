import logging

from aiogram import Router

from handlers.manage.base import ManageBase, ManageConfig, Data
from schemas.representations import ClientReprSchema, CompanyListSchema
from services.clients import get_client_service
from services.companies import get_company_service
from routers.clients.profile.state import states_group
from .terminology import terminology


async def company_count(data: Data):
    state_data = await data.request.state.get_data()
    client_uuid = state_data['client_uuid']
    service = get_client_service()
    client: ClientReprSchema = await service.get(uuid=client_uuid)
    company_service = get_company_service()
    companies: CompanyListSchema = await company_service.get_list(
        creator_uuid=client_uuid)
    return client.is_premium or companies.total_count == 0


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.profile

config = ManageConfig(
    logger=logger,
    router=router,
    states_group=states_group,
    router_state=router_state,
    item_prefix='client',
    service_caller=get_client_service,
    term=terminology,
    callbacks={
        'update_profile': 'routers.clients.update.handler',
        'create_company': 'routers.companies.create.handler',
    },
    callbacks_validate={
        'create_company': (company_count, 'forbitten')
    },
    format_caption={
        'first_name': 'first_name',
        'last_name': 'last_name',
        'sex': 'sex',
    }
)

handler = ManageBase(
    config=config
)
