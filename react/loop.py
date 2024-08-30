import re
action_re = re.compile(r'^Action: (\w+): (.*)$')

def get_final_answer(generator):
    return generator.messages[-1]['content']
    
def loop(query, generator,known_actions, max_turns=10):
    i = 0
    react_process=""
    action_agent=[]
    observations=""
    next_prompt = query
    while i < max_turns:
        i += 1
        result = generator(next_prompt)
        react_process+= f'[{i}], {result} \n'
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            action, action_input = actions[0].groups()
            action_agent.append(action)
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(f" -- running {action} -- \n")
            react_process+= f"**[ -- running {action} -> {action_input} -- ]** \n"
            observation = known_actions[action](action_input)
            if observation:
                react_process+=f"Observation: {observation} \n"
                observations+=f"{observation} \n"
                next_prompt = "Observation: {}".format(observation)
                print('_________________')
        else: break
        if "Answer" in result and i >1:
            break
    return get_final_answer(generator).split("Answer")[-1].strip(":"), react_process, action_agent,observations