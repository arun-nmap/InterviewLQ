from duckduckgo_search import ddg

def get_ideal_answer(question):
    res = ddg(question, max_results=1)
    return res[0]["body"] if res else ""
