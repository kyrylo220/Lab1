class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight


def kruskal_mst(edges, num_vertices):
    # Сортуємо ребра за вагою
    edges.sort(key=lambda x: x.weight)

    # Ініціалізуємо множини підмножин для кожного вершини
    parent = [i for i in range(num_vertices)]
    rank = [0 for _ in range(num_vertices)]

    def find(u):
        # Знаходимо корінь дерева, якому належить вершина u
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        # З'єднуємо два дерева за їх рангами
        root_u = find(u)
        root_v = find(v)

        if rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        elif rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        else:
            parent[root_v] = root_u
            rank[root_u] += 1

    # Результуючий остовий граф
    mst = []

    # Кількість ребер, які має бути додано в остове дерево
    num_edges_added = 0

    # Поки не додано достатньо ребер або не враховані всі ребра
    while num_edges_added < num_vertices - 1 and edges:
        edge = edges.pop(0)
        u = edge.src
        v = edge.dest

        # Знаходимо корені дерев, яким належать вершини ребра
        root_u = find(u)
        root_v = find(v)

        # Якщо вершини належать різним деревам, додаємо ребро до остового дерева
        if root_u != root_v:
            mst.append(edge)
            num_edges_added += 1
            # З'єднуємо дерева
            union(root_u, root_v)

    return mst


# Зчитуємо матрицю інцидентності з файлу
def read_incidence_matrix(file_name):
    matrix = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            row = list(map(int, line.strip().split()))
            matrix.append(row)
    return matrix


# Основна функція
if __name__ == "__main__":
    # Введіть назву файлу з матрицею інцидентності
    file_name = input("Введіть назву файлу з матрицею інцидентності: ")

    # Зчитуємо матрицю інцидентності з файлу
    incidence_matrix = read_incidence_matrix(file_name)

    # Кількість вершин у графі
    num_vertices = len(incidence_matrix)

    # Список ребер графу
    edges = []

    # Проходимо по матриці інцидентності та додаємо ребра в список edges
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if incidence_matrix[i][j] != 0:
                weight = incidence_matrix[i][j]
                edges.append(Edge(i, j, weight))

    # Знаходимо Мінімальне остове дерево Крускала
    mst = kruskal_mst(edges, num_vertices)

    # Виводимо ребра Мінімального остового дерева
    print("Ребра Мінімального остового дерева:")
    for edge in mst:
        print(f"{edge.src} - {edge.dest} : вага = {edge.weight}")