PLUGIN_REGISTRY = {}

def register_plugin(plugin_cls):
    for intent in plugin_cls.intents:
        PLUGIN_REGISTRY[intent] = plugin_cls
