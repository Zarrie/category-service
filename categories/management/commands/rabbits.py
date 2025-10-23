from django.core.management.base import BaseCommand
from categories.models import Category, CategorySimilarity
from collections import deque, defaultdict

class Command(BaseCommand):
    help = "Print longest rabbit hole and rabbit islands"

    def handle(self, *args, **options):
        # build adjacency
        adj = defaultdict(set)
        for e in CategorySimilarity.objects.all().values_list("cat_left_id", "cat_right_id"):
            a, b = e
            adj[a].add(b); adj[b].add(a)

        nodes = set(Category.objects.values_list("id", flat=True))
        visited = set()
        islands = []

        def bfs(start):
            q = deque([start])
            parent = {start: None}
            visited_local = {start}
            order = []
            while q:
                u = q.popleft()
                order.append(u)
                for v in adj[u]:
                    if v not in visited_local:
                        visited_local.add(v)
                        parent[v] = u
                        q.append(v)
            return order, parent

        # connected components
        for n in nodes:
            if n in visited:
                continue
            comp, _ = bfs(n)
            visited |= set(comp)
            islands.append(comp)

        # longest shortest path per island (diameter via double BFS)
        best_path = []
        def bfs_farthest(src):
            q = deque([src]); dist = {src:0}; parent = {src:None}
            far = src
            while q:
                u = q.popleft()
                if dist[u] > dist[far]: far = u
                for v in adj[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        q.append(v)
            return far, parent

        for comp in islands:
            if not comp:
                continue
            x, _ = bfs_farthest(comp[0])
            y, parent = bfs_farthest(x)
            path = []
            cur = y
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            if len(path) > len(best_path):
                best_path = path

        # print results
        id_to_name = dict(Category.objects.values_list("id", "name"))
        def pretty(ids): return " -> ".join(f"{id_to_name.get(i,'?')}({i})" for i in ids)

        self.stdout.write("Longest rabbit hole:")
        self.stdout.write(pretty(best_path))

        self.stdout.write("\nRabbit islands:")
        for comp in islands:
            line = ", ".join(f"{id_to_name.get(i,'?')}({i})" for i in comp)
            self.stdout.write(f"- {line}")