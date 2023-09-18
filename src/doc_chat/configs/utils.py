import yaml
import os


class LLMConfig:
    config_path_relative = "doc_chat/configs/llm_config.yaml"
    with open(config_path_relative, 'r') as file:
        configs = yaml.safe_load(file)


l = LLMConfig()
# print(l.configs)
