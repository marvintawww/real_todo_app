from src.repositories.jwt import JWTQueryRepository, JWTCommandRepository


async def test_create_and_get_token_by_jti(db_session, created_jwtblacklist_item):
    query_repo = JWTQueryRepository(session=db_session)
    found = await query_repo.get_by_jti(jti="124")

    assert found is not None
    assert found.jti == "124"
