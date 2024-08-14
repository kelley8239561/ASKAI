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
from task.parser import taskParser

def getTemplate():
    pass


# 任务分解
taskSplit = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    你是李开的个人助理，你可以代替李开在电脑上做任意操作，你要想尽办法根据李开给你的任务指令给出非常详细的计划。
                """,
                input_variables = [],
            )
        ),
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    你可以遵从以下的行动和思考步骤：  
                    # 1. 计划生成：根据任务指令信息，生成计划列表<AppTaskList>
                    - 计划列表<AppTaskList>中每一条。需要包含使用哪个app，任务指引taskInstruction以及需要达到的目标objective
                    # 2. 可行性分析：对于计划列表<AppTaskList>中每一条计划，进行如下的思考
                    - 是不是必要的，如果不必要，则在计划列表<AppTaskList>中去掉该条计划
                    - 参考后续给出的<ComputerAppList>，判断该条计划中的app能否完成任务指引taskInstruction并达到目标objective，如果不能，需要对该条计划进行调整直至能够完成任务指引taskInstruction并达到目标objective
                """,
                input_variables = [],
            )
        ),
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    你使用的Computer是windows操作系统，你可以通过搜索获取windows系统的原生功能，同时我们也对可以帮助你完成任务的app列表<ComputerAppList>进行了如下的列举和描述
                    '''
                    <ComputerAppList>
                    [
                        {{
                            'app':'微信'  
                            'description':'方便在电脑上与微信好友沟通，传输文件等' 
                        }},
                        {{
                            'app':'Foxmail'  
                            'description':'邮件管理软件，支持所有邮件的相关功能，比如发送、接受、编辑邮件'     
                        }},
                        {{
                            'app':'Microsoft Office（Word、Excel、PowerPoint）'  
                            'description':'Word 用于文字处理和文档编辑,Excel 用于数据处理和分析,PowerPoint 用于制作演示文稿'    
                        }},
                        {{
                            'app':'腾讯文档'  
                            'description':'在线文档协作工具，支持多人同时编辑，实时保存'    
                        }},
                        {{
                            'app':'XMind'  
                            'description':'思维导图软件，用于整理思路、规划项目等'    
                        }},
                        {{
                            'app':'百度网盘'  
                            'description':'云存储服务，方便文件的上传、下载和分享'    
                        }},
                        {{
                            'app':'迅雷'  
                            'description':'下载工具，支持多种下载协议，提高下载速度'    
                        }},
                        {{
                            'app':'Edge浏览器'  
                            'description':''    
                        }},
                        {{
                            'app':'Chrome浏览器'  
                            'description':'能够加载和显示各种网页，包括文字、图片、音频、视频等多种元素，让用户获取丰富的信息。具备搜索栏，用户输入关键词后，浏览器会连接搜索引擎，快速呈现相关的搜索结果。
                                            允许用户将感兴趣或经常访问的网页添加到书签或收藏夹中，方便下次快速访问。
                                            自动记录用户访问过的网页，便于用户回顾和查找之前浏览过的内容。
                                            支持同时打开多个网页，并以标签页的形式呈现，用户可以轻松切换和关闭标签页。
                                            能够下载文件、文档、图片、视频等各种资源，并对下载任务进行管理，如暂停、继续、取消等。
                                            可以安装各种插件和扩展程序，以增加额外的功能，如广告拦截、密码管理、网页截图等。
                                            提供选项来控制浏览器的隐私设置，例如清除浏览数据、阻止跟踪器、启用加密连接等，保护用户的隐私和安全。
                                            记住用户在表单中输入的个人信息，如用户名、密码、地址等，在需要时自动填充，提高填写表单的效率。'    
                        }},
                        {{
                            'app':'应用搜索'  
                            'description':'可以便捷进入到各个应用'    
                        }},
                        {{
                            'app':'语音对话'  
                            'description':'可以基于某个话题跟一个人进行对话并获取对话内容信息'    
                        }},
                        {{
                            'app':'文案生成'  
                            'description':'根据给定的背景信息，生成一段文字，可以是邮件、对话内容或者其他正式或非正式的文案'    
                        }},
                        
                    ]
                    '''
                """,
                input_variables = [],
            )
        ),
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    以下是一个案例：
                    针对任务taskInstruction：给微软客服发送一封报修邮件，生成计划列表<AppTaskList>：
                    '''
                    {{
                        "taskInstruction":"给微软客服发送一封报修邮件",
                        "tasks":[
                            {{
                                "app":"应用搜索",
                                "task":"搜索并打开Foxmail",
                                "objective":"Foxmail打开"
                            }},
                            {{
                                "app":"Foxmail",
                                "task":"登录账号",
                                "objective":"账号登录完成"
                            }},
                            {{
                                "app":"语音对话",
                                "task":"调用语音对话api，询问并记录邮件关键内容",
                                "objective":"获取邮件关键内容<content>"
                            }},
                            {{
                                "app":"文案生成",
                                "task":"调用文案生成api，通过输入邮件关键内容<content>，获取完整邮件<mail>",
                                "objective":"生成完整邮件<mail>"
                            }},
                            {{
                                "app":"Foxmail",
                                "task":"发送完整邮件<mail>",
                                "objective":"完成给微软客服发送一封报修邮件"
                            }},
                            {{
                                "app":"应用搜索",
                                "task":"搜索并打开Foxmail",
                                "objective":"Foxmail打开"
                            }}
                        ]
                    }}
                """,
                input_variables = [],
            )
        ),
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    The output should be formatted as a JSON instance that conforms to the JSON schema below.As an example, for the schema 
                    {{
                        "properties": {{
                            "foo": {{
                                "title": "Foo",
                                "description": "a list of strings",
                                "type": "array",
                                "items": {{
                                    "type": "string"
                                }}
                            }}
                        }},
                        "required": [
                            "foo"
                        ]
                    }}
                    the object {{
                        "foo": [
                            "bar",
                            "baz"
                        ]
                    }} is a well-formatted instance of the schema. The object {{
                        "properties": {{
                            "foo": [
                                "bar",
                                "baz"
                            ]
                        }}
                    }} is not well-formatted.

                    Here is the output schema:
                    ```
                    {{
                        "properties": {{
                            "taskInstruction": {{
                                "title": "Taskinstruction",
                                "escription": "\u8981\u5b8c\u6210\u7684\u4efb\u52a1\u63cf\u8ff0",
                                "type": "string"
                            }},
                            "tasks": {{
                                "title": "Tasks",
                                "description": "\u5b8c\u6210taskInstruction\u9700\u8981\u7684AppTask\u5217\u8868\uff0c\u6bcf\u4e00\u884c\u662f\u4e00\u4e2aAppTask",
                                "type": "array",
                                "items": {{
                                    "$ref": "#/definitions/AppTask"
                                }}
                            }}
                        }},
                        "required": [
                            "taskInstruction",
                            "tasks"
                        ],
                        "definitions": {{
                            "AppTask": {{
                                "title": "AppTask",
                                "type": "object",
                                "properties": {{
                                    "app": {{
                                        "title": "App",
                                        "description": "\u5b8c\u6210\u4efb\u52a1\u8981\u4f7f\u7528\u7684app/\u9875\u9762\u540d\u79f0",
                                        "type": "string"
                                    }},
                                    "task": {{
                                        "title": "Task",
                                        "description": "\u5728\u5f53\u524dapp\u6216\u9875\u9762\u9700\u8981\u5b8c\u6210\u7684\u4efb\u52a1\u63cf\u8ff0",
                                        "type": "string"
                                    }},
                                    "objective": {{
                                        "title": "Objective",
                                        "description": "\u5728\u5f53\u524dapp\u6216\u9875\u9762\u5b8c\u6210\u4efb\u52a1\u540e\u9700\u8981\u8fbe\u5230\u7684\u72b6\u6001",
                                        "type": "string"
                                    }}
                                }},
                                "required": [
                                    "app",
                                    "task",
                                    "objective"
                                ]
                            }}
                        }}
                    }}
                    ```
                """,
                input_variables = [],
            )
        ),
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    目前你正在电脑前接收任务指令，请根据下面的指令生成计划列表<AppTaskList>
                """,
                input_variables = [],
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{humanInfor}",
                input_variables = ["humanInfor"],
            )
        ), 
    ]
)

taskSplit1 = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    你是李开的个人助理，你可以代替李开在电脑上做任意操作，你要想尽办法根据李开给你的任务指令给出非常详细的计划。
                    
                    你可以遵从以下的行动和思考步骤：  
                    # 1. 计划生成：根据任务指令信息，生成计划列表<AppTaskList>
                    - 计划列表<AppTaskList>中每一条。需要包含使用哪个app，任务指引taskInstruction以及需要达到的目标objective
                    # 2. 可行性分析：对于计划列表<AppTaskList>中每一条计划，进行如下的思考
                    - 是不是必要的，如果不必要，则在计划列表<AppTaskList>中去掉该条计划
                    - 参考后续给出的<ComputerAppList>，判断该条计划中的app能否完成任务指引taskInstruction并达到目标objective，如果不能，需要对该条计划进行调整直至能够完成任务指引taskInstruction并达到目标objective
                    你使用的Computer是windows操作系统，你可以通过搜索获取windows系统的原生功能，同时我们也对可以帮助你完成任务的app列表<ComputerAppList>进行了如下的列举和描述
                    '''
                    <ComputerAppList>
                    [
                        {{
                            'app':'微信'  
                            'description':'方便在电脑上与微信好友沟通，传输文件等' 
                        }},
                        {{
                            'app':'Foxmail'  
                            'description':'邮件管理软件，支持所有邮件的相关功能，比如发送、接受、编辑邮件'     
                        }},
                        {{
                            'app':'Microsoft Office（Word、Excel、PowerPoint）'  
                            'description':'Word 用于文字处理和文档编辑,Excel 用于数据处理和分析,PowerPoint 用于制作演示文稿'    
                        }},
                        {{
                            'app':'腾讯文档'  
                            'description':'在线文档协作工具，支持多人同时编辑，实时保存'    
                        }},
                        {{
                            'app':'XMind'  
                            'description':'思维导图软件，用于整理思路、规划项目等'    
                        }},
                        {{
                            'app':'百度网盘'  
                            'description':'云存储服务，方便文件的上传、下载和分享'    
                        }},
                        {{
                            'app':'迅雷'  
                            'description':'下载工具，支持多种下载协议，提高下载速度'    
                        }},
                        {{
                            'app':'Edge浏览器'  
                            'description':''    
                        }},
                        {{
                            'app':'Chrome浏览器'  
                            'description':'能够加载和显示各种网页，包括文字、图片、音频、视频等多种元素，让用户获取丰富的信息。具备搜索栏，用户输入关键词后，浏览器会连接搜索引擎，快速呈现相关的搜索结果。
                                            允许用户将感兴趣或经常访问的网页添加到书签或收藏夹中，方便下次快速访问。
                                            自动记录用户访问过的网页，便于用户回顾和查找之前浏览过的内容。
                                            支持同时打开多个网页，并以标签页的形式呈现，用户可以轻松切换和关闭标签页。
                                            能够下载文件、文档、图片、视频等各种资源，并对下载任务进行管理，如暂停、继续、取消等。
                                            可以安装各种插件和扩展程序，以增加额外的功能，如广告拦截、密码管理、网页截图等。
                                            提供选项来控制浏览器的隐私设置，例如清除浏览数据、阻止跟踪器、启用加密连接等，保护用户的隐私和安全。
                                            记住用户在表单中输入的个人信息，如用户名、密码、地址等，在需要时自动填充，提高填写表单的效率。'    
                        }},
                        {{
                            'app':'应用搜索'  
                            'description':'可以便捷进入到各个应用'    
                        }},
                        {{
                            'app':'语音对话'  
                            'description':'可以基于某个话题跟一个人进行对话并获取对话内容信息'    
                        }},
                        {{
                            'app':'文案生成'  
                            'description':'根据给定的背景信息，生成一段文字，可以是邮件、对话内容或者其他正式或非正式的文案'    
                        }},
                        
                    ]
                    '''
                    以下是一个案例：
                    针对任务taskInstruction：给微软客服发送一封报修邮件，生成计划列表<AppTaskList>：
                    '''
                    {{
                        "taskInstruction":"给微软客服发送一封报修邮件",
                        "tasks":[
                            {{
                                "app":"应用搜索",
                                "task":"搜索并打开Foxmail",
                                "objective":"Foxmail打开"
                            }},
                            {{
                                "app":"Foxmail",
                                "task":"登录账号",
                                "objective":"账号登录完成"
                            }},
                            {{
                                "app":"语音对话",
                                "task":"调用语音对话api，询问并记录邮件关键内容",
                                "objective":"获取邮件关键内容<content>"
                            }},
                            {{
                                "app":"文案生成",
                                "task":"调用文案生成api，通过输入邮件关键内容<content>，获取完整邮件<mail>",
                                "objective":"生成完整邮件<mail>"
                            }},
                            {{
                                "app":"Foxmail",
                                "task":"发送完整邮件<mail>",
                                "objective":"完成给微软客服发送一封报修邮件"
                            }},
                            {{
                                "app":"应用搜索",
                                "task":"搜索并打开Foxmail",
                                "objective":"Foxmail打开"
                            }}
                        ]
                    }}
                    The output should be formatted as a JSON instance that conforms to the JSON schema below.As an example, for the schema 
                    {{
                        "properties": {{
                            "foo": {{
                                "title": "Foo",
                                "description": "a list of strings",
                                "type": "array",
                                "items": {{
                                    "type": "string"
                                }}
                            }}
                        }},
                        "required": [
                            "foo"
                        ]
                    }}
                    the object {{
                        "foo": [
                            "bar",
                            "baz"
                        ]
                    }} is a well-formatted instance of the schema. The object {{
                        "properties": {{
                            "foo": [
                                "bar",
                                "baz"
                            ]
                        }}
                    }} is not well-formatted.

                    Here is the output schema:
                    ```
                    {{
                        "properties": {{
                            "taskInstruction": {{
                                "title": "Taskinstruction",
                                "escription": "\u8981\u5b8c\u6210\u7684\u4efb\u52a1\u63cf\u8ff0",
                                "type": "string"
                            }},
                            "tasks": {{
                                "title": "Tasks",
                                "description": "\u5b8c\u6210taskInstruction\u9700\u8981\u7684AppTask\u5217\u8868\uff0c\u6bcf\u4e00\u884c\u662f\u4e00\u4e2aAppTask",
                                "type": "array",
                                "items": {{
                                    "$ref": "#/definitions/AppTask"
                                }}
                            }}
                        }},
                        "required": [
                            "taskInstruction",
                            "tasks"
                        ],
                        "definitions": {{
                            "AppTask": {{
                                "title": "AppTask",
                                "type": "object",
                                "properties": {{
                                    "app": {{
                                        "title": "App",
                                        "description": "\u5b8c\u6210\u4efb\u52a1\u8981\u4f7f\u7528\u7684app/\u9875\u9762\u540d\u79f0",
                                        "type": "string"
                                    }},
                                    "task": {{
                                        "title": "Task",
                                        "description": "\u5728\u5f53\u524dapp\u6216\u9875\u9762\u9700\u8981\u5b8c\u6210\u7684\u4efb\u52a1\u63cf\u8ff0",
                                        "type": "string"
                                    }},
                                    "objective": {{
                                        "title": "Objective",
                                        "description": "\u5728\u5f53\u524dapp\u6216\u9875\u9762\u5b8c\u6210\u4efb\u52a1\u540e\u9700\u8981\u8fbe\u5230\u7684\u72b6\u6001",
                                        "type": "string"
                                    }}
                                }},
                                "required": [
                                    "app",
                                    "task",
                                    "objective"
                                ]
                            }}
                        }}
                    }}
                    ```
                    目前你正在电脑前接收任务指令，请根据下面的指令生成计划列表<AppTaskList>
                """,
                input_variables = [],
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{humanInfor}",
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


# 任务获取
taskExtract = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="""
                    你是李开的个人助理，你要从跟他的对话中，获取到需要代替他去做的任务，并按照以下格式进行输出
                    
                    # 格式
                    (
                        {{
                            task：*****,
                            obj:*****,
                        }},
                        {{
                            task：*****,
                            obj:*****,
                        }},
                        ……
                    )
                    
                    其中，
                    task:*****是要描述清楚要去完成的任务
                    boj:*****是要描述清楚最终要达到的目的或效果是什么样的
                    
                    例如：
                    task:给爸爸发送一条祝福短信
                    obj:祝福短信发送成功
                """,
                input_variables = [],
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{humanInfor}",
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
