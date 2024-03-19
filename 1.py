import sys, json

try:
    with open("sets.json", "rt") as f:
        sets = json.load(f)
except:
    sets = dict()


def on_error(description, task=None):
    print(f"Error: {description}")
    if task: print(f"while executing \"{ ' '.join(task) }\"")
    print("Changes will not be applied. Use -h for help")
    exit()

def help_(*args):
    print("""usage: 1.py [{command} [argument]...]...
commands:
    -i name [element]...        input set of elements and assign to name "name" 
    -o name                     output set named "name"
    -a name element             insert "element" into set named "name"
    -d name element             delete "element" from set named "name"
    -L, -l                      list names of all sets
    -h                          help
    """)

def list_sets():
    print(*(sets.keys()))

def input_set(name, *elms):
    if name in sets: print(f"set \"{name}\" exists and will be overwriten")
    sets[name] = []
    for i in elms: add_to_set(name, i)
    print(f"\"{name}\" created")

def output_set(name):
    if sets[name]:
        set_str = "{"+(', '.join(sets[name]))+"}"
    else:
        set_str = "\u2205"
    print(f"{name}={set_str}")
    
def add_to_set(name, elm):
    if elm not in sets[name]:
        sets[name].append(elm)

def del_from_set(name, elm):
    try:
        sets[name].remove(elm)
    except ValueError:
        print(f"NIL: {elm} not in set {name}")
 
actions = {
    "-i": input_set,
    "-o": output_set,
    "-a": add_to_set,
    "-d": del_from_set,
    "-h": help_,
    "-L": list_sets,
    "-l": list_sets,
    None: lambda x:None, # for triggering task execution before exit
    }

def parse(args):
    task = [args[0]]
    for arg in args[1:]:
        if arg in actions:
            try:
                actions[task[0]](*task[1:])
            except TypeError:
                on_error("wrong amount of arguments", task)
            except KeyError:
                on_error("no set with such name", task)
            except ValueError:
                on_error("no set with such name", task)
            task.clear()
        task.append(arg)
    return

if __name__ == "__main__":
    args = list(sys.argv[1:])+[None]
    if len(args)<=1:
        print("No arguments provided. Use -h for help")
    elif args[0] not in actions:
        on_error(f"first argument \"{args[0]}\" is not valid command")
    parse(args)
    if sets:
        with open("sets.json", "wt") as f:
            json.dump(sets, f)
