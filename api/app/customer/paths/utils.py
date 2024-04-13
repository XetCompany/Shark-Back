import sys

from app.models import (
    User, Cart, City, PointInCity, PointType, PathType, ProductInWarehouse, GroupPaths, GroupPath,
    Path, ProductCompany, GroupPathsRelation, SearchInfo,
)


def search_paths(user: User, filters: dict, pickup_point: PointInCity, limit: int = 10):
    # ToDo: А если склад и пункт выдачи в одном городе?

    cart = Cart.objects.get_or_create(user=user)[0]
    first_cart_product = cart.products.first()
    if not first_cart_product:
        return None

    company = first_cart_product.product.company

    nodes = get_nodes()
    graph_data = get_graph_data(company, filters)
    get_path_value = get_func_get_path_value(filters)
    graph = Graph(nodes, graph_data, get_path_value)
    start_node = pickup_point.city.name
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=start_node)

    sorted_shortest_path = list(sorted(shortest_path.items(), key=lambda x: x[1]))
    warehouse_cities = PointInCity.objects.filter(company=company, type=PointType.WAREHOUSE).values_list('city__name', flat=True)
    warehouse_cities = list(warehouse_cities)
    sorted_shortest_path = list(filter(lambda x: x[0] in warehouse_cities, sorted_shortest_path))
    sorted_shortest_path = list(filter(lambda x: x[1] != sys.maxsize, sorted_shortest_path))

    warehouses_details = get_warehouses_products_details_for_paths(
        cart,
        company,
        sorted_shortest_path,
        previous_nodes,
        start_node,
        filters,
    )
    warehouses_details = warehouses_details[:limit]
    generate_search_infos(warehouses_details, cart, company)

    return warehouses_details


def get_warehouses_products_details_for_paths(
    cart, company, sorted_shortest_path, previous_nodes, start_node, filters
):
    cart_products = get_dict_products_from_cart(cart)
    warehouses_details = []
    warehouses_detail = []
    for target_node, _ in sorted_shortest_path:
        warehouse_products = ProductInWarehouse.objects.filter(
            warehouse__city__name=target_node, product__company=company, warehouse__type=PointType.WAREHOUSE
        ).all()
        warehouse_products = list(warehouse_products)
        decreased_products = decrease_products(cart_products, warehouse_products)

        if decreased_products:
            paths_info = get_paths_from_product(target_node, previous_nodes, start_node)

            is_filter = filtering_paths_info(paths_info, filters)
            if not is_filter:
                continue

            warehouses_detail.append(
                {
                    'products': decreased_products,
                    'paths_info': paths_info,
                    'city': target_node,
                }
            )

        if not cart_products and warehouses_detail:
            warehouses_details.append(warehouses_detail)
            warehouses_detail = []
            cart_products = get_dict_products_from_cart(cart)

    return warehouses_details


def filtering_paths_info(paths_info, filters):
    total_price = sum([path_info[0].price for path_info in paths_info])
    total_time = sum([path_info[0].time for path_info in paths_info])
    total_distance = sum([path_info[0].length for path_info in paths_info])

    if filters['min_price'] is not None and total_price < filters['min_price']:
        return False

    if filters['max_price'] is not None and total_price > filters['max_price']:
        return False

    if filters['min_time'] is not None and total_time < filters['min_time']:
        return False

    if filters['max_time'] is not None and total_time > filters['max_time']:
        return False

    if filters['min_distance'] is not None and total_distance < filters['min_distance']:
        return False

    if filters['max_distance'] is not None and total_distance > filters['max_distance']:
        return False

    return True


def decrease_products(cart_products, warehouse_products):
    deacreased_products = {}
    for warehouse_product in warehouse_products:
        wh_product_id = warehouse_product.product.id
        if wh_product_id in cart_products:
            decrease_count = min(cart_products[wh_product_id], warehouse_product.count)
            cart_products[wh_product_id] -= decrease_count

            deacreased_products[wh_product_id] = decrease_count

            if cart_products[wh_product_id] == 0:
                del cart_products[wh_product_id]

    return deacreased_products


def generate_search_infos(warehouses_details, cart, company):
    for warehouse_detail_group in warehouses_details:
        search_info = SearchInfo.objects.create(
            user=cart.user,
        )
        for warehouse_detail in warehouse_detail_group:
            for product_id, count in warehouse_detail['products'].items():
                product = ProductCompany.objects.get(id=product_id, company=company)
                warehouse = PointInCity.objects.get(city__name=warehouse_detail['city'], company=company, type=PointType.WAREHOUSE)
                group_paths = GroupPaths.objects.create(
                    product=product,
                    count=count,
                    warehouse=warehouse,
                )

                for path, is_reverse in warehouse_detail['paths_info']:
                    group_path = GroupPath.objects.create(
                        path=path,
                        is_reversed=is_reverse,
                    )
                    GroupPathsRelation.objects.create(
                        group_paths=group_paths,
                        group_path=group_path,
                    )

                if not warehouse_detail['paths_info']:
                    group_paths.is_instant_delivery = True
                    group_paths.instant_city = City.objects.get(name=warehouse_detail['city'])
                    group_paths.save()

                search_info.groups_paths.add(group_paths)


def get_paths_from_product(target_node, previous_nodes, start_node):
    paths = []
    node = target_node
    while node != start_node:
        previous_node, path = previous_nodes[node]
        paths.append(path)
        node = previous_node

    paths = list(reversed(paths))

    paths_with_info = []
    need_start_node = start_node
    for path in paths:
        if path.point_a.name == need_start_node:
            paths_with_info.append((path, False))
            need_start_node = path.point_b.name
        else:
            paths_with_info.append((path, True))
            need_start_node = path.point_a.name

    return paths_with_info


def decrease_warehouse_product_count(company, warehouses_details):
    # TODO: неактульно неправильно
    for warehouse_detail_group in warehouses_details:
        for warehouse_detail in warehouse_detail_group:
            for product_id, count in warehouse_detail['products'].items():
                product = ProductInWarehouse.objects.get(
                    warehouse__city__name=warehouse_detail['city'],
                    product__id=product_id,
                    product__company=company,
                )
                product.count -= count

                # if product.count == 0:
                #     product.delete()
                # else:
                #     product.save()


def get_dict_products_from_cart(cart):
    products = {}
    for product in cart.products.all():
        if product.product.name not in products:
            products[product.product.id] = 0

        products[product.product.id] += product.count

    return products



def get_nodes():
    return [city.name for city in City.objects.all()]


def get_graph_data(company: User, filters):
    types = {
        'is_automobile': PathType.AUTOMOBILE,
        'is_railway': PathType.RAILWAY,
        'is_sea': PathType.SEA,
        'is_river': PathType.RIVER,
        'is_air': PathType.AIR,
    }
    available_types = [types[key] for key, value in filters.items() if value and key in types]

    data = {}
    for path in company.paths.all():
        if path.type not in available_types:
            continue

        if path.point_a.name not in data:
            data[path.point_a.name] = {}

        data[path.point_a.name][path.point_b.name] = path

    return data


def get_func_get_path_value(filters):
    if filters['sort_by'] == 'price':
        return lambda path: path.price
    elif filters['sort_by'] == 'time':
        return lambda path: path.time
    elif filters['sort_by'] == 'distance':
        return lambda path: path.distance
    elif filters['sort_by'] == 'all':
        return lambda path: path.price * path.time * path.distance


class Graph:
    def __init__(self, nodes, init_graph, get_path_value):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        self.get_path_value = get_path_value

    def construct_graph(self, nodes, init_graph):
        """
        Этот метод обеспечивает симметричность графика. Другими словами, если существует путь от узла A к B со значением V, должен быть путь от узла B к узлу A со значением V.
        """
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    def get_nodes(self):
        """Возвращает узлы графа"""
        return self.nodes

    def get_outgoing_edges(self, node):
        """Возвращает соседей узла"""
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False):
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        """Возвращает значение ребра между двумя узлами."""
        return self.get_path_value(self.graph[node1][node2])


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())

    # Мы будем использовать этот словарь, чтобы сэкономить на посещении каждого узла и обновлять его по мере продвижения по графику
    shortest_path = {}

    # Мы будем использовать этот dict, чтобы сохранить кратчайший известный путь к найденному узлу
    previous_nodes = {}

    # Мы будем использовать max_value для инициализации значения "бесконечности" непосещенных узлов
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # Однако мы инициализируем значение начального узла 0
    shortest_path[start_node] = 0

    # Алгоритм выполняется до тех пор, пока мы не посетим все узлы
    while unvisited_nodes:
        # Приведенный ниже блок кода находит узел с наименьшей оценкой
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # Приведенный ниже блок кода извлекает соседей текущего узла и обновляет их расстояния
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            path = graph.graph[current_min_node][neighbor]
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node, path

        # После посещения его соседей мы отмечаем узел как "посещенный"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Добавить начальный узел вручную
    path.append(start_node)

    print("Найден следующий лучший маршрут с ценностью {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))

