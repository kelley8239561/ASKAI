from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def getTemplate():
    pass


# 简单对话使用
simpleChatPrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    你是李开的个人助理，你要想办法准确干练的回答李开的所有问题。
                    对于想要找李开的人，你要了解他们的诉求，并向办法解决他们的问题并向李开进行汇报
                """,
                input_variables = [],
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="我是李开，你的主人，{humanInfor}",
                input_variables = ["humanInfor"],
            )
        ), 
        AIMessagePromptTemplate(
            prompt=PromptTemplate(
                template="",
                input_variables = [],
            )
        ),
    ]
)

'''
# for Debug
chat_prompt.format_prompt(
    input_language="haha", 
    output_language="hoho", 
    text="aaaaaaaaaaa", 
    lastResponse='lalalala'
).to_messages()
'''



