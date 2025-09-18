class Ops:
    ADD_TABLE = "add_table"
    UPDATE_TABLE = "update_table"
    DROP_TABLE = "drop_table"
    ADD_API = "add_api"
    UPDATE_API = "update_api"
    DROP_API = "drop_api"

class IrTypes:
    ENTITY = "entity"
    API = "api"

class ModeTypes:
    SPEC = "spec"
    ADVICE = "advice"

class RoleTypes:
    USER = "user"
    SYSTEM = "system"

PROMPT_TEMPLATE = "{} + \n\n目前的規格如下:\n + {}"
PROMPT_TEMPLATE_2 = """
    你是系統規格分析助手，必須僅根據提供的文件內容回答；
    問題：{}\n\n
    文件內容：\n{}
    """
MAX_CTX_CHARS = 12000