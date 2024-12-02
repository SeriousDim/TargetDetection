from fastapi import APIRouter

service_router = APIRouter(
    tags=["detection"]
)

@service_router.post("/predict")
async def predict():
    return {
        "target": {
            "center": {
                "x": 10,
                "y": 10
            },
            "width": 10,
            "height": 10
        },
        "hits": [
            {
                "center": {
                    "x": 10,
                    "y": 10
                },
                "width": 10,
                "height": 10
            }
        ],
        "image_size": {
            "width": 10,
            "height": 10
        }
    }


@service_router.post("/recommendations")
async def get_recommendations():
    return ""
