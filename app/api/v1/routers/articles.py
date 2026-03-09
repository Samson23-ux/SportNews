from decimal import Decimal
from typing import Annotated
from beanie import PydanticObjectId
from fastapi.responses import StreamingResponse
from pymongo.asynchronous.client_session import AsyncClientSession
from fastapi import APIRouter, Depends, Request, Query, Form, UploadFile, File


from app.api.v1.schemas.users import UserRoleV1, AccountV1
from app.dependencies import get_session, required_roles, get_current_user
from app.api.v1.schemas.articles import (
    ImageResponseV1,
    ArticleCreateV1,
    ArticleUpdateV1,
    ArticleResponseV1,
    ArticleDraftCreateV1,
    ArticleDraftResponseV1,
)


articles_router_v1 = APIRouter()


@articles_router_v1.get(
    "/articles",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Get all articles",
)
async def get_articles(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    sport: Annotated[str, Query(description="Filter articles by sport")] = None,
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit users to view at once")] = 20,
    sort: Annotated[str, Query(description="Sort users by created_at")] = None,
    order: Annotated[str, Query(description="Sort users in asc or desc order")] = None,
):
    pass


@articles_router_v1.get(
    "/article/drafts",
    status_code=200,
    response_model=ArticleDraftResponseV1,
    description="Get all drafted articles",
)
async def get_drafts(
    request: Request,
    curr_user: Annotated[
        AccountV1, Depends(required_roles([UserRoleV1.EDITOR, UserRoleV1.AUTHOR]))
    ],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit users to view at once")] = 20,
    sort: Annotated[str, Query(description="Sort users by created_at")] = None,
    order: Annotated[str, Query(description="Sort users in asc or desc order")] = None,
):
    pass


@articles_router_v1.get(
    "/articles/{article_id}",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Get article by its id",
)
async def get_article(
    request: Request,
    article_id: PydanticObjectId,
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.get(
    "/articles/drafts/{draft_id}",
    status_code=200,
    response_model=ArticleDraftResponseV1,
    description="Get draft by its id",
)
async def get_draft(
    request: Request,
    article_id: PydanticObjectId,
    curr_user: Annotated[
        AccountV1, Depends(required_roles([UserRoleV1.EDITOR, UserRoleV1.AUTHOR]))
    ],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.get(
    "/articles/{article_id}/images",
    status_code=200,
    response_class=StreamingResponse,
    description="Get article images",
)
async def get_article_images(
    request: Request,
    article_id: PydanticObjectId,
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.post(
    "/articles",
    status_code=201,
    response_model=ArticleResponseV1,
    description="Create an article. Only authors are allowed to create an article",
)
async def create_article(
    request: Request,
    article_create: ArticleCreateV1,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.AUTHOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.post(
    "/articles/drafts",
    status_code=201,
    response_model=ArticleDraftResponseV1,
    description="Create a draft",
)
async def create_article_draft(
    request: Request,
    draft_create: ArticleDraftCreateV1,
    curr_user: Annotated[
        AccountV1, Depends(required_roles([UserRoleV1.EDITOR, UserRoleV1.AUTHOR]))
    ],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.post(
    "/articles/{article_id}/rate",
    status_code=201,
    response_model=ArticleResponseV1,
    description="Rate an article",
)
async def create_rating(
    request: Request,
    article_id: PydanticObjectId,
    rating: Annotated[Decimal, Form(..., decimal_places=1)],
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.USER]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.post(
    "/articles/{article_id}/images",
    status_code=201,
    response_model=ImageResponseV1,
    description="Upload article images",
)
async def upload_images(
    request: Request,
    article_id: PydanticObjectId,
    article_images: Annotated[list[UploadFile], File()],
    curr_user: Annotated[
        AccountV1, Depends(required_roles([UserRoleV1.AUTHOR, UserRoleV1.EDITOR]))
    ],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.patch(
    "/articles/{article_id}",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Update an existing article. Only editors are allowed to update an article",
)
async def update_article(
    request: Request,
    article_id: PydanticObjectId,
    article_update: ArticleUpdateV1,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.EDITOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.patch(
    "/articles/drafts/{draft_id}",
    status_code=200,
    response_model=ArticleDraftResponseV1,
    description="Update draft. Only editors and authors are allowed to update a draft",
)
async def update_draft(
    request: Request,
    draft_id: PydanticObjectId,
    draft_update: ArticleDraftCreateV1,
    curr_user: Annotated[
        AccountV1, Depends(required_roles([UserRoleV1.EDITOR, UserRoleV1.AUTHOR]))
    ],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.patch(
    "/articles/{article_id}/rate",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Update a rating",
)
async def update_rating(
    request: Request,
    article_id: PydanticObjectId,
    rating: Annotated[Decimal, Form(..., decimal_places=1)],
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.USER]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.delete(
    "/articles/{article_id}",
    status_code=204,
    description="Delete an existing article. Only admin are allowed to delete an article",
)
async def delete_article(
    request: Request,
    article_id: PydanticObjectId,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.delete(
    "/articles/drafts/{draft_id}",
    status_code=204,
    description="Delete a draft. Only authors and editors are allowed to delete a draft",
)
async def delete_draft(
    request: Request,
    draft_id: PydanticObjectId,
    curr_user: Annotated[
        AccountV1, Depends(required_roles([UserRoleV1.EDITOR, UserRoleV1.AUTHOR]))
    ],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.delete(
    "/articles/{article_id}/remove-rating",
    status_code=204,
    description="Remove a rating",
)
async def delete_rating(
    request: Request,
    article_id: PydanticObjectId,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.USER]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@articles_router_v1.delete(
    "/articles/{article_id}/images",
    status_code=204,
    description="Delete article images",
)
async def delete_images(
    request: Request,
    article_id: PydanticObjectId,
    article_images: Annotated[
        list[str], Form(..., description="A list of image names to delete")
    ],
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.AUTHOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass
