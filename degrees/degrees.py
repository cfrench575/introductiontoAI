import csv
import sys

from util import Node, StackFrontier, QueueFrontier

#exec(open('degrees.py').read())

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])
    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }
    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    #print("ello")
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    print(directory)

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    # namepairs = {k: names[k] for k in list(names)[:10]}
    # namekeys = [names[k] for k in sorted(names.keys())[:10]]
    # print(namepairs)
    # print(namekeys)
    # peoplepairs = {k: people[k] for k in list(people)[:10]}
    # peoplekeys = [people[k] for k in sorted(people.keys())[:10]]
    # print(peoplepairs)
    # print(peoplekeys)
    # moviespairs = {k: movies[k] for k in list(movies)[:10]}
    # movieskeys = [movies[k] for k in sorted(movies.keys())[:10]]
    # print(moviespairs)
    # print(movieskeys)
    # print(people)s
    # print(movies)

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")
    print(source)
    print(target)
    path = shortest_path(source, target)
     
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")



##pseudo code: start with initial state,  check each node in frontier - apply test yo check for goal.
#  If frontier is empty, no solution
# if node is not solution, remove from list - expand search to neighbor nodes
# keep track of what has already been explored
# if node not solution, explore neighbors
#if node is solution, return path to get there as solution

#https://www.redblobgames.com/pathfinding/a-star/implementation.html
#good pseudo code https://medium.com/tebs-lab/breadth-first-search-and-depth-first-search-4310f3bf8416
##parent is previous person/movie
##action is movie person in


##source is person - is a state input (node)

##frontier is a class, node is class

def shortest_path(source, target):
    #instantiating class
    frontier = QueueFrontier()
    # add function QueueFrontier class (state, parent, action)
    frontier.add(Node(source, None, None))
    #set of already explored nodes to set aside
    already_explored_nodes = []
    if source == target:
        sys.exit("0 degrees of separation")
    #loops through these lines of code
    while True:
        if frontier.empty():
            return None
        #nodes we have not visited that are connected to nodes we have visited = frontier
        #remove node from frontier to explore
        node = frontier.remove()
        #check for solution
        if node.state == target:
            path = []
            #if parent is none, starting node so
            while node.parent is not None:
                #iterates out through parents of solution
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path
        #set aside explored node    
        already_explored_nodes.append(node.state)
        ##Check all other people in current movie
        for movie_id, person_id in neighbors_for_person(node.state):
            #make sure they haven't been explored
            if not (person_id in already_explored_nodes):
                #current node, parent node, movie - adds each neighbor to frontier
                #state, parent, action
                neighbor = Node(person_id, node, movie_id)
                frontier.add(neighbor)


###other solution - breadth first from both source and target, compare frontiers and seeing if they intersect
## only works if there is a solution - how to handel two not connected people?


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
