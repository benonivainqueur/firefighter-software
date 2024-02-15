

def count(list):
    return len(list)

# add in some functions here. dont forget that you may need some imports. look at some python examples online to see how to get started. 


def list_to_dict(list):
    return {i: list[i] for i in range(0, len(list))}

def dict_to_list(dict):
    return [dict[i] for i in range(0, len(dict))]

# main method
if __name__ == "__main__":
    print("Hello, world!")
    print("count" , count([1,2,3,4,5]))
    print("list to dict", list_to_dict([1,2,3,4,5]))
    print("dict to list: " , dict_to_list({0: 1, 1: 2, 2: 3, 3: 4, 4: 5}))