# pylint: disable=missing-docstring

query_resp =\
    [
        {
            id: "509488",
            pillar_name: 'recipes',
            image: "https://spoonacular.com/recipeImages/A-High-Protein-Snack--Healthy-Almond-Joy-Cheesecake-%7BGluten-Free--Low-Carb-+-High-Protein%7D-509488.jpg",
            contexts:
                [
                    """Healthy Almond Joy "<span class="search-context">Cheese</span>cake" is a Southern recipe that serves 1""",
                    """Cup Low Fat Cottage <span class=\"search-context\">Cheese""",
                    """combine the cottage <span class="search-context">cheese</span>, protein powder""",
                    """scrape the sides down multiple times until its <span class="search-context">cream</span>y."""
                ]
        },
        {
            id: "408444",
            pillar_name: "grocery_items",
            image: "https://spoonacular.com/productImages/408444-636x393.jpg",
            contexts:
                [
                    """All Natural Sour <span class="search-context">Cream</span>cake"""",
                    """Dairy Sour <span class=\"search-context\">Cream</span> Pure And Natural""",
                    """Shurfresh Sour <span class="search-context">Cream</span> - Cultured Grade A Pasteurized""",
                    """Daisy Brand Sour <span class="search-context">Cream</span>, 5 lb"""
                ]
        },
        {
            id: "19228",
            pillar_name: "ingredients",
            image: "https://storage.googleapis.com/vennfridge/saved_ingredient_images%2F19228.jpg",
            contexts:
                [
                    """<span class="search-context">Cream Cheese Frosting</span>"""",
                    """Carrot Sheet Cake with <span class="search-context">Cream Cheese Frosting</span>""""
                ]
        },
        {
            id: "Dip",
            pillar_name: "tags",
            image: "http://vennfridge.me/static/images/tags/Dip.png",
            contexts:
                [
                    """Avocado Goat <span class="search-context">Cheese</span> Dip with Whole-Wheat Pita Chips"""",
                    """Nacho <span class="search-context">Cheese</span> Sauce""""
                ]
        }
    ]


"""

def mock_loop_list(li: List[Any], page: int, page_size: int, maxsize: int):
    # pylint: disable=invalid-name
    assert page >= 0
    assert page_size > 0
    assert maxsize > 0
    assert page * page_size < maxsize

    first_entry = (page * page_size) % len(li)
    resultlist = li[first_entry: min(first_entry + page_size, len(li))]
    entries_left = max(0, page_size - len(resultlist))
    while entries_left > 0:
        entries_to_add = min(len(li), entries_left)
        resultlist += li[:entries_to_add]
        entries_left = entries_left - entries_to_add

    assert len(resultlist) > 0
    return resultlist


def loop_filter_sort(query_params: QueryParams, li: List[Any]):
    # pylint: disable=invalid-name

    def generate_tag_filter(tag_filters: List[int]):
        def filter_func(ele: Any):
            if len(tag_filters) == 0:
                return True

            for tag in tag_filters:
                if tag in ele["tags"]:
                    return True
            return False
        return filter_func

    li = sorted(li, key=query_params.sort_key[0],
                reverse=query_params.sort_key[1])
    li = mock_loop_list(li, query_params.page, query_params.page_size,
                        MOCK_DATA_MAX_SIZE)
    return list(filter(generate_tag_filter(query_params.tag_filters), li))

"""
