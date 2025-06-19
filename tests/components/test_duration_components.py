from components.duration_components import SelectId, get_duration_components


def test_get_duration_components_includes_all_selects():
    components = get_duration_components()
    select_ids = set()
    for component in components:
        assert len(component.components) == 1
        select_ids.add(component.components[0].to_dict()["custom_id"])
    for select in SelectId:
        assert select in select_ids
