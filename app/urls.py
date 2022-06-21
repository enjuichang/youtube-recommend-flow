# -*- coding: utf-8 -*-
from app.extensions import api
from app.controllers import (
    health,
    gpt3_wrapper
)


# Health Routes
api.add_resource(health.HealthResource, '/', '/health')
# GPT3 Wrapper
api.add_resource(gpt3_wrapper.GPT3Resource, '/gpt3')
