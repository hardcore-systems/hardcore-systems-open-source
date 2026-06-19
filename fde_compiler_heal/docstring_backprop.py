import os
import json
from openai import OpenAI

class DocstringBackpropagation:
    """
    A generic closed-loop optimizer that runs an agent with a mock tool,
    captures execution errors in the sandbox, and refines the tool's docstring.
    """
    def __init__(self, api_key=None, base_url="https://api.deepseek.com"):
        self.client = OpenAI(
            api_key=api_key or os.getenv("DEEPSEEK_API_KEY"),
            base_url=base_url
        )

    def run_optimizer_loop(self, tool_executor, initial_desc, task_desc, max_iterations=4):
        tool_description = initial_desc
        history = []
        
        for i in range(max_iterations):
            print(f"\n--- Iteration {i+1} ---")
            print(f"Current Tool Description: '{tool_description}'")
            
            # 1. Forward Pass: Agent generates action
            decision = self.call_agent(tool_description, task_desc)
            action = decision.get("action", "")
            query_val = decision.get("query", "")
            print(f"Agent Action: {action}, Query Passed: '{query_val}'")
            
            # 2. Execute tool
            result = tool_executor(query_val)
            print(f"Tool Result Status: {result['status']}")
            
            step_log = {
                "iteration": i + 1,
                "description": tool_description,
                "query_passed": query_val,
                "result": result,
                "critique": ""
            }
            
            if result["status"] == "success":
                print("Success! Agent called the tool correctly.")
                history.append(step_log)
                break
                
            # 3. Backward Pass: Compile new description
            if i < max_iterations - 1:
                critique, refined_desc = self.compile_new_tool_description(
                    tool_description, query_val, result["message"]
                )
                print(f"Critique: {critique}")
                print(f"Refined Desc: '{refined_desc}'")
                step_log["critique"] = critique
                tool_description = refined_desc
                
            history.append(step_log)
        return history

    def call_agent(self, tool_desc, task_desc):
        system_prompt = (
            "You are an assistant equipped with a database query tool. Your task is to fulfill the request.\n"
            "To accomplish this, you must output a JSON action invoking the tool. "
            "Output ONLY the JSON object. Do not wrap it in markdown block quotes.\n\n"
            "Available Tools:\n"
            f"- query_database(query): {tool_desc}\n\n"
            "Tool invocation format:\n"
            '{"action": "query_database", "query": "your input parameter here"}'
        )
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": task_desc}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"action": "error", "query": str(e)}

    def compile_new_tool_description(self, current_desc, agent_input, tool_error):
        system_prompt = (
            "You are a Compiler Optimizer. Your task is to optimize a Tool Description (docstring) "
            "so that an AI Agent calls the tool with correct syntax. You are given:\n"
            "1. The current tool description\n"
            "2. The input parameters the agent passed\n"
            "3. The error returned by the tool execution\n\n"
            "Analyze why the agent passed the wrong parameters and rewrite the tool description "
            "to explicitly warn the agent about the syntax rules and constraints. Output a JSON object containing:\n"
            "{\n"
            '  "critique": "Explanation of why the agent failed and what instructions to add to the tool description.",\n'
            '  "refined_description": "The new, fully optimized tool description."\n'
            "}"
        )
        
        user_content = (
            f"### Current Tool Description:\n{current_desc}\n\n"
            f"### Agent Passed Argument:\n{agent_input}\n\n"
            f"### Tool Execution Error:\n{tool_error}\n\n"
            "Please generate the optimized JSON."
        )
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            result = json.loads(response.choices[0].message.content)
            return result.get("critique", ""), result.get("refined_description", "")
        except Exception as e:
            return str(e), current_desc
