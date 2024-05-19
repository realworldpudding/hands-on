from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def toppage() -> dict:
    return {
        'message': 'Hello, world!',
    }
