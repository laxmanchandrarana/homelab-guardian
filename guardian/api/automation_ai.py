from fastapi import APIRouter

router=APIRouter(prefix="/ai",tags=["AI"])

@router.get("/automation")
def automation_ai():

    return {

        "health":94,

        "recommendations":[

            {
                "severity":"high",
                "title":"Enable restart automation",
                "description":"Nextcloud has no recovery rule configured."
            },

            {
                "severity":"medium",
                "title":"Restart cooldown",
                "description":"Increase cooldown from 60s to 300s."
            },

            {
                "severity":"low",
                "title":"Retry count",
                "description":"Use 3 retries for Docker services."
            }

        ]

    }

