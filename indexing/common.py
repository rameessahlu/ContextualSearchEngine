def createSubQueryList(tokens, token_type='bigram', clause_type='must'):
    sub_query_list = []
    for token in tokens:
        if token is not None and token_type == 'bigram' and len(token.split()) == 2:
            sub_query_list.append({'term' : {'tags' : token}})
        elif (token is not None and token_type == 'unigram' and len(token.split()) == 1):
            sub_query_list.append({'term' : {'tags' : token}})
    sub_query_list = {clause_type: sub_query_list}
    print('DEBUG# Token:{} Clause:{} subQuery:{}'.format(token_type, clause_type, str(sub_query_list)))
    return sub_query_list