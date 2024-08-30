def res_check_hitl(llm,state):
    generate=state["generate"]
    iter_count=state["iter_count"]
    if iter_count >2:
        input(f"--------------------------------------------\n\n질문을 수정하여 다시 시도해 주세요.\n\n")
        return "yes"
    else:
        response = input(f"--------------------------------------------\n\n[y/n] 아래 답변이 충분하다면 y를 입력해 주세요.: \n{generate}\n\n")
        if response == "n":
            return "no"
        else: return "yes"