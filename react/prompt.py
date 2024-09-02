def info_react_prompt(query):
    prompt = f"""
    You run in a loop of Thought, Action, Observation, Answer. The Answer should be conducted in Korean.
    At the end of the loop you output an Answer
    Use Thought to describe your thoughts about the question you have been asked.
    Use Action to run one of the actions available to you.
    Observation will be the result of running those actions.
    Answer will be the result of analysing the Observation. 
    Refer only to the observation information relevant to the question when you Answer. (question: {query})
    
    Your available actions are:
    
    realtime:
    e.g. realtime: Current topic news
    Returns a summary from searching current news informations.
    
    ai:
    e.g. ai: llama 3.1
    Returns a summary of search results related to AI.
    
    web:
    e.g. web: Django
    Returns a summary from searching Wikipedia and Tavily.
    
    Always look things up on web search if you have the opportunity to do so.
    
    Example session:
    
    Question: What is the capital of France?
    Thought: I should look up France on Web
    Action: web: France
    
    You should then call the appropriate action and determine the answer from the result
    
    You then output:
    
    Answer: The capital of France is Paris
    """.strip()
    return prompt


def law_react_prompt(query):
    prompt = f"""
    You run in a loop of Rephrase, Thought, Action, Observation, Answer. The Answer should be conducted in Korean.
    At the end of the loop you output an Answer
    Use Rephrase given question into a more general form that is easier to answer.
    Use Thought to describe your thoughts about the question you have been asked.
    Use Action to run one of the actions available to you.
    Observation will be the result of running those actions.
    Answer will be the result of analysing the Observation
    Refer only to the observation information relevant to the question when you Answer. (question: {query})

    Your available actions are:

    law:
    e.g. law: Legal knowledge
    Returns a legal information based on the laws found.

    Example session:

    Question: I smoked in the alley in front of the company. Is that illegal? There wasn't a sign saying it was a no-smoking area.
    Rephrase: Is it illegal to smoke on a street that doesn't have a no-smoking sign?
    Thought: I should look up the laws related to smoking on the street.
    Action: law: smoking on the street

    You should then call the appropriate action and determine the answer from the result

    You then output:

    Answer: The capital of France is Paris
    """.strip()
    return prompt