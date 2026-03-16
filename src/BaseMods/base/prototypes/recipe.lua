local wood = data:get_prototype("resource", "wood")
local ore = data:get_prototype("resource", "ore")
local brick = data:get_prototype("resource", "brick")
local cow = data:get_prototype("resource", "cow")
local buckwheat = data:get_prototype("resource", "buckwheat")

data:extend{
    {
        type="recipe",
        name="build-village",
        display_name="Build Village",
        result=data:get_prototype("settlement", "village"),
        ingredients={
            {
                type="ingredient",
                resource=data:id(wood),
                amount=1
            },
            {
                type="ingredient",
                resource=data:id(brick),
                amount=1
            },
            {
                type="ingredient",
                resource=data:id(cow),
                amount=1
            },
            {
                type="ingredient",
                resource=data:id(buckwheat),
                amount=1
            }
        }
    },
    {
        type="recipe",
        name="build-city",
        display_name="Build City",
        result=data:get_prototype("settlement", "city"),
        ingredients={
            {
                type="ingredient",
                resource=data:id(buckwheat),
                amount=2
            },
            {
                type="ingredient",
                resource=data:id(ore),
                amount=3
            }
        }
    }
}
