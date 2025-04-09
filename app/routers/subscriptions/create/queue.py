from handlers.remember.base import RememberConfig, Remember
from schemas.base import RememberTypeEnum
from schemas.subscriptions import SubscriptionCreateSchema
from services.subscriptions import get_subscription_service
from .state_routers.client.handlers import handler as client


config = RememberConfig(
    remember_type=RememberTypeEnum.create,
    item_prefix='subscription',
    service_caller=get_subscription_service,
    schema=SubscriptionCreateSchema,
    queue=[client, ],
    manage_caller=(
        'routers.subscriptions.manage_managment.handler'
    ),
)

handler = Remember(
    config=config
)
