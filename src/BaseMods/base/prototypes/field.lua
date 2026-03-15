local outer_bound = data:get_prototype("field", "outer-bound")

outer_bound.display_name = "Deep Sea"
outer_bound.sprite = "__base__/graphics/field/sea.png"

data:extend{
    {
        type="field",
        name="forest",
        display_name="Forest",
        sprite="__base__/graphics/field/forest.png",
        resource=data:id_of("resource", "wood"),
        weight=4,
        minimum_amount=2
    },
    {
        type="field",
        name="grass-field",
        display_name="Grass Field",
        sprite="__base__/graphics/field/grass-field.png",
        resource=data:id_of("resource", "cow"),
        weight=4,
        minimum_amount=2
    },
    {
        type="field",
        name="mountain",
        display_name="Mountain",
        sprite="__base__/graphics/field/mountain.png",
        resource=data:id_of("resource", "ore"),
        weight=3,
        minimum_amount=1
    },
    {
        type="field",
        name="mine",
        display_name="Mine",
        sprite="__base__/graphics/field/mine.png",
        resource=data:id_of("resource", "brick"),
        weight=3,
        minimum_amount=1
    },
    {
        type="field",
        name="field",
        display_name="Field",
        sprite="__base__/graphics/field/field.png",
        resource=data:id_of("resource", "buckwheat"),
        weight=4,
        minimum_amount=2
    },
    {
        type="field",
        name="desert",
        display_name="Desert",
        sprite="__base__/graphics/field/desert.png",
        weight=1,
        minimum_amount=0
    }
}
