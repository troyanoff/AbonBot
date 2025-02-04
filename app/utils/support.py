
from schemas.representations import ClientReprSchema


async def choice_forward_company(
    now_uuid: str,
    companies: list[ClientReprSchema]
):
    len_companies = len(companies)
    if len_companies == 1:
        return companies[0]
    now_company = None
    for company in companies:
        if company.uuid == now_uuid:
            now_company = company
    index_now_company = companies.index(now_company)
    if index_now_company == len_companies - 1:
        return companies[0]
    return companies[index_now_company + 1]


async def choice_back_company(
    now_uuid: str,
    companies: list[ClientReprSchema]
):
    len_companies = len(companies)
    if len_companies == 1:
        return companies[0]
    now_company = None
    for company in companies:
        if company.uuid == now_uuid:
            now_company = company
    index_now_company = companies.index(now_company)
    if index_now_company == 0:
        return companies[len_companies - 1]
    return companies[index_now_company - 1]
