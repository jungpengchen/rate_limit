
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.schema.runnable import RunnableParallel


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

az_cre={
  "azure_endpoint": "https://chirpai-gpt.openai.azure.com/",
  "deployment_name": "pressure_test-gpt-35",
  "openai_api_version": "2023-07-01-preview",
  "openai_api_key": "0532c4a9894a4e129f562bd6627f0edb",
  "model": "gpt-3.5-turbo"
}

cre={
    "LANGCHAIN_PROJECT": "orin",
    "LANGCHAIN_API_KEY":"ls__8a9d4209c8674947a7d3811d8a70bdcd",
    "LANGCHAIN_ENDPOINT": "https://api.smith.langchain.com",
    "LANGCHAIN_TRACING_V2": "true"
}
for k,v in cre.items():
    os.environ[k]=v
for k,v in az_cre.items():
    os.environ[k]=v
deployment_names = {"large": "yuming-gpt-35", "small": "pressure_test-gpt-35"}

config = {"configurable": {"session_id": "orin_history3"}}

example = """
         ## example
         Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
 Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
Once upon a time in a small, picturesque village nestled amidst rolling hills, there lived a curious little fox named Finn. Finn was known for his playful nature and mischievous adventures. One sunny morning, as Finn ventured out of his cozy den, he noticed a delicate butterfly fluttering nearby.

Intrigued, Finn decided to follow the butterfly, darting through the woods, leaping over fallen logs, and navigating around sparkling streams. The butterfly led him to a beautiful meadow filled with colorful wildflowers. Finn watched in awe as the butterfly gracefully danced from one flower to another, spreading joy with its delicate wings.

As Finn sat mesmerized, a gentle voice called out, "Hello, little fox! Are you enjoying the wonders of this meadow?" Startled, Finn turned to see a wise old owl perched on a branch above.

"Yes, I am," replied Finn, his eyes still fixed on the dancing butterfly. "Isn't it amazing how such a tiny creature can bring so much happiness?"

The owl nodded approvingly and said, "Indeed, young fox. It's the small wonders in life that often bring the greatest joy. Remember to appreciate them always.
"""
system_example_template = ("system", """You're a good stroy teller, and you should tell me a short story in  50 words.
         
""")
messages_list_template = [system_example_template,
        ("human", "{question}")
]

def create_chain(deployment_name, example_count):
    messages_list = messages_list_template.copy()
    messages_list[0] = (system_example_template[0], system_example_template[1]+example[:example_count])
    prompt = ChatPromptTemplate.from_messages(messages_list)
    chain_tmp = prompt | AzureChatOpenAI(
        azure_endpoint=os.environ["azure_endpoint"],
        deployment_name=deployment_names[deployment_name],
        openai_api_version=os.environ["openai_api_version"],
        openai_api_key=os.environ["openai_api_key"],
        timeout=10.0, max_retries=2
        )
    return chain_tmp 

import time
import datetime
from models.Models import Param

def invoke(model_name: str, param: Param):
# 设置测试的请求次数和时间间隔（以秒为单位）

    # 发送请求并测试 TPM
    init_start_time = time.time()
    print(datetime.datetime.now())
    parallel_dict = {}
    # 发送请求前记录当前时间
    start_time = time.time()
    parallel_dict[f"{param.req_id}"] = create_chain(model_name, param.example_ch_count)
    test=RunnableParallel(parallel_dict)
    is_succeed = False
    try:
        result = test.invoke({"question": "tell me a cute story"})
        is_succeed = True
        # 打印请求状态码和执行时间
    except Exception as e:
        print(str(e))
        print(e.__traceback__)
    finally:
        time_now = time.time()
        print(f"{param.req_id} {is_succeed} - Elapsed time: {time_now - start_time:.2f} seconds, Total time: {time_now - init_start_time:.2f} seconds, {datetime.datetime.now()}")
    return is_succeed


