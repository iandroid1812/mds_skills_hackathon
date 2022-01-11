import df_engine.conditions as cnd
import df_engine.labels as lbl
from df_engine.core import Actor
from df_engine.core.keywords import LOCAL, RESPONSE, TRANSITIONS

import scenario.condition as loc_cnd
import scenario.response as rsp

# TODO: extend graph
plot = {
    "service_flow": {
        LOCAL: {
            TRANSITIONS: {
                ("greeting_flow", "node1"): loc_cnd.greeting_condition,
                # ("weather_flow", "node1"): loc_cnd.weather_condition,
                # ("light_flow", "node1"): loc_cnd.light_condition
            }
        },
        "start_node": {RESPONSE: ""},
        "fallback_node": {RESPONSE: "I didn't quite catch that, can you repeat please?"},
    },
    "greeting_flow": {
        "node1": {
            RESPONSE: "Hello, I am your Home Assistant. How can I help?",
            TRANSITIONS: {
                ("weather_flow", "node1"): loc_cnd.weather_condition,
                ("light_flow", "node1"): loc_cnd.light_condition,
            }
        }
    },
    "weather_flow": {
        "node1": {
            RESPONSE: rsp.basic_weather_response,
            TRANSITIONS: {
                ("weather_flow", "node2"): loc_cnd.condition_yes,
                ("weather_flow", "negative_node"): loc_cnd.condition_no
            }
        },
        "node2": {
            RESPONSE: rsp.extra_weather_response,
            TRANSITIONS: {
                ("appreciation_flow", "node1"): loc_cnd.appreciate_condition
            }
        },
        "negative_node": {
            RESPONSE: "Ok, that's it for the weather then.",
            TRANSITIONS: {
                ("service_flow", "start_node"): cnd.true()
            }
        }
    },
    "light_flow": {
        "node1": {
            RESPONSE: "Ok, in which room?",
            TRANSITIONS: {
                ("light_flow", "node2"): loc_cnd.room_condition,
                lbl.repeat(): cnd.true()
            }
        },
        "node2": {
            RESPONSE: rsp.light_response,
            TRANSITIONS: {
                ("appreciation_flow", "node1"): loc_cnd.appreciate_condition
            }
        }
    },
    "appreciation_flow": {
        "node1": {
            RESPONSE: "Glad I could help!",
            TRANSITIONS: {
                ("service_flow", "start_node"): cnd.true()
            }
        }
    }
}


actor = Actor(
    plot,
    start_label=("service_flow", "start_node"),
    fallback_label=("service_flow", "fallback_node")
)


