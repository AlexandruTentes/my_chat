def search_by_id(account_id):
    path = "db/accounts/"

    characters_array = list(account_id)
    path += characters_array[0].lower()

    try:
        with open(path) as read_file:
            for each_line in read_file:
                #line.append(each_line)
                aux_line = each_line
                aux_line = aux_line.split()
                if aux_line[1] == account_id:
                    return aux_line
    except:
        return False
