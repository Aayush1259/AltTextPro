class AltContextError(Exception):
    pass

class OpenAIError(AltContextError):
    pass

class LangChainError(AltContextError):
    pass